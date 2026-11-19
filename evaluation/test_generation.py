import csv
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from evaluation import evaluate_generation as ev

REPONDABLE = {"query_id": "F001", "lang": "fr", "cas": "NET01", "answerable": True,
              "question": "Aucun réseau Wi-Fi.", "gold_doc_ids": ["DOC001", "DOC003"]}
HORS = {"query_id": "F041", "lang": "fr", "cas": "HORS", "answerable": False,
        "question": "Capitale du Canada ?", "gold_doc_ids": []}


def reponse(type_="etapes", langue="fr", docs=("DOC001",)):
    return {"answer": "1. Active le Wi-Fi. [S1]", "langue": langue, "type": type_,
            "sources": [{"doc_id": d} for d in docs], "ticket_suggere": False}


class GenerationTests(TestCase):
    def test_question_repondable(self):
        ligne = ev.evaluer_question(REPONDABLE, lambda q: reponse())
        self.assertEqual((ligne["langue_ok"], ligne["guide_attendu_cite"], ligne["repli_correct"]),
                         ("oui", "oui", "sans objet"))

    def test_mauvais_guide_et_mauvaise_langue(self):
        ligne = ev.evaluer_question(REPONDABLE, lambda q: reponse(langue="en", docs=("DOC028",)))
        self.assertEqual((ligne["langue_ok"], ligne["guide_attendu_cite"]), ("non", "non"))

    def test_hors_corpus(self):
        bon = ev.evaluer_question(HORS, lambda q: reponse("repli", docs=()))
        mauvais = ev.evaluer_question(HORS, lambda q: reponse())
        self.assertEqual((bon["repli_correct"], mauvais["repli_correct"]), ("oui", "non"))

    @patch.object(ev.time, "sleep")
    def test_nouvel_essai_si_limite_groq(self, _sleep):
        class RateLimitError(Exception):
            pass
        appels = iter([RateLimitError("429"), reponse()])

        def repondre(question):
            valeur = next(appels)
            if isinstance(valeur, Exception):
                raise valeur
            return valeur

        self.assertEqual(ev.evaluer_question(REPONDABLE, repondre)["type"], "etapes")

    def test_erreur_consignee_et_synthese(self):
        def panne(question):
            raise RuntimeError("Qdrant arrêté")
        lignes = [ev.evaluer_question(REPONDABLE, panne),
                  ev.evaluer_question(REPONDABLE, lambda q: reponse()),
                  ev.evaluer_question(HORS, lambda q: reponse("repli", docs=()))]
        self.assertIn("Qdrant arrêté", lignes[0]["reponse"])
        resume = ev.synthese(lignes)
        self.assertEqual((resume["erreurs"], resume["hors_corpus_repli_correct_pct"]), (1, 100.0))

    def test_csv_lisible_par_excel(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "grille.csv"
            ev.ecrire_csv([ev.evaluer_question(REPONDABLE, lambda q: reponse())], chemin)
            self.assertTrue(chemin.read_bytes().startswith(b"\xef\xbb\xbf"))
            with chemin.open(encoding="utf-8-sig") as fichier:
                lignes = list(csv.DictReader(fichier, delimiter=";"))
            self.assertEqual(lignes[0]["query_id"], "F001")
            self.assertEqual(lignes[0]["note_0_1_2"], "")
