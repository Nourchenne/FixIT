"""Recherche BM25 seule et recherche hybride (dense + BM25).

Même principe que RetrievalMode.HYBRID du lab 15bis : Qdrant récupère des
candidats avec chaque méthode, puis fusionne les deux classements par
Reciprocal Rank Fusion (RRF). Un passage bien classé par les deux méthodes
remonte en tête.

Utilisé par le benchmark (evaluation.evaluate_retrieval --mode). Le chat
continue d'utiliser la recherche dense (assistant.services.retrieval).

    python -m assistant.services.recherche_hybride "Erreur 0x80070005 Windows Update"
"""

import argparse
import json
from functools import lru_cache
from pathlib import Path

from qdrant_client import models

from assistant.services.retrieval import get_client
from documents.services import bm25
from documents.services.embeddings import embed_query
from documents.services.indexing_hybride import CREUX, DENSE, HYBRID_INFO_FILE

CANDIDATS = 20


@lru_cache(maxsize=1)
def collection_hybride():
    if not Path(HYBRID_INFO_FILE).is_file():
        raise FileNotFoundError(
            "Collection hybride introuvable. "
            "Lance d'abord python -m documents.services.indexing_hybride."
        )
    info = json.loads(Path(HYBRID_INFO_FILE).read_text(encoding="utf-8"))
    return info["collection_name"]


def _verifier(question, limit):
    if not isinstance(question, str) or not question.strip():
        raise ValueError("La question ne doit pas être vide.")
    if limit < 1:
        raise ValueError("Le nombre de résultats doit être positif.")


def _passages(reponse):
    return [{
        "score": float(p.score),
        "page_content": (p.payload or {}).get("page_content", ""),
        "metadata": (p.payload or {}).get("metadata", {}),
    } for p in reponse.points]


def _requete_bm25(question):
    indices, poids = bm25.vecteur_question(question)
    return models.SparseVector(indices=indices, values=poids)


def search_bm25(question, limit=3):
    """Recherche par mots-clés seule."""
    _verifier(question, limit)
    requete = _requete_bm25(question)
    if not requete.indices:          # question sans mot utile
        return []
    reponse = get_client().query_points(
        collection_name=collection_hybride(), query=requete, using=CREUX,
        limit=limit, with_payload=True,
    )
    return _passages(reponse)


def search_hybride(question, limit=3, candidats=CANDIDATS):
    """Dense + BM25, fusionnés par RRF."""
    _verifier(question, limit)
    candidats = max(candidats, limit)
    prefetch = [models.Prefetch(query=embed_query(question).tolist(),
                                using=DENSE, limit=candidats)]
    requete = _requete_bm25(question)
    if requete.indices:
        prefetch.append(models.Prefetch(query=requete, using=CREUX, limit=candidats))
    reponse = get_client().query_points(
        collection_name=collection_hybride(), prefetch=prefetch,
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=limit, with_payload=True,
    )
    return _passages(reponse)


def main():
    parser = argparse.ArgumentParser(description="Comparer BM25 et hybride.")
    parser.add_argument("question")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    for nom, fonction in (("BM25", search_bm25), ("HYBRIDE", search_hybride)):
        print(f"\n--- {nom} ---")
        for rang, p in enumerate(fonction(args.question, args.limit), start=1):
            meta = p["metadata"]
            print(f"{rang}. {meta.get('doc_id')} p.{meta.get('page')} "
                  f"(score {p['score']:.4f}) {meta.get('titre', '')}")


if __name__ == "__main__":
    main()
