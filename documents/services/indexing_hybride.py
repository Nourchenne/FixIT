"""Construire la collection hybride (dense + BM25) pour le benchmark.

La collection dense utilisée par le chat n'est pas modifiée. On crée une
seconde collection, `<collection dense>_hybride`, qui contient pour chaque
passage :
- le vecteur dense, recopié tel quel depuis la collection dense (aucun calcul
  d'embedding, donc exactement les mêmes vecteurs) ;
- un vecteur creux BM25 (documents/services/bm25.py), avec l'IDF appliqué
  par Qdrant.

Lancer depuis la racine du dépôt, Qdrant démarré, après
documents.services.indexing :

    python -m documents.services.indexing_hybride
"""

import json
from pathlib import Path

from qdrant_client import QdrantClient, models

from config.qdrant import QDRANT_URL
from documents.services import bm25

BASE_DIR = Path(__file__).resolve().parents[2]
INDEX_INFO_FILE = BASE_DIR / "data" / "processed" / "vector_index.json"
HYBRID_INFO_FILE = BASE_DIR / "data" / "processed" / "hybrid_index.json"

DENSE = "dense"
CREUX = "bm25"
LOT = 64


def lire_points(client, collection):
    """Tous les points de la collection dense, avec vecteurs et contenu."""
    points, suivant = [], None
    while True:
        lot, suivant = client.scroll(
            collection_name=collection, limit=LOT, offset=suivant,
            with_payload=True, with_vectors=True,
        )
        points.extend(lot)
        if suivant is None:
            return points


def construire(client, collection_dense):
    """Créer (ou recréer) la collection hybride ; renvoie ses informations."""
    if not client.collection_exists(collection_dense):
        raise ValueError(
            f"Collection dense introuvable : {collection_dense}. "
            "Lance d'abord python -m documents.services.indexing."
        )
    points = lire_points(client, collection_dense)
    if not points:
        raise ValueError("La collection dense est vide.")

    textes = [(p.payload or {}).get("page_content", "") for p in points]
    moyenne = bm25.longueur_moyenne(textes)
    taille = len(points[0].vector)

    collection = f"{collection_dense}_hybride"
    if client.collection_exists(collection):
        client.delete_collection(collection)
    client.create_collection(
        collection_name=collection,
        vectors_config={DENSE: models.VectorParams(
            size=taille, distance=models.Distance.COSINE)},
        sparse_vectors_config={CREUX: models.SparseVectorParams(
            modifier=models.Modifier.IDF)},
    )

    for debut in range(0, len(points), LOT):
        nouveaux = []
        for point, texte in zip(points[debut:debut + LOT],
                                textes[debut:debut + LOT]):
            indices, poids = bm25.vecteur_passage(texte, moyenne)
            nouveaux.append(models.PointStruct(
                id=point.id,
                vector={
                    DENSE: point.vector,
                    CREUX: models.SparseVector(indices=indices, values=poids),
                },
                payload=point.payload,
            ))
        client.upsert(collection_name=collection, points=nouveaux, wait=True)

    total = client.count(collection_name=collection, exact=True).count
    if total != len(points):
        raise RuntimeError(f"{total} points enregistrés au lieu de {len(points)}.")

    return {
        "collection_name": collection,
        "collection_dense": collection_dense,
        "point_count": total,
        "bm25": {"k1": bm25.K1, "b": bm25.B, "longueur_moyenne": round(moyenne, 2)},
    }


def main():
    if not INDEX_INFO_FILE.is_file():
        raise FileNotFoundError(
            "Index dense introuvable. Lance d'abord documents.services.indexing."
        )
    collection_dense = json.loads(
        INDEX_INFO_FILE.read_text(encoding="utf-8"))["collection_name"]

    client = QdrantClient(url=QDRANT_URL)
    try:
        info = construire(client, collection_dense)
    finally:
        client.close()

    HYBRID_INFO_FILE.write_text(
        json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n--- BILAN INDEXATION HYBRIDE ---")
    print(f"Collection : {info['collection_name']}")
    print(f"Passages : {info['point_count']}")
    print(f"Longueur moyenne (mots) : {info['bm25']['longueur_moyenne']}")
    print(f"Configuration : {HYBRID_INFO_FILE.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
