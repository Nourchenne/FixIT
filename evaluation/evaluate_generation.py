"""Évaluer les réponses générées par FixIT (volet génération du benchmark).

Pour chaque question du jeu de test, appelle answer_question (Qdrant + Groq),
contrôle automatiquement la langue, les citations et le repli, puis écrit une
grille CSV à compléter à la main : une note 0, 1 ou 2 par réponse
(incorrecte, partiellement correcte, correcte et complète — cahier §8).

Lancer depuis la racine du dépôt (Qdrant démarré, .env configuré) :

    python -m evaluation.evaluate_generation
    python -m evaluation.evaluate_generation --limite 5      # essai rapide
    python -m evaluation.evaluate_generation --pause 3       # plus lent, moins de refus Groq

Le fichier produit (evaluation/results/generation_<date>.csv) s'ouvre dans
Excel : séparateur « ; », encodage UTF-8 avec BOM.
"""

import argparse
import csv
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from evaluation.evaluate_retrieval import load_questions  # noqa: E402

QUESTIONS_FILE = BASE_DIR / "evaluation" / "questions_final.jsonl"
RESULTS_DIR = BASE_DIR / "evaluation" / "results"
ATTENTE_LIMITE_GROQ = 20  # secondes avant un nouvel essai si Groq limite le débit

COLONNES = [
    "query_id", "lang", "cas", "question", "langue_obtenue", "langue_ok",
    "type", "sources", "guide_attendu_cite", "repli_correct", "duree_s",
    "reponse", "note_0_1_2", "commentaire",
]


def appeler(question, repondre):
    """Appeler le chat ; un nouvel essai si Groq signale une limite de débit."""
    for essai in (1, 2):
        try:
            return repondre(question), ""
        except Exception as erreur:  # noqa: BLE001 — on consigne toute erreur
            limite = "RateLimit" in type(erreur).__name__ or "429" in str(erreur)
            if limite and essai == 1:
                time.sleep(ATTENTE_LIMITE_GROQ)
                continue
            return None, f"{type(erreur).__name__} : {erreur}"
    return None, "Échec inattendu"


def evaluer_question(item, repondre):
    debut = time.perf_counter()
    resultat, erreur = appeler(item["question"], repondre)
    duree = round(time.perf_counter() - debut, 2)

    ligne = {colonne: "" for colonne in COLONNES}
    ligne.update({"query_id": item.get("query_id"), "lang": item.get("lang"),
                  "cas": item.get("cas"), "question": item["question"], "duree_s": duree})

    if resultat is None:
        ligne.update({"type": "erreur", "reponse": erreur})
        return ligne

    docs = [source["doc_id"] for source in resultat.get("sources", [])]
    attendus = set(item.get("gold_doc_ids", []))
    ligne.update({
        "langue_obtenue": resultat.get("langue", ""),
        "langue_ok": "oui" if resultat.get("langue") == item.get("lang") else "non",
        "type": resultat.get("type", ""),
        "sources": " ".join(docs),
        "reponse": resultat.get("answer", ""),
    })
    if item.get("answerable", True):
        ligne["guide_attendu_cite"] = "oui" if attendus & set(docs) else "non"
        ligne["repli_correct"] = "sans objet"
    else:
        ligne["guide_attendu_cite"] = "sans objet"
        ligne["repli_correct"] = "oui" if resultat.get("type") == "repli" and not docs else "non"
    return ligne


def pourcentage(lignes, colonne, valeur="oui"):
    if not lignes:
        return None
    return round(100 * sum(l[colonne] == valeur for l in lignes) / len(lignes), 1)


def synthese(lignes):
    repondables = [l for l in lignes if l["repli_correct"] == "sans objet"]
    hors = [l for l in lignes if l["guide_attendu_cite"] == "sans objet"]
    durees = [l["duree_s"] for l in lignes if l["type"] != "erreur"]
    return {
        "questions": len(lignes),
        "erreurs": sum(l["type"] == "erreur" for l in lignes),
        "langue_correcte_pct": pourcentage([l for l in lignes if l["type"] != "erreur"], "langue_ok"),
        "repondables_guide_attendu_cite_pct": pourcentage(repondables, "guide_attendu_cite"),
        "repondables_sans_etapes": sum(l["type"] in ("repli", "clarification") for l in repondables),
        "hors_corpus_repli_correct_pct": pourcentage(hors, "repli_correct"),
        "duree_mediane_s": round(statistics.median(durees), 2) if durees else None,
        "duree_max_s": max(durees) if durees else None,
    }


def ecrire_csv(lignes, chemin):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", encoding="utf-8-sig", newline="") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=COLONNES, delimiter=";")
        ecrivain.writeheader()
        ecrivain.writerows(lignes)


def afficher(resume, chemin):
    print("\n" + "=" * 64)
    print("ÉVALUATION DES RÉPONSES FixIT")
    print("=" * 64)
    print(f"Questions traitées           : {resume['questions']} (erreurs : {resume['erreurs']})")
    print(f"Langue correcte              : {resume['langue_correcte_pct']} %")
    print(f"Répondables citant un guide attendu : {resume['repondables_guide_attendu_cite_pct']} %")
    print(f"Répondables sans étapes (repli ou clarification) : {resume['repondables_sans_etapes']}")
    print(f"Hors corpus avec repli correct : {resume['hors_corpus_repli_correct_pct']} %")
    print(f"Durée médiane / maximale     : {resume['duree_mediane_s']} s / {resume['duree_max_s']} s")
    print("=" * 64)
    print(f"Grille à noter (colonne note_0_1_2) : {chemin.relative_to(BASE_DIR)}")


def main():
    parser = argparse.ArgumentParser(description="Évaluer les réponses générées par FixIT.")
    parser.add_argument("--questions", type=Path, default=QUESTIONS_FILE)
    parser.add_argument("--pause", type=float, default=2.0,
                        help="Pause entre deux questions, en secondes (limite de débit Groq).")
    parser.add_argument("--limite", type=int, default=0,
                        help="Ne traiter que les N premières questions (0 = toutes).")
    args = parser.parse_args()

    from assistant.services.chat import answer_question

    questions = load_questions(args.questions)
    if args.limite:
        questions = questions[:args.limite]

    lignes = []
    for numero, item in enumerate(questions, start=1):
        print(f"[{numero}/{len(questions)}] {item['question']}")
        lignes.append(evaluer_question(item, answer_question))
        if numero < len(questions):
            time.sleep(args.pause)

    horodatage = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    chemin = RESULTS_DIR / f"generation_{horodatage}.csv"
    ecrire_csv(lignes, chemin)
    resume = synthese(lignes)
    chemin.with_suffix(".json").write_text(
        json.dumps({"date_utc": horodatage, "questions": str(args.questions), **resume},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    afficher(resume, chemin)


if __name__ == "__main__":
    main()
