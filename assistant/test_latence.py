import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from assistant.apps import doit_precharger
from assistant.services import retrieval
from documents.services import embeddings


class Vecteur(list):
    def tolist(self):
        return list(self)


INFO = {"collection_name": "fixit_test",
        "embedding_config": {"dimension": 3}}


class PrechargementTests(unittest.TestCase):
    def test_decision(self):
        cas = [
            (["manage.py", "runserver"], {"RUN_MAIN": "true"}, True),
            (["manage.py", "runserver"], {}, False),          # processus de surveillance
            (["manage.py", "runserver", "--noreload"], {}, True),
            (["manage.py", "migrate"], {"RUN_MAIN": "true"}, False),
            (["manage.py", "test"], {}, False),
            (["manage.py", "runserver"], {"RUN_MAIN": "true",
                                          "FIXIT_PRECHARGEMENT": "0"}, False),
        ]
        for argv, env, attendu in cas:
            with self.subTest(argv=argv, env=env):
                self.assertIs(doit_precharger(argv, env), attendu)


class RechercheTests(unittest.TestCase):
    def setUp(self):
        retrieval.get_client.cache_clear()
        self.addCleanup(retrieval.get_client.cache_clear)
        patches = [
            patch.object(retrieval, "load_index_info", return_value=INFO),
            patch.object(retrieval, "embed_query", return_value=Vecteur([0.1, 0.2, 0.3])),
            patch.object(retrieval, "QdrantClient"),
        ]
        mocks = [p.start() for p in patches]
        for p in patches:
            self.addCleanup(p.stop)
        self.client_cls = mocks[2]
        client = self.client_cls.return_value
        client.collection_exists.return_value = True
        point = SimpleNamespace(score=0.88, payload={
            "page_content": "Active le Wi-Fi.",
            "metadata": {"doc_id": "DOC001", "page": 8}})
        client.query_points.return_value = SimpleNamespace(points=[point])

    def test_client_reutilise_entre_questions(self):
        retrieval.search_documents("Mon PC ne trouve aucun réseau.")
        retrieval.search_documents("Le son ne marche plus.")
        self.client_cls.assert_called_once()
        self.client_cls.return_value.close.assert_not_called()

    def test_format_des_resultats(self):
        r = retrieval.search_documents("Wi-Fi absent", limit=1)
        self.assertEqual(r, [{"score": 0.88, "page_content": "Active le Wi-Fi.",
                              "metadata": {"doc_id": "DOC001", "page": 8}}])

    def test_collection_absente(self):
        self.client_cls.return_value.collection_exists.return_value = False
        with self.assertRaises(ValueError):
            retrieval.search_documents("Wi-Fi absent")

    def test_question_vide(self):
        with self.assertRaises(ValueError):
            retrieval.search_documents("   ")


class ModeleTests(unittest.TestCase):
    def test_un_seul_chargement_meme_en_parallele(self):
        compteur = MagicMock()

        def chargement_lent(*args, **kwargs):
            compteur()
            time.sleep(0.05)
            return object()

        embeddings._charger_modele.cache_clear()
        self.addCleanup(embeddings._charger_modele.cache_clear)
        with patch.object(embeddings, "SentenceTransformer", side_effect=chargement_lent):
            fils = [threading.Thread(target=embeddings.get_model) for _ in range(5)]
            for f in fils:
                f.start()
            for f in fils:
                f.join()
        self.assertEqual(compteur.call_count, 1)
