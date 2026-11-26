"""Importe data/sources.csv dans le modèle Document.

Règles :
- doc_id absent de la base -> créé (revision=1, à indexer).
- doc_id présent mais PDF inchangé (même empreinte) -> métadonnées mises à
  jour si besoin, revision et etat_indexation non touchés.
- doc_id présent et PDF modifié (empreinte différente) -> nouvelle révision
  (revision + 1) et etat_indexation repassé à "à indexer", pour signaler
  qu'il faut relancer l'indexation sur ce document.

La détection de doublons entre documents (deux doc_id différents pour un
même contenu) est hors périmètre : chaque doc_id est traité indépendamment.
"""
from datetime import date

from django.core.management.base import BaseCommand, CommandError

from documents.models import Document
from documents.services.ingesting import PDF_DIR, load_sources
from documents.services.metadata_extractor import hash_fichier

# Colonnes de sources.csv copiées telles quelles sur le Document.
CHAMPS_TEXTE = (
    "titre",
    "fichier",
    "url_source",
    "source",
    "type_doc",
    "categorie",
    "systeme",
    "marque",
    "modele",
    "version_connue",
    "cas_couverts",
)


class Command(BaseCommand):
    help = "Importe data/sources.csv dans la base (création, mise à jour, nouvelle révision si le PDF a changé)."

    def handle(self, *args, **options):
        try:
            sources = load_sources()
        except (FileNotFoundError, ValueError) as erreur:
            raise CommandError(str(erreur)) from erreur

        crees = revises = mis_a_jour = inchanges = 0

        for source in sources:
            empreinte = hash_fichier(PDF_DIR / source["fichier"])
            champs = {cle: source.get(cle, "") for cle in CHAMPS_TEXTE}
            texte_date = source.get("date_collecte") or ""
            champs["date_collecte"] = date.fromisoformat(texte_date) if texte_date else None

            document = Document.objects.filter(doc_id=source["doc_id"]).first()

            if document is None:
                Document.objects.create(
                    doc_id=source["doc_id"],
                    contenu_hash=empreinte,
                    revision=1,
                    etat_indexation=Document.Indexation.A_INDEXER,
                    **champs,
                )
                crees += 1
                continue

            if document.contenu_hash != empreinte:
                for cle, valeur in champs.items():
                    setattr(document, cle, valeur)
                document.contenu_hash = empreinte
                document.revision += 1
                document.etat_indexation = Document.Indexation.A_INDEXER
                document.save()
                revises += 1
                continue

            a_change = False
            for cle, valeur in champs.items():
                if getattr(document, cle) != valeur:
                    setattr(document, cle, valeur)
                    a_change = True
            if a_change:
                document.save()
                mis_a_jour += 1
            else:
                inchanges += 1

        self.stdout.write(self.style.SUCCESS(
            f"{crees} créé(s), {revises} nouvelle(s) révision(s), "
            f"{mis_a_jour} mis à jour, {inchanges} inchangé(s)."
        ))
