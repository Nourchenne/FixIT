"""Évalue la qualité des réponses générées par le chat (pas seulement le
retrieval), avec Ragas et un modèle juge plus gros que celui qui répond.

Deux métriques, qui ne demandent pas de réponse de référence écrite à la
main (questions_final.jsonl n'en contient pas, seulement des gold_doc_ids) :

- faithfulness : la réponse n'invente rien par rapport aux passages fournis
  au modèle (détecte les hallucinations) ;
- answer_relevancy : la réponse adresse bien la question posée.

La pertinence du retrieval lui-même (les bons passages sont-ils trouvés ?)
reste mesurée par evaluate_retrieval.py (Recall@k, MRR@10), qui dispose déjà
des gold_doc_ids pour ça ; ce script ne refait pas cette mesure.

Lancer depuis la racine du dépôt (là où se trouve manage.py), Qdrant Docker
démarré, GROQ_API_KEY configuré dans .env :

    python -m evaluation.evaluate_generation
    python -m evaluation.evaluate_generation --n 40

Chaque question coûte plusieurs appels Groq (génération de la réponse par
le modèle du chat, puis jugement par un modèle plus gros pour chaque
métrique) : --n limite le nombre de questions pour éviter les quotas
pendant les essais.
"""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from groq import BadRequestError, RateLimitError
from langchain_core.embeddings import Embeddings
from langchain_groq import ChatGroq
from ragas import evaluate
from ragas.dataset_schema import EvaluationDataset, SingleTurnSample
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import AnswerRelevancy, Faithfulness
from ragas.run_config import RunConfig

from assistant.services.chat import (
    CANDIDATS_RECHERCHE,
    LIMITE_SOURCES,
    answer_question,
    filtrer_par_marque,
)
from assistant.services.retrieval import search_documents
from documents.services.embeddings import embed_documents, embed_query

BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = BASE_DIR / "questions_final.jsonl"
RESULTS_DIR = BASE_DIR / "results"

# Modèle juge : plus gros que celui qui répond (GROQ_MODEL, ex. gpt-oss-20b),
# pour que l'évaluation ne soit pas faite par le modèle qu'on évalue.
MODELE_JUGE = "openai/gpt-oss-120b"

# Le compte Groq gratuit limite les tokens par minute : on espace les
# questions et on réessaie en cas de dépassement plutôt que de planter.
DELAI_ENTRE_QUESTIONS = 5
TENTATIVES_MAX = 5
PAUSE_APRES_LIMITE = 20


class EmbeddingsE5(Embeddings):
    """Adapte le modèle d'embeddings du projet (multilingual-e5-small) à
    l'interface attendue par Ragas, sans dépendance supplémentaire."""

    def embed_documents(self, texts):
        return [vecteur.tolist() for vecteur in embed_documents(texts)]

    def embed_query(self, texte):
        return embed_query(texte).tolist()


def charger_questions(chemin, n):
    """Les n premières questions répondables du jeu annoté.

    Les questions hors corpus (answerable=false) sont exclues : pour elles,
    le chat répond par un repli sans passage, ce que faithfulness/
    answer_relevancy ne sont pas faits pour juger.
    """
    questions = []
    with chemin.open(encoding="utf-8") as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne:
                questions.append(json.loads(ligne))

    repondables = [q for q in questions if q.get("answerable")]

    if not repondables:
        raise ValueError(f"Aucune question répondable dans {chemin}.")

    return repondables[:n]


def contextes_utilises(question_texte):
    """Les mêmes passages que ceux réellement envoyés au modèle de
    génération par answer_question (même recherche, même filtre marque)."""
    passages = search_documents(question_texte, limit=CANDIDATS_RECHERCHE)
    passages = filtrer_par_marque(passages, question_texte)[:LIMITE_SOURCES]
    return [p["page_content"] for p in passages] or ["(aucun passage retrouvé)"]


def repondre_avec_reessai(question_texte):
    """answer_question, avec pause et réessai si la limite Groq (tokens par
    minute) est atteinte, ou si Groq renvoie un JSON invalide (aléa connu
    des petits modèles en mode JSON, qui disparaît presque toujours au
    deuxième essai) — au lieu de laisser planter tout le lot."""
    for tentative in range(1, TENTATIVES_MAX + 1):
        try:
            return answer_question(question_texte)
        except RateLimitError:
            if tentative == TENTATIVES_MAX:
                raise
            print(f"  Limite Groq atteinte, pause de {PAUSE_APRES_LIMITE}s "
                  f"(essai {tentative}/{TENTATIVES_MAX})...")
            time.sleep(PAUSE_APRES_LIMITE)
        except BadRequestError:
            if tentative == TENTATIVES_MAX:
                raise
            print(f"  Réponse JSON invalide côté Groq, nouvel essai "
                  f"({tentative}/{TENTATIVES_MAX})...")
            time.sleep(2)


def construire_echantillons(questions):
    """Un SingleTurnSample par question : question, contextes réellement
    utilisés, réponse réelle du chat (pipeline complet, pas un extrait)."""
    echantillons = []
    for index, donnee in enumerate(questions):
        if index > 0:
            time.sleep(DELAI_ENTRE_QUESTIONS)
        question_texte = donnee["question"]
        contextes = contextes_utilises(question_texte)
        reponse = repondre_avec_reessai(question_texte)
        echantillons.append(SingleTurnSample(
            user_input=question_texte,
            response=reponse["answer"],
            retrieved_contexts=contextes,
        ))
    return echantillons


def main():
    parser = argparse.ArgumentParser(
        description="Évalue la qualité de génération du chat (faithfulness, "
                    "answer_relevancy) avec Ragas et un modèle juge."
    )
    parser.add_argument(
        "--n", type=int, default=10,
        help="Nombre de questions répondables à évaluer (défaut : 10).",
    )
    parser.add_argument(
        "--questions", type=Path, default=QUESTIONS_FILE,
        help="Jeu de questions annoté (.jsonl). Par défaut : questions_final.jsonl.",
    )
    args = parser.parse_args()

    load_dotenv(BASE_DIR.parent / ".env")

    questions = charger_questions(args.questions, args.n)
    print(f"{len(questions)} question(s) répondable(s) à évaluer...")

    echantillons = construire_echantillons(questions)
    dataset = EvaluationDataset(samples=echantillons)

    juge = LangchainLLMWrapper(ChatGroq(model=MODELE_JUGE, temperature=0))
    embeddings = LangchainEmbeddingsWrapper(EmbeddingsE5())

    # max_workers bas : le compte Groq gratuit limite les tokens par minute,
    # envoyer les appels au juge un par un (plutôt que 16 en parallèle, la
    # valeur par défaut) évite de déclencher la même limite que ci-dessus.
    resultat = evaluate(
        dataset,
        metrics=[Faithfulness(), AnswerRelevancy()],
        llm=juge,
        embeddings=embeddings,
        run_config=RunConfig(max_workers=2, max_retries=10, max_wait=60),
    )

    table = resultat.to_pandas()
    table.insert(0, "query_id", [q["query_id"] for q in questions])
    table.insert(1, "lang", [q["lang"] for q in questions])

    RESULTS_DIR.mkdir(exist_ok=True)
    horodatage = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    chemin_sortie = RESULTS_DIR / f"generation_{horodatage}.csv"
    table.to_csv(chemin_sortie, index=False)

    print("\nMoyennes :")
    print(table[["faithfulness", "answer_relevancy"]].mean().round(3))
    print(f"\nDétail par question : {chemin_sortie}")


if __name__ == "__main__":
    main()
