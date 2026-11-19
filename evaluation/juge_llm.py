"""Noter automatiquement les réponses de FixIT avec un modèle « juge ».

Complète la grille CSV produite par evaluate_generation avec trois colonnes :
note_auto_llm (0, 1 ou 2), raison_auto_llm et modele_juge. La colonne
note_0_1_2, réservée à la notation humaine, n'est jamais modifiée.

Ces notes sont des mesures automatiques, non vérifiées : un modèle d'une autre
famille que le générateur (qwen par défaut) applique le barème du cahier des
charges, puis un échantillon est contrôlé à la main.

    python -m evaluation.juge_llm                  # dernier CSV de generation_*.csv
    python -m evaluation.juge_llm --limite 3       # essai rapide
    python -m evaluation.juge_llm --pause 10       # plus lent, moins de refus Groq
    python -m evaluation.juge_llm --modele openai/gpt-oss-120b --suffixe _2   # second juge
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

QUESTIONS_FILE = BASE_DIR / "evaluation" / "questions_final.jsonl"
SOURCES_FILE = BASE_DIR / "data" / "sources.csv"
RESULTS_DIR = BASE_DIR / "evaluation" / "results"
MODELE_JUGE = "qwen/qwen3.8-27b"
ATTENTE_LIMITE_GROQ = 25
EXTRAIT_MAX = 900

CONSIGNE = """Tu es un évaluateur strict de réponses d'un assistant de dépannage PC et Wi-Fi.
Tu reçois : la question de l'utilisateur, les extraits de guides que l'assistant a lus
(S1, S2, S3), la réponse de l'assistant et les guides attendus pour cette question.

Barème :
- 2 : correcte et complète. Les étapes traitent bien le problème posé et sont
  justifiées par les extraits cités.
- 1 : partiellement correcte. Utile mais incomplète, ou une étape hors sujet, ou une
  source mal choisie.
- 0 : incorrecte. Mauvais problème, procédure absente des extraits (inventée), ou
  réponse de repli ou de clarification alors que la question est couverte par un guide.

Méthode :
1. Les étapes parlent-elles du problème posé ? Si non, la note est 0.
2. Chaque étape se retrouve-t-elle dans l'extrait cité entre crochets ? Une étape
   absente de l'extrait est inventée.
3. Le conseil est-il précis et utile ?
Citer un autre guide que ceux attendus n'est pas une erreur si la réponse reste
pertinente. La langue de la réponse ne compte pas dans la note.

Réponds uniquement par un objet JSON : {"note": 0, "raison": "une phrase courte en français"}.
"note" vaut 0, 1 ou 2."""


def charger_titres():
    with SOURCES_FILE.open(encoding="utf-8-sig") as fichier:
        return {r["doc_id"]: r["titre"] for r in csv.DictReader(fichier)}


def charger_questions():
    questions = {}
    for ligne in QUESTIONS_FILE.read_text(encoding="utf-8").splitlines():
        if ligne.strip():
            item = json.loads(ligne)
            questions[item["query_id"]] = item
    return questions


def dernier_csv():
    fichiers = sorted(RESULTS_DIR.glob("generation_*.csv"))
    if not fichiers:
        raise SystemExit("Aucun fichier generation_*.csv : lancer d'abord evaluate_generation.")
    return fichiers[-1]


def extrait(texte):
    texte = " ".join(texte.split())
    return texte if len(texte) <= EXTRAIT_MAX else texte[:EXTRAIT_MAX].rsplit(" ", 1)[0] + " […]"


def construire_demande(ligne, item, titres, passages):
    attendus = "; ".join(f"{d} ({titres.get(d, '?')})" for d in item.get("gold_doc_ids", []))
    extraits = "\n".join(
        f"[S{i}] {p['metadata'].get('doc_id')} — {p['metadata'].get('titre')} "
        f"(page {p['metadata'].get('page')}) : {extrait(p['page_content'])}"
        for i, p in enumerate(passages, start=1)
    )
    return (
        f"Question : {ligne['question']}\n\n"
        f"Guides attendus : {attendus}\n\n"
        f"Extraits lus par l'assistant :\n{extraits}\n\n"
        f"Réponse de l'assistant (type : {ligne['type']}) :\n{ligne['reponse']}"
    )


def analyser(contenu):
    contenu = re.sub(r"<think>.*?</think>", "", contenu or "", flags=re.S).strip()
    donnees = json.loads(contenu)
    note = donnees.get("note")
    if isinstance(note, str) and note.strip().isdigit():
        note = int(note)
    if note not in (0, 1, 2) or isinstance(note, bool):
        raise ValueError(f"note invalide : {donnees!r}")
    return note, " ".join(str(donnees.get("raison", "")).split())


def juger(client, modele, demande):
    """Un nouvel essai après une limite de débit ; trois au maximum."""
    derniere = None
    for essai in range(1, 4):
        try:
            reponse = client.chat.completions.create(
                model=modele, temperature=0,
                response_format={"type": "json_object"},
                messages=[{"role": "system", "content": CONSIGNE},
                          {"role": "user", "content": demande}],
            )
            return analyser(reponse.choices[0].message.content), ""
        except Exception as erreur:  # noqa: BLE001 — on consigne toute erreur
            derniere = f"{type(erreur).__name__} : {erreur}"
            limite = "RateLimit" in type(erreur).__name__ or "429" in str(erreur)
            if essai < 3 and (limite or isinstance(erreur, (ValueError, json.JSONDecodeError))):
                time.sleep(ATTENTE_LIMITE_GROQ if limite else 2)
                continue
            break
    return None, derniere


def ecrire_csv(lignes, colonnes, chemin):
    with chemin.open("w", encoding="utf-8-sig", newline="") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=colonnes, delimiter=";")
        ecrivain.writeheader()
        ecrivain.writerows(lignes)


def main():
    parser = argparse.ArgumentParser(description="Noter les réponses avec un modèle juge.")
    parser.add_argument("--csv", type=Path, default=None)
    parser.add_argument("--modele", default=MODELE_JUGE)
    parser.add_argument("--pause", type=float, default=6.0,
                        help="Pause entre deux questions, en secondes (limite de débit Groq).")
    parser.add_argument("--limite", type=int, default=0,
                        help="Ne noter que les N premières questions répondables (0 = toutes).")
    parser.add_argument("--suffixe", default="",
                        help="Suffixe ajouté aux trois colonnes (ex. _2 pour un second juge).")
    args = parser.parse_args()
    col_note = "note_auto_llm" + args.suffixe
    col_raison = "raison_auto_llm" + args.suffixe
    col_modele = "modele_juge" + args.suffixe

    from dotenv import load_dotenv
    from groq import Groq

    from assistant.services.retrieval import search_documents

    load_dotenv(BASE_DIR / ".env")
    if not os.getenv("GROQ_API_KEY"):
        raise SystemExit("Configure GROQ_API_KEY dans .env.")
    client = Groq(api_key=os.environ["GROQ_API_KEY"], timeout=60, max_retries=0)

    chemin = args.csv or dernier_csv()
    with chemin.open(encoding="utf-8-sig") as fichier:
        lecteur = csv.DictReader(fichier, delimiter=";")
        colonnes = list(lecteur.fieldnames)
        lignes = list(lecteur)
    colonnes += [c for c in (col_note, col_raison, col_modele) if c not in colonnes]

    questions, titres = charger_questions(), charger_titres()
    cibles = [l for l in lignes
              if questions[l["query_id"]].get("answerable", True) and l["type"] != "erreur"]
    if args.limite:
        cibles = cibles[:args.limite]

    for numero, ligne in enumerate(cibles, start=1):
        print(f"[{numero}/{len(cibles)}] {ligne['query_id']} {ligne['question']}")
        passages = search_documents(ligne["question"], limit=3)
        demande = construire_demande(ligne, questions[ligne["query_id"]], titres, passages)
        resultat, erreur = juger(client, args.modele, demande)
        if resultat is None:
            ligne.update({col_note: "", col_raison: f"ERREUR {erreur}",
                          col_modele: args.modele})
        else:
            note, raison = resultat
            ligne.update({col_note: str(note), col_raison: raison,
                          col_modele: args.modele})
        if numero < len(cibles):
            time.sleep(args.pause)

    ecrire_csv(lignes, colonnes, chemin)
    notes = Counter(l.get(col_note) for l in cibles)
    erreurs = sum(1 for l in cibles if not l.get(col_note))
    notees = [int(l[col_note]) for l in cibles if l.get(col_note)]
    print("\n" + "=" * 64)
    print(f"NOTATION AUTOMATIQUE ({args.modele}) — {chemin.name}")
    print("=" * 64)
    print(f"Réponses notées : {len(notees)} sur {len(cibles)} (erreurs : {erreurs})")
    print(f"Répartition 0 / 1 / 2 : {notes.get('0', 0)} / {notes.get('1', 0)} / {notes.get('2', 0)}")
    if notees:
        print(f"Note moyenne : {sum(notees) / len(notees):.2f}")


if __name__ == "__main__":
    main()
