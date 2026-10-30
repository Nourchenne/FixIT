import argparse
import json
from pathlib import Path

from qdrant_client import QdrantClient

from documents.services.embeddings import embed_query
from documents.services.indexing import EMBEDDING_CONFIG


BASE_DIR = Path(__file__).resolve().parents[2]
INDEX_INFO_FILE = BASE_DIR / "data" / "processed" / "vector_index.json"


def load_index_info():
    """Lire la configuration de l'index terminé."""
    if not INDEX_INFO_FILE.is_file():
        raise FileNotFoundError(
            "Configuration de l'index introuvable. "
            "Exécute d'abord documents.services.indexing."
        )

    with INDEX_INFO_FILE.open(encoding="utf-8") as file:
        information = json.load(file)

    # Vérifier que la recherche utilise le même encodage que l'index.
    if information["embedding_config"] != EMBEDDING_CONFIG:
        raise ValueError(
            "La configuration des embeddings a changé. "
            "Il faut réindexer les documents avant la recherche."
        )

    return information


def search_documents(question, limit=3):
    """Rechercher les passages les plus proches d'une question."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("La question ne doit pas être vide.")

    if limit < 1:
        raise ValueError("Le nombre de résultats doit être positif.")

    information = load_index_info()
    collection_name = information["collection_name"]
    qdrant_path = BASE_DIR / information["qdrant_path"]

    if not qdrant_path.is_dir():
        raise FileNotFoundError(
            f"Base Qdrant introuvable : {qdrant_path}"
        )

    client = QdrantClient(path=str(qdrant_path))

    try:
        if not client.collection_exists(collection_name):
            raise ValueError(
                f"Collection introuvable : {collection_name}"
            )

        # embed_query ajoute le préfixe "query: " et normalise le vecteur.
        question_vector = embed_query(question)

        if len(question_vector) != information["embedding_config"]["dimension"]:
            raise ValueError(
                "La dimension du vecteur ne correspond pas à celle de l'index."
            )

        response = client.query_points(
            collection_name=collection_name,
            query=question_vector.tolist(),
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        results = []

        for point in response.points:
            payload = point.payload or {}

            results.append({
                "score": float(point.score),
                "page_content": payload.get("page_content", ""),
                "metadata": payload.get("metadata", {}),
            })

        return results

    finally:
        client.close()


def main():
    """Tester la recherche depuis le terminal."""
    parser = argparse.ArgumentParser(
        description="Rechercher des passages dans la base FixIT."
    )
    parser.add_argument(
        "question",
        help="La question à rechercher, entre guillemets.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Nombre de passages à afficher. Par défaut : 3.",
    )
    args = parser.parse_args()

    results = search_documents(args.question, limit=args.limit)

    print(f"\nQuestion : {args.question}")
    print(f"Passages retrouvés : {len(results)}")

    for rank, result in enumerate(results, start=1):
        metadata = result["metadata"]

        print("\n" + "=" * 60)
        print(f"Résultat {rank}")
        print(f"Score de similarité : {result['score']:.4f}")
        print(f"Document : {metadata.get('doc_id', '')}")
        print(f"Titre : {metadata.get('titre', '')}")
        print(f"Fichier : {metadata.get('fichier', '')}")
        print(f"Page : {metadata.get('page', '')}")
        print(f"Source : {metadata.get('source_url', '')}")
        print("\nPASSAGE :")
        print(result["page_content"])


if __name__ == "__main__":
    main()