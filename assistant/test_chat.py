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


class LangueTests(unittest.TestCase):
    """La langue de la réponse est décidée par le code, pas par le modèle."""

    def test_detecter_langue(self):
        cas = [
            ("Mon ordinateur ne trouve aucun réseau Wi-Fi.", "fr"),
            ("No Wi-Fi networks show up in the taskbar.", "en"),
            ("Wi-Fi disconnects whenever my laptop wakes from sleep.", "en"),
            ("Connected to Wi-Fi, no internet, yellow triangle on the icon.", "en"),
            ("Réponds en anglais : mon Wi-Fi coupe.", "en"),
            ("Answer in French: my Wi-Fi keeps dropping.", "fr"),
            ("Wi-Fi ?", None),
        ]
        for texte, attendu in cas:
            with self.subTest(texte=texte):
                self.assertEqual(chat.detecter_langue(texte), attendu)

    def test_question_courte_en_francais(self):
        self.assertEqual(chat.langue_question("Wi-Fi ?"), "fr")

    def test_langue_imposee_au_formatage(self):
        meta = {"doc_id": "DOC001", "titre": "Guide", "page": 1,
                "source_url": "https://example.org"}
        r = chat.formater_reponse({"langue": "fr", "etapes": []},
                                  [{"page_content": "x", "metadata": meta}],
                                  langue="en")
        self.assertEqual(r, repli("en"))

    @patch.dict("os.environ", {"GROQ_API_KEY": "test", "GROQ_MODEL": "test"})
    @patch.object(chat, "ChatGroq")
    @patch.object(chat, "search_documents")
    def test_reponse_dans_la_mauvaise_langue_relancee(self, recherche, modele):
        recherche.return_value = [{"page_content": "Activez le Wi-Fi.", "metadata": {
            "doc_id": "DOC001", "titre": "Guide Wi-Fi", "page": 8,
            "source_url": "https://example.org/wifi"}}]
        chat.get_modele.cache_clear()
        self.addCleanup(chat.get_modele.cache_clear)
        appel = modele.return_value.bind.return_value.invoke
        en_francais = ('{"langue":"fr","resume":"Le PC ne voit aucun réseau.",'
                       '"etapes":[{"texte":"Activez le Wi-Fi dans les paramètres.","source":1}]}')
        en_anglais = ('{"langue":"en","resume":"The PC does not see any network.",'
                      '"etapes":[{"texte":"Turn on Wi-Fi in the settings.","source":1}]}')
        appel.side_effect = [type("M", (), {"content": en_francais}),
                             type("M", (), {"content": en_anglais})]

        r = chat.answer_question("No Wi-Fi networks show up in the taskbar.")

        self.assertEqual(appel.call_count, 2)
        demande = appel.call_args_list[0].args[0][1][1]
        self.assertIn('"langue": "en"', demande)
        self.assertEqual(r["langue"], "en")
        self.assertIn("Turn on Wi-Fi in the settings. [S1]", r["answer"])


class AvertissementTests(unittest.TestCase):
    """Une étape qui peut effacer les données est précédée d'un avertissement."""

    def setUp(self):
        meta = {"doc_id": "DOC020", "titre": "Réinitialiser le PC", "page": 2,
                "source_url": "https://example.org/reset"}
        self.passages = [{"page_content": "x", "metadata": meta}]

    def formater(self, langue, resume, texte):
        donnees = {"langue": langue, "resume": resume,
                   "etapes": [{"texte": texte, "source": 1}]}
        return chat.formater_reponse(donnees, self.passages)["answer"].split("\n")

    def test_avertissement_ajoute_avant_les_etapes(self):
        lignes = self.formater(
            "fr", "Vous voulez réinitialiser votre PC.",
            "Ouvrez Réinitialiser ce PC, puis choisissez une option.")
        self.assertEqual(lignes[1], chat.AVERTISSEMENT_DONNEES["fr"])
        self.assertTrue(lignes[2].startswith("1. "))

    def test_avertissement_en_anglais(self):
        lignes = self.formater("en", "You want to reset your PC.",
                               "Select Reset this PC, then Remove everything.")
        self.assertIn(chat.AVERTISSEMENT_DONNEES["en"], lignes)

    def test_pas_de_doublon_si_deja_averti(self):
        lignes = self.formater(
            "fr", "Vous voulez réinitialiser votre PC.",
            "Sauvegardez vos fichiers, puis ouvrez Réinitialiser ce PC.")
        self.assertNotIn(chat.AVERTISSEMENT_DONNEES["fr"], lignes)

    def test_mot_perdu_dans_une_autre_etape_ne_suffit_pas(self):
        # Cas réel : « Supprimer tout » sans avertissement à l'étape 1, et
        # « seront perdues » à l'étape 2, qui parle d'un point de restauration.
        donnees = {"langue": "fr", "resume": "Vous souhaitez réinitialiser votre PC.",
                   "etapes": [
                       {"texte": "Ouvrez Réinitialiser ce PC. Choisissez « Conserver "
                                 "mes fichiers » ou « Supprimer tout ».", "source": 1},
                       {"texte": "Choisissez un point de restauration. Seules les "
                                 "modifications postérieures seront perdues.", "source": 1}]}
        lignes = chat.formater_reponse(donnees, self.passages)["answer"].split("\n")
        self.assertEqual(lignes[1], chat.AVERTISSEMENT_DONNEES["fr"])

    def test_etape_sur_plusieurs_lignes_mise_sur_une_ligne(self):
        donnees = {"langue": "fr", "etapes": [{"texte": "Exécutez :\n1. netsh int ip reset"
                                                         "\n2. ipconfig /renew", "source": 1}]}
        r = chat.formater_reponse(donnees, self.passages)
        self.assertEqual(r["answer"],
                         "1. Exécutez : 1. netsh int ip reset 2. ipconfig /renew [S1]")

    def test_reinitialisation_du_reseau_non_concernee(self):
        lignes = self.formater("fr", "Le Wi-Fi ne fonctionne plus.",
                               "Lancez la réinitialisation du réseau.")
        self.assertNotIn(chat.AVERTISSEMENT_DONNEES["fr"], lignes)
