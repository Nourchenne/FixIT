"""Évaluer la recherche documentaire de FixIT (Recall@k et MRR@k).

Interroge la collection Qdrant active via assistant.services.retrieval et
mesure la qualité du classement sur le jeu de questions annoté.

Lancer depuis la racine du dépôt (là où se trouve manage.py), Qdrant Docker
démarré :

    python -m evaluation.evaluate_retrieval
    python -m evaluation.evaluate_retrieval --limit 10

Définitions utilisées (voir evaluation/README.md) :
- Pertinence au niveau DOCUMENT : un passage est pertinent si son doc_id
  figure dans les doc_ids attendus de la question (gold_doc_ids). Trouver
  l'un des guides attendus suffit à répondre.
- Recall@k : proportion de questions répondables pour lesquelles au moins un
  passage pertinent apparaît dans les k premiers résultats (hit-rate@k).
- MRR@10 : moyenne de 1/rang du premier passage pertinent (0 s'il est absent
  des 10 premiers).
Les questions hors corpus sont exclues de Recall/MRR (cahier des charges :
moyenne sur les questions répondables) ; on y mesure plutôt le score du
meilleur passage, pour vérifier qu'il reste plus bas que sur les questions
répondables.
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
# Permet d'importer les services du projet quel que soit le mode de lancement.
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from assistant.services.retrieval import search_documents  # noqa: E402

QUESTIONS_FILE = BASE_DIR / "evaluation" / "questions.jsonl"
RESULTS_DIR = BASE_DIR / "evaluation" / "results"
K_VALUES = (5, 10)
MAX_K = 10


def load_questions(path):
    """Lire le jeu de questions annoté (un objet JSON par ligne)."""
    if not path.is_file():
        raise FileNotFoundError(f"Jeu de questions introuvable : {path}")

    questions = []
    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                questions.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Ligne JSON invalide {line_number} dans {path.name}."
                ) from error

    if not questions:
        raise ValueError("Le jeu de questions est vide.")

    return questions


def rank_of_first_relevant(passages, gold_doc_ids):
    """Rang (1..N) du premier passage dont le doc_id est attendu, sinon 0."""
    gold = set(gold_doc_ids)
    for rank, passage in enumerate(passages, start=1):
        doc_id = (passage.get("metadata") or {}).get("doc_id")
        if doc_id in gold:
            return rank
    return 0


def top_score(passages):
    """Score du meilleur passage renvoyé, ou None si aucun résultat."""
    return passages[0]["score"] if passages else None


def evaluate(questions, limit, retrieve):
    """Interroger la recherche pour chaque question et agréger les mesures.

    retrieve(question, limit) -> liste de passages ordonnés (dense ou reranké).
    """
    details = []
    answerable = [q for q in questions if q.get("answerable", True)]
    out_of_corpus = [q for q in questions if not q.get("answerable", True)]

    # Accumulateurs globaux et par sous-groupe (langue, cas).
    totals = {f"recall@{k}": 0.0 for k in K_VALUES}
    totals["mrr@10"] = 0.0
    by_lang = defaultdict(lambda: {"n": 0, **{f"recall@{k}": 0.0 for k in K_VALUES}, "mrr@10": 0.0})
    by_cas = defaultdict(lambda: {"n": 0, **{f"recall@{k}": 0.0 for k in K_VALUES}, "mrr@10": 0.0})

    for question in answerable:
        passages = retrieve(question["question"], limit)
        rank = rank_of_first_relevant(passages, question.get("gold_doc_ids", []))
        reciprocal = 1.0 / rank if rank else 0.0

        row = {
            "query_id": question.get("query_id"),
            "lang": question.get("lang"),
            "cas": question.get("cas"),
            "question": question["question"],
            "gold_doc_ids": question.get("gold_doc_ids", []),
            "retrieved": [
                {
                    "doc_id": (p.get("metadata") or {}).get("doc_id"),
                    "page": (p.get("metadata") or {}).get("page"),
                    "score": round(float(p["score"]), 4),
                }
                for p in passages
            ],
            "first_relevant_rank": rank,
            "reciprocal_rank": round(reciprocal, 4),
        }
        for k in K_VALUES:
            hit = 1.0 if rank and rank <= k else 0.0
            row[f"hit@{k}"] = hit
            totals[f"recall@{k}"] += hit
            by_lang[question.get("lang")][f"recall@{k}"] += hit
            by_cas[question.get("cas")][f"recall@{k}"] += hit
        totals["mrr@10"] += reciprocal
        by_lang[question.get("lang")]["mrr@10"] += reciprocal
        by_cas[question.get("cas")]["mrr@10"] += reciprocal
        by_lang[question.get("lang")]["n"] += 1
        by_cas[question.get("cas")]["n"] += 1
        details.append(row)

    n = len(answerable)
    summary = {f"recall@{k}": round(totals[f"recall@{k}"] / n, 4) for k in K_VALUES}
    summary["mrr@10"] = round(totals["mrr@10"] / n, 4)
    summary["n_answerable"] = n

    def finalize(group):
        out = {}
        for key, acc in group.items():
            m = acc["n"] or 1
            out[key] = {
                "n": acc["n"],
                **{f"recall@{k}": round(acc[f"recall@{k}"] / m, 4) for k in K_VALUES},
                "mrr@10": round(acc["mrr@10"] / m, 4),
            }
        return out

    # Analyse des hors-corpus : distribution du meilleur score.
    out_scores = []
    out_details = []
    for question in out_of_corpus:
        passages = retrieve(question["question"], limit)
        score = top_score(passages)
        if score is not None:
            out_scores.append(float(score))
        out_details.append({
            "query_id": question.get("query_id"),
            "lang": question.get("lang"),
            "question": question["question"],
            "top_score": round(float(score), 4) if score is not None else None,
            "top_doc_id": (passages[0]["metadata"].get("doc_id") if passages else None),
        })

    answerable_top = [d["retrieved"][0]["score"] for d in details if d["retrieved"]]
    hors = {
        "n": len(out_of_corpus),
        "top_score_moyen": round(sum(out_scores) / len(out_scores), 4) if out_scores else None,
        "top_score_max": round(max(out_scores), 4) if out_scores else None,
    }
    if answerable_top:
        hors["rappel_top_score_moyen_repondables"] = round(sum(answerable_top) / len(answerable_top), 4)

    return {
        "summary": summary,
        "by_lang": finalize(by_lang),
        "by_cas": finalize(by_cas),
        "hors_corpus": hors,
        "details": details,
        "hors_corpus_details": out_details,
    }


def print_report(report, limit, collection_hint="", config="dense"):
    s = report["summary"]
    print("\n" + "=" * 64)
    print("BENCHMARK RECHERCHE FixIT")
    print("=" * 64)
    print(f"Configuration : {config}")
    if collection_hint:
        print(f"Collection : {collection_hint}")
    print(f"limit (passages récupérés par question) : {limit}")
    print(f"Questions répondables évaluées : {s['n_answerable']}")
    print("-" * 64)
    print(f"Recall@5  : {s['recall@5']:.3f}")
    print(f"Recall@10 : {s['recall@10']:.3f}")
    print(f"MRR@10    : {s['mrr@10']:.3f}")
    print("-" * 64)
    print("Par langue :")
    for lang, m in sorted(report["by_lang"].items()):
        print(f"  {lang} (n={m['n']:2d}) : "
              f"R@5={m['recall@5']:.3f}  R@10={m['recall@10']:.3f}  MRR@10={m['mrr@10']:.3f}")
    print("-" * 64)
    print("Par cas :")
    for cas, m in sorted(report["by_cas"].items()):
        print(f"  {cas:8s} (n={m['n']:2d}) : "
              f"R@5={m['recall@5']:.3f}  R@10={m['recall@10']:.3f}  MRR@10={m['mrr@10']:.3f}")
    print("-" * 64)
    h = report["hors_corpus"]
    print(f"Hors corpus (n={h['n']}) : top-score moyen={h.get('top_score_moyen')} "
          f"(max={h.get('top_score_max')})")
    if "rappel_top_score_moyen_repondables" in h:
        print(f"  (pour comparaison, top-score moyen des répondables : "
              f"{h['rappel_top_score_moyen_repondables']})")
    print("=" * 64)

    # Lister les questions répondables ratées (aucun doc attendu dans le top-k).
    manques = [d for d in report["details"] if d["first_relevant_rank"] == 0]
    if manques:
        print(f"\nÉchecs ({len(manques)}) — aucun guide attendu dans les {limit} premiers :")
        for d in manques:
            print(f"  [{d['query_id']} {d['lang']} {d['cas']}] {d['question']}")
            print(f"      attendu {d['gold_doc_ids']} | obtenu "
                  f"{[r['doc_id'] for r in d['retrieved'][:3]]}")
    else:
        print("\nAucun échec : chaque question répondable a retrouvé un guide attendu.")


def save_results(report, limit, config="dense"):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = RESULTS_DIR / f"retrieval_{config}_{stamp}.json"
    payload = {
        "date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config": config,
        "limit": limit,
        **report,
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Évaluer la recherche documentaire de FixIT."
    )
    parser.add_argument(
        "--limit", type=int, default=MAX_K,
        help=f"Nombre de passages récupérés par question. Défaut : {MAX_K}.",
    )
    parser.add_argument(
        "--questions", type=Path, default=QUESTIONS_FILE,
        help="Chemin du jeu de questions annoté (.jsonl).",
    )
    parser.add_argument(
        "--rerank", action="store_true",
        help="Ajouter un reranking cross-encoder après la recherche dense.",
    )
    parser.add_argument(
        "--candidates", type=int, default=20,
        help="Candidats récupérés en dense avant reranking. Défaut : 20.",
    )
    args = parser.parse_args()

    if args.limit < max(K_VALUES):
        print(f"Attention : --limit={args.limit} < {max(K_VALUES)}, "
              f"Recall@{max(K_VALUES)} sera sous-estimé.")

    questions = load_questions(args.questions)

    # Choix de la fonction de recherche : dense (référence) ou reranké.
    if args.rerank:
        from assistant.services.reranking import search_documents_reranked
        config = "rerank"

        def retrieve(question, limit):
            return search_documents_reranked(
                question, limit=limit, candidate_limit=args.candidates
            )
    else:
        config = "dense"

        def retrieve(question, limit):
            return search_documents(question, limit=limit)

    collection_hint = ""
    try:
        from assistant.services.retrieval import load_index_info
        collection_hint = load_index_info().get("collection_name", "")
    except Exception:
        pass

    report = evaluate(questions, limit=args.limit, retrieve=retrieve)
    print_report(report, args.limit, collection_hint, config)
    path = save_results(report, args.limit, config)
    print(f"\nRésultats détaillés enregistrés : {path.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
