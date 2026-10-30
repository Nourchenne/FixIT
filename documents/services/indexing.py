import hashlib
import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient, models

from documents.services.embeddings import (
    MODEL_NAME,
    embed_documents,
)


BASE_DIR = Path(__file__).resolve().parents[2]

CHUNKS_FILE = BASE_DIR / "data" / "processed" / "chunks.jsonl"
QDRANT_PATH = BASE_DIR / "data" / "vectorstore" / "qdrant"
INDEX_INFO_FILE = BASE_DIR / "data" / "processed" / "vector_index.json"

VECTOR_SIZE = 384
BATCH_SIZE = 16

# À modifier si la manière de calculer les embeddings change.
EMBEDDING_CONFIG = {
    "model": MODEL_NAME,
    "dimension": VECTOR_SIZE,
    "document_prefix": "passage: ",
    "normalize_embeddings": True,
    "distance": "Cosine",
}


def load_chunks():
    """Lire les chunks et vérifier leur structure."""
    if not CHUNKS_FILE.is_file():
        raise FileNotFoundError(
            f"Fichier introuvable : {CHUNKS_FILE}"
        )

    file_content = CHUNKS_FILE.read_bytes()
    chunks = []
    seen_ids = set()

    for line_number, line in enumerate(
        file_content.decode("utf-8-sig").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue

        chunk = json.loads(line)
        content = chunk.get("page_content")
        metadata = chunk.get("metadata")

        if not isinstance(content, str) or not content.strip():
            raise ValueError(
                f"Texte absent ou vide à la ligne {line_number}."
            )

        if not isinstance(metadata, dict):
            raise ValueError(
                f"Métadonnées invalides à la ligne {line_number}."
            )

        required_fields = {
            "chunk_id",
            "doc_id",
            "fichier",
            "page",
            "source_url",
        }

        if not required_fields.issubset(metadata):
            raise ValueError(
                f"Métadonnées manquantes à la ligne {line_number}."
            )

        chunk_id = metadata["chunk_id"]

        if not isinstance(chunk_id, str) or not chunk_id:
            raise ValueError(
                f"Identifiant invalide à la ligne {line_number}."
            )

        if chunk_id in seen_ids:
            raise ValueError(
                f"Identifiant de chunk en double : {chunk_id}"
            )

        seen_ids.add(chunk_id)
        chunks.append(chunk)

    if not chunks:
        raise ValueError("Le fichier de chunks est vide.")

    return chunks, file_content


def get_collection_name(file_content):
    """Identifier une version du corpus et de son encodage."""
    configuration = json.dumps(
        EMBEDDING_CONFIG,
        sort_keys=True,
    ).encode("utf-8")

    fingerprint = hashlib.sha256(
        configuration + b"\n" + file_content
    ).hexdigest()[:16]

    return f"fixit_{fingerprint}"


def save_index_info(collection_name, count):
    """Enregistrer les informations nécessaires à la recherche."""
    information = {
        "collection_name": collection_name,
        "qdrant_path": QDRANT_PATH.relative_to(BASE_DIR).as_posix(),
        "chunks_file": CHUNKS_FILE.relative_to(BASE_DIR).as_posix(),
        "chunk_count": count,
        "embedding_config": EMBEDDING_CONFIG,
    }

    INDEX_INFO_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = INDEX_INFO_FILE.with_suffix(".json.tmp")

    try:
        temporary_file.write_text(
            json.dumps(information, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary_file.replace(INDEX_INFO_FILE)
    finally:
        if temporary_file.exists():
            temporary_file.unlink()


def main():
    chunks, file_content = load_chunks()
    collection_name = get_collection_name(file_content)

    QDRANT_PATH.mkdir(parents=True, exist_ok=True)

    # Ouvrir une base Qdrant persistante sur le disque.
    client = QdrantClient(path=str(QDRANT_PATH))

    try:
        # Créer la collection uniquement si elle n'existe pas.
        if not client.collection_exists(collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=VECTOR_SIZE,
                    distance=models.Distance.COSINE,
                ),
            )

        for start in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[start:start + BATCH_SIZE]

            texts = [
                chunk["page_content"]
                for chunk in batch
            ]

            # Notre fonction ajoute "passage: " aux textes,
            # vérifie leur longueur et normalise les vecteurs.
            vectors = embed_documents(texts)

            if vectors.shape != (len(batch), VECTOR_SIZE):
                raise ValueError(
                    f"Dimensions inattendues : {vectors.shape}"
                )

            points = []

            for chunk, vector in zip(batch, vectors):
                # Qdrant accepte notamment les UUID comme identifiants.
                # Le même chunk produit toujours le même UUID.
                point_id = str(
                    uuid5(
                        NAMESPACE_URL,
                        chunk["metadata"]["chunk_id"],
                    )
                )

                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=vector.tolist(),
                        payload={
                            "page_content": chunk["page_content"],
                            "metadata": chunk["metadata"],
                        },
                    )
                )

            # Ajouter les points ou remplacer ceux de même identifiant.
            client.upsert(
                collection_name=collection_name,
                points=points,
                wait=True,
            )

            processed = start + len(batch)
            print(f"Progression : {processed}/{len(chunks)} chunks")

        stored_count = client.count(
            collection_name=collection_name,
            exact=True,
        ).count

        if stored_count != len(chunks):
            raise RuntimeError(
                f"Nombre inattendu de points : {stored_count}, "
                f"attendu : {len(chunks)}"
            )

        # Publier la configuration seulement après l'indexation complète.
        save_index_info(collection_name, stored_count)

        print("\n--- BILAN INDEXATION ---")
        print(f"Chunks enregistrés : {stored_count}")
        print(f"Dimension des vecteurs : {VECTOR_SIZE}")
        print(f"Collection : {collection_name}")
        print(f"Base locale : {QDRANT_PATH}")
        print(f"Configuration : {INDEX_INFO_FILE}")

    finally:
        # Libérer la base, même si une erreur survient.
        client.close()


if __name__ == "__main__":
    main()