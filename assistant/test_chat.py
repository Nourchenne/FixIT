import unittest
from unittest.mock import patch

from assistant.services import chat


def repli(lang, ticket=False):
    answer = chat.REFUS[lang]
    if ticket:
        answer += "\n" + chat.SUGGESTION_TICKET[lang]
    return {"answer": answer, "sources": [], "langue": lang,
            "type": "repli", "ticket_suggere": ticket}


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.meta = {"doc_id": "DOC001", "titre": "Guide Wi-Fi",
                     "page": 8, "source_url": "https://example.org/wifi"}
        self.passages = [{"page_content": "Active le Wi-Fi.",
                          "metadata": self.meta}]
        chat.get_modele.cache_clear()
        self.addCleanup(chat.get_modele.cache_clear)

    # --- comportements d'origine (citations, repli, langue) ---------------

    def test_citations_fr_et_en(self):
        for lang, text in [("fr", "Active le Wi-Fi."),
                           ("en", "Turn on Wi-Fi.")]:
            step = {"texte": text, "source": 1}
            data = {"langue": lang, "etapes": [step, step]}
            r = chat.formater_reponse(data, self.passages)
            self.assertEqual(r["type"], "etapes")
            self.assertEqual(r["langue"], lang)
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
                self.assertEqual(r, repli(lang))

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
        self.assertEqual(r, repli("en"))
        appel.assert_called_once()

    # --- mission 1 : clarification, résumé, ticket ---------------------------

    def test_clarification(self):
        for lang, question in [("fr", "Sur quel appareil le Wi-Fi pose-t-il problème ?"),
                               ("en", "Which device has the Wi-Fi problem?")]:
            data = {"langue": lang, "clarification": question, "etapes": []}
            r = chat.formater_reponse(data, self.passages)
            self.assertEqual(r, {"answer": question, "sources": [], "langue": lang,
                                 "type": "clarification", "ticket_suggere": False})

    def test_clarification_vide_ignoree(self):
        data = {"langue": "fr", "clarification": "  ",
                "etapes": [{"texte": "Active le Wi-Fi.", "source": 1}]}
        r = chat.formater_reponse(data, self.passages)
        self.assertEqual(r["type"], "etapes")

    def test_resume_numerotation_et_ticket(self):
        data = {"langue": "fr", "resume": "Le PC ne voit aucun réseau.",
                "etapes": [{"texte": "Active le Wi-Fi.", "source": 1},
                           {"texte": "Redémarre le routeur.", "source": 1}],
                "ticket": True}
        r = chat.formater_reponse(data, self.passages)
        lignes = r["answer"].split("\n")
        self.assertEqual(lignes[0], "Le PC ne voit aucun réseau.")
        self.assertEqual(lignes[1], "1. Active le Wi-Fi. [S1]")
        self.assertEqual(lignes[2], "2. Redémarre le routeur. [S1]")
        self.assertEqual(lignes[3], chat.SUGGESTION_TICKET["fr"])
        self.assertTrue(r["ticket_suggere"])

    def test_ticket_sur_repli(self):
        r = chat.formater_reponse({"langue": "en", "etapes": [], "ticket": True},
                                  self.passages)
        self.assertEqual(r, repli("en", ticket=True))

    @patch.dict("os.environ", {"GROQ_API_KEY": "test", "GROQ_MODEL": "test"})
    @patch.object(chat, "ChatGroq")
    def test_client_groq_reutilise(self, modele):
        self.assertIs(chat.get_modele(), chat.get_modele())
        modele.assert_called_once()

    @patch.dict("os.environ", {"GROQ_API_KEY": "", "GROQ_MODEL": ""})
    @patch.object(chat, "load_dotenv")
    def test_configuration_manquante(self, _dotenv):
        with self.assertRaises(ValueError):
            chat.get_modele()
