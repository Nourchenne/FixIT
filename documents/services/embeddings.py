from functools import lru_cache

from sentence_transformers import SentenceTransformer


MODEL_NAME = "intfloat/multilingual-e5-small"


@lru_cache(maxsize=1)
def get_model():
    """Charger le modèle une seule fois par processus Python."""
    return SentenceTransformer(
        MODEL_NAME,
        device="cpu",
    )


def encode_texts(texts, prefix):
    """Transformer les textes en vecteurs sans troncature silencieuse."""
    if not texts:
        raise ValueError("La liste des textes est vide.")

    if any(not isinstance(text, str) or not text.strip() for text in texts):
        raise ValueError("Chaque texte doit être une chaîne non vide.")

    model = get_model()

    prepared_texts = [
        prefix + text.strip()
        for text in texts
    ]

    # Vérifier que chaque texte tient dans la limite du modèle.
    for index, text in enumerate(prepared_texts, start=1):
        token_ids = model.tokenizer(
            text,
            truncation=False,
            add_special_tokens=True,
        )["input_ids"]

        if len(token_ids) > model.max_seq_length:
            raise ValueError(
                f"Texte numéro {index} trop long : "
                f"{len(token_ids)} tokens pour une limite "
                f"de {model.max_seq_length}. "
                "Il faut réduire ce chunk avant son encodage."
            )

    return model.encode(
        prepared_texts,
        batch_size=16,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=len(prepared_texts) > 1,
    )


def embed_documents(texts):
    """Créer les embeddings des passages documentaires."""
    return encode_texts(texts, prefix="passage: ")


def embed_query(question):
    """Créer l'embedding d'une question."""
    return encode_texts([question], prefix="query: ")[0]


def main():
    """Tester le modèle sur un passage et une question."""
    passage = (
        "Si aucun réseau Wi-Fi n'apparaît, vérifier que "
        "la carte réseau sans fil est activée."
    )
    question = "Mon ordinateur ne trouve aucun réseau Wi-Fi."

    document_vectors = embed_documents([passage])
    question_vector = embed_query(question)

    print("\n--- TEST EMBEDDINGS ---")
    print(f"Modèle : {MODEL_NAME}")
    print(f"Dimension du passage : {len(document_vectors[0])}")
    print(f"Dimension de la question : {len(question_vector)}")
    print("Embeddings calculés avec succès.")


if __name__ == "__main__":
    main()