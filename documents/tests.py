import csv

from django.core.management import call_command
from django.test import TestCase

from documents.models import Document
from documents.services.ingesting import SOURCES_FILE


def nombre_de_sources():
    with SOURCES_FILE.open("r", encoding="utf-8-sig", newline="") as fichier:
        return sum(1 for _ in csv.DictReader(fichier))


class ImporterSourcesTests(TestCase):
    """Commande d'import de data/sources.csv (gestion documentaire, R04)."""

    def test_premier_import_cree_tous_les_documents(self):
        call_command("importer_sources")

        self.assertEqual(Document.objects.count(), nombre_de_sources())
        doc001 = Document.objects.get(doc_id="DOC001")
        self.assertEqual(doc001.revision, 1)
        self.assertEqual(doc001.etat_indexation, Document.Indexation.A_INDEXER)
        self.assertTrue(doc001.contenu_hash)

    def test_reimport_sans_changement_ne_cree_rien_de_plus(self):
        call_command("importer_sources")
        total_apres_premier_import = Document.objects.count()

        call_command("importer_sources")

        self.assertEqual(Document.objects.count(), total_apres_premier_import)
        doc001 = Document.objects.get(doc_id="DOC001")
        self.assertEqual(doc001.revision, 1)

    def test_pdf_modifie_incremente_la_revision(self):
        call_command("importer_sources")
        doc001 = Document.objects.get(doc_id="DOC001")
        empreinte_initiale = doc001.contenu_hash

        # On simule un nouveau PDF pour ce document (empreinte différente),
        # sans toucher au vrai fichier sur le disque.
        doc001.contenu_hash = "empreinte-de-test-perimee"
        doc001.save()

        call_command("importer_sources")
        doc001.refresh_from_db()

        self.assertEqual(doc001.revision, 2)
        self.assertEqual(doc001.etat_indexation, Document.Indexation.A_INDEXER)
        self.assertEqual(doc001.contenu_hash, empreinte_initiale)

    def test_metadonnee_modifiee_sans_changement_pdf_ne_touche_pas_la_revision(self):
        call_command("importer_sources")
        doc001 = Document.objects.get(doc_id="DOC001")
        doc001.titre = "Titre modifié à la main"
        doc001.save()

        call_command("importer_sources")
        doc001.refresh_from_db()

        # Le PDF n'a pas changé : le titre du CSV est restauré, pas de
        # nouvelle révision.
        self.assertNotEqual(doc001.titre, "Titre modifié à la main")
        self.assertEqual(doc001.revision, 1)
