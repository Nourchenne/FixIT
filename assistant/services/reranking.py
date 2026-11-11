"""Reranking des passages avec un cross-encoder multilingue.

Principe (cours, lab 16) : la recherche dense récupère un vivier large de
candidats, puis un cross-encoder réévalue chaque paire (question, passage) et
les reclasse. Le modèle est multilingue (FR/EN), adapté au corpus FixIT.

On n'écrase pas search_documents : le dense reste la recherche de référence.
Ce module fournit une variante rerankée, utilisée pour la comparaison du
benchmark et, si le gain est confirmé, pour la recherche en production.
"""

from functools import lru_cache

from sentence_transformers import CrossEncoder

from assistant.services.retrieval import search_documents

# Cross-encoder multilingue (même modèle que le lab 16 du cours).
RERANK_MODEL = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"

# Nombre de candidats récupérés en dense avant reranking.
DEFAULT_CANDIDATES = 20


@lru_cache(maxsize=1)
def get_reranker():
    """Charger le cross-encoder une seule fois par processus."""
    return CrossEncoder(RERANK_MODEL, device="cpu")


def rerank(question, passages, top_k=None):
    """Reclasser des passages par pertinence (question, passage).

    Conserve les passages tels quels (métadonnées comprises) et ajoute un
    champ rerank_score. Renvoie les top_k premiers si top_k est fourni.
    """
    if not passages:
        return []

    model = get_reranker()
    pairs = [(question, passage["page_content"]) for passage in passages]
    scores = model.predict(pairs)

    ranked = sorted(
        zip(passages, scores),
        key=lambda couple: couple[1],
        reverse=True,
    )

    results = []
    for passage, score in ranked:
        enriched = dict(passage)
        enriched["rerank_score"] = float(score)
        results.append(enriched)

    return results[:top_k] if top_k else results


def search_documents_reranked(question, limit=3, candidate_limit=DEFAULT_CANDIDATES):
    """Recherche dense élargie, puis reranking, puis top-limit."""
    candidates = search_documents(question, limit=candidate_limit)
    return rerank(question, candidates, top_k=limit)


def main():
    """Comparer rapidement dense et reranké sur une question."""
    import argparse

    parser = argparse.ArgumentParser(description="Tester le reranking FixIT.")
    parser.add_argument("question")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--candidates", type=int, default=DEFAULT_CANDIDATES)
    args = parser.parse_args()

    dense = search_documents(args.question, limit=args.limit)
    reranked = search_documents_reranked(
        args.question, limit=args.limit, candidate_limit=args.candidates
    )

    print(f"\nQuestion : {args.question}")
    print("\n--- DENSE (top {}) ---".format(args.limit))
    for rank, passage in enumerate(dense, start=1):
        meta = passage["metadata"]
        print(f"{rank}. {meta.get('doc_id')} p.{meta.get('page')} "
              f"(score {passage['score']:.4f})")

    print("\n--- RERANKÉ (top {} sur {} candidats) ---".format(
        args.limit, args.candidates))
    for rank, passage in enumerate(reranked, start=1):
        meta = passage["metadata"]
        print(f"{rank}. {meta.get('doc_id')} p.{meta.get('page')} "
              f"(rerank {passage['rerank_score']:.4f})")


if __name__ == "__main__":
    main()
