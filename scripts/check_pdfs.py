from pathlib import Path

from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parents[1]
PDF_DIR = BASE_DIR / "data" / "raw"

#vérifier que nos documents sont lisibles par Python avant de passer au découpage
# Seuil indicatif : une page courte doit être examinée,
# mais elle n'est pas forcément incorrecte.
MIN_CHARACTERS = 80


def main():
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"Aucun PDF trouvé dans : {PDF_DIR}")
        return

    total_pages = 0
    documents_to_review = 0
    errors = 0

    for pdf_path in pdf_files:
        try:
            with pdf_path.open("rb") as pdf_file:
                reader = PdfReader(pdf_file)
                page_count = len(reader.pages)
                total_characters = 0
                short_pages = []

                for page_number, page in enumerate(reader.pages, start=1):
                    text = page.extract_text() or ""
                    character_count = len("".join(text.split()))
                    total_characters += character_count

                    if character_count < MIN_CHARACTERS:
                        short_pages.append(page_number)

            total_pages += page_count

            print(
                f"\n{pdf_path.name} | "
                f"{page_count} pages | "
                f"{total_characters} caractères hors espaces"
            )

            if page_count == 0 or short_pages:
                documents_to_review += 1
                print(f"  À examiner : pages peu textuelles {short_pages}")
            else:
                print("  Texte détecté sur toutes les pages.")

        except Exception as error:
            errors += 1
            print(f"\nERREUR : {pdf_path.name}")
            print(f"  {type(error).__name__} : {error}")

    print("\n--- BILAN ---")
    print(f"PDF examinés : {len(pdf_files)}")
    print(f"Pages des PDF lus sans erreur : {total_pages}")
    print(f"Documents avec pages à examiner : {documents_to_review}")
    print(f"Documents en erreur : {errors}")


if __name__ == "__main__":
    main()