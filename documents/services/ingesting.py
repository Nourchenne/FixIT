#transformer les pdf en chunks
import csv
import hashlib
import json
import re
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


# Racine du projet FixIT.
BASE_DIR = Path(__file__).resolve().parents[2]

PDF_DIR = BASE_DIR / "data" / "raw"
SOURCES_FILE = BASE_DIR / "data" / "sources.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "chunks.jsonl"

# Tailles mesurées en caractères.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# Corrections ciblées, observées dans les textes extraits.
TEXT_CORRECTIONS = {
    "quevous": "que vous",
    "parexécuter": "par exécuter",
    "résoudrela": "résoudre la",
    "administrateursur": "administrateur sur",
    "s’affichelorsque": "s’affiche lorsque",
    "s'affichelorsque": "s'affiche lorsque",
}


def load_sources():
    """Lire le registre et vérifier les références aux PDF."""
    if not SOURCES_FILE.is_file():
        raise FileNotFoundError(
            f"Registre introuvable : {SOURCES_FILE}"
        )

    if not PDF_DIR.is_dir():
        raise FileNotFoundError(
            f"Dossier PDF introuvable : {PDF_DIR}"
        )

    required_columns = {
        "doc_id",
        "fichier",
        "titre",
        "url_source",
    }

    sources = []
    seen_ids = set()
    seen_files = set()

    with SOURCES_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []

        missing_columns = required_columns - set(fieldnames)

        if missing_columns:
            raise ValueError(
                "Colonnes manquantes dans sources.csv : "
                + ", ".join(sorted(missing_columns))
            )

        if len(fieldnames) != len(set(fieldnames)):
            raise ValueError(
                "Des noms de colonnes sont en double dans sources.csv."
            )

        for line_number, row in enumerate(reader, start=2):
            # DictReader utilise None si une ligne est mal structurée.
            if None in row or any(
                value is None for value in row.values()
            ):
                raise ValueError(
                    f"Ligne CSV mal structurée : {line_number}"
                )

            source = {
                key: value.strip()
                for key, value in row.items()
            }

            # Ignorer les lignes entièrement vides.
            if not any(source.values()):
                continue

            empty_fields = [
                key
                for key in required_columns
                if not source[key]
            ]

            if empty_fields:
                raise ValueError(
                    f"Ligne {line_number}, champs vides : "
                    + ", ".join(sorted(empty_fields))
                )

            doc_id = source["doc_id"]
            filename = source["fichier"]

            # Un nom de fichier est attendu, pas un chemin.
            if (
                "/" in filename
                or "\\" in filename
                or ":" in filename
                or not filename.lower().endswith(".pdf")
            ):
                raise ValueError(
                    f"Nom de PDF non valide : {filename}"
                )

            filename_key = filename.casefold()

            if doc_id in seen_ids:
                raise ValueError(
                    f"Identifiant en double : {doc_id}"
                )

            if filename_key in seen_files:
                raise ValueError(
                    f"Fichier référencé plusieurs fois : {filename}"
                )

            if not (PDF_DIR / filename).is_file():
                raise FileNotFoundError(
                    f"PDF manquant : {filename}"
                )

            seen_ids.add(doc_id)
            seen_files.add(filename_key)
            sources.append(source)

    if not sources:
        raise ValueError(
            "sources.csv ne contient aucun document."
        )

    return sources


def clean_text(text, page_number):
    """Nettoyer le texte sans réécrire les procédures."""
    # Normaliser certains caractères d'espacement.
    text = text.replace("\u00a0", " ")
    text = text.replace("\u202f", " ")
    text = text.replace("\u00ad", "")

    lines = [
        line.strip()
        for line in text.splitlines()
    ]

    # Retirer les lignes vides au début.
    while lines and not lines[0]:
        lines.pop(0)

    # Dans certaines copies, le numéro de page est extrait en premier.
    if lines and lines[0] == str(page_number):
        lines.pop(0)

    # Retirer la présentation initiale des copies préparées pour FixIT.
    # Ne rien retirer si aucun marqueur connu n'est trouvé.
    if page_number == 1:
        for index, line in enumerate(lines[:15]):
            if line.startswith((
                "Copie textuelle nettoyée",
                "Synthèse FixIT",
            )):
                lines = lines[index + 1:]
                break

    text = "\n".join(lines)

    # Réduire les espaces multiples sans supprimer les paragraphes.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Corriger uniquement les erreurs identifiées.
    for incorrect, correct in TEXT_CORRECTIONS.items():
        text = text.replace(incorrect, correct)

    return text.strip()


def create_chunks(sources):
    """Extraire et découper chaque page avec ses métadonnées."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
        keep_separator=True,
        is_separator_regex=False,
    )

    chunks = []
    total_pages = 0

    for source in sources:
        pdf_path = PDF_DIR / source["fichier"]
        document_chunk_count = 0

        with pdf_path.open("rb") as pdf_file:
            reader = PdfReader(pdf_file)

            if len(reader.pages) == 0:
                raise ValueError(
                    f"PDF sans pages : {pdf_path.name}"
                )

            for page_number, page in enumerate(
                reader.pages, start=1
            ):
                raw_text = page.extract_text() or ""
                text = clean_text(raw_text, page_number)

                if not text:
                    raise ValueError(
                        f"Texte vide après nettoyage : "
                        f"{pdf_path.name}, page {page_number}"
                    )

                page_chunks = splitter.split_text(text)

                if not page_chunks:
                    raise ValueError(
                        f"Aucun chunk créé : "
                        f"{pdf_path.name}, page {page_number}"
                    )

                for chunk_number, content in enumerate(
                    page_chunks, start=1
                ):
                    # Identifiant reproductible pour le même contenu,
                    # au même emplacement dans le document.
                    identifier = (
                        f"{source['doc_id']}|"
                        f"{page_number}|"
                        f"{chunk_number}|"
                        f"{content}"
                    )

                    chunk_id = hashlib.sha256(
                        identifier.encode("utf-8")
                    ).hexdigest()

                    metadata = {
                        **source,
                        "page": page_number,
                        "chunk_in_page": chunk_number,
                        "chunk_id": chunk_id,
                        "source_url": source["url_source"],
                    }

                    chunks.append({
                        "page_content": content,
                        "metadata": metadata,
                    })

                    document_chunk_count += 1

                total_pages += 1

        print(
            f"{pdf_path.name} : "
            f"{document_chunk_count} chunks"
        )

    return chunks, total_pages


def save_chunks(chunks):
    """Enregistrer les chunks, un objet JSON par ligne."""
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_file = OUTPUT_FILE.with_suffix(".jsonl.tmp")

    try:
        with temporary_file.open(
            "w",
            encoding="utf-8",
            newline="\n",
        ) as file:
            for chunk in chunks:
                file.write(
                    json.dumps(chunk, ensure_ascii=False)
                    + "\n"
                )

        # Remplacer l'ancien fichier après l'écriture complète.
        temporary_file.replace(OUTPUT_FILE)

    finally:
        # Nettoyer un éventuel fichier temporaire en cas d'erreur.
        if temporary_file.exists():
            temporary_file.unlink()


def main():
    """Exécuter la préparation des chunks et afficher le bilan."""
    sources = load_sources()
    chunks, total_pages = create_chunks(sources)

    if not chunks:
        raise ValueError("Aucun chunk créé.")

    save_chunks(chunks)

    print("\n--- BILAN ---")
    print(f"Documents traités : {len(sources)}")
    print(f"Pages traitées : {total_pages}")
    print(f"Chunks créés : {len(chunks)}")
    print(f"Fichier généré : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()