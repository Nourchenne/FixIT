import unittest
from unittest.mock import patch

from assistant.services import chat


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.meta = {"doc_id": "DOC001", "titre": "Guide Wi-Fi",
                     "page": 8, "source_url": "https://example.org/wifi"}
        self.passages = [{"page_content": "Active le Wi-Fi.",
                           "metadata": self.meta}]

    def test_citations_fr_et_en(self):
        for lang, text in [("fr", "Active le Wi-Fi."),
                            ("en", "Turn on Wi-Fi.")]:
            step = {"texte": text, "source": 1}
            data = {"langue": lang, "etapes": [step, step]}
            r = chat.formater_reponse(data, self.passages)
            self.assertIn(text + " [S1]", r["answer"])
            self.assertEqual(len(r["sources"]), 1)
            ref = r["sources"][0]
            self.assertEqual((ref["titre"], ref["page"], ref["url"]),
                              ("Guide Wi-Fi", 8, self.meta["source_url"]))

    def test_repli_fr_et_en(self):
        for lang in ("fr", "en"):
            for steps in ([], [{"texte": "Test", "source": 9}]):
                r = chat.formater_reponse(
                    {"langue": lang, "etapes": steps}, self.passages)
                self.assertEqual(r, {"answer": chat.REFUS[lang],
                                      "sources": []})

    def test_langue_invalide(self):
        with self.assertRaises(ValueError):
            chat.formater_reponse({"langue": "xx", "etapes": []}, [])

    def test_question_vide(self):
        with self.assertRaises(ValueError):
            chat.answer_question(" ")

    @patch.dict("os.environ", {"GROQ_API_KEY": "test", "GROQ_MODEL": "test"})
    @patch.object(chat, "ChatGroq")
    @patch.object(chat, "search_documents", return_value=[])
    def test_aucun_extrait_anglais(self, recherche, modele):
        appel = modele.return_value.bind.return_value.invoke
        appel.return_value.content = '{"langue":"en","etapes":[]}'
        r = chat.answer_question("My laptop cannot find any Wi-Fi networks.")
        self.assertEqual(r, {"answer": chat.REFUS["en"], "sources": []})
        appel.assert_called_once()
