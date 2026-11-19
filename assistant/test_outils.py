import json
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from langchain_core.messages import AIMessage, ToolMessage

from assistant.models import Message
from assistant.services import outils


class DetectionTests(TestCase):
    def test_questions_de_suivi(self):
        self.assertTrue(outils.concerne_un_ticket("Où en est mon ticket 12 ?"))
        self.assertTrue(outils.concerne_un_ticket("What is the status of ticket #3?"))
        self.assertFalse(outils.concerne_un_ticket("Comment créer un ticket ?"))
        self.assertFalse(outils.concerne_un_ticket("Mon PC a 2 écrans noirs."))


class AgentTests(TestCase):
    def setUp(self):
        self.alice = get_user_model().objects.create_user("alice", password="motdepasse-alice")
        outils.get_modele_outils.cache_clear()
        self.addCleanup(outils.get_modele_outils.cache_clear)

    @patch("integrations.outils_langchain.appeler_outil")
    @patch.object(outils, "get_modele_outils")
    def test_boucle_outil_puis_reponse(self, modele, appeler_outil):
        appeler_outil.return_value = {"id": 3, "statut_libelle": "En cours"}
        lie = modele.return_value.bind_tools.return_value
        lie.invoke.side_effect = [
            AIMessage(content="", tool_calls=[
                {"name": "get_ticket_status", "args": {"ticket_id": 3}, "id": "appel-1"}]),
            AIMessage(content="Votre ticket 3 est en cours de traitement."),
        ]
        r = outils.repondre_sur_ticket("Où en est mon ticket 3 ?", self.alice)

        self.assertEqual(r["answer"], "Votre ticket 3 est en cours de traitement.")
        self.assertEqual((r["type"], r["langue"]), ("ticket", "fr"))
        appeler_outil.assert_called_once_with("get_ticket_status", {"ticket_id": 3}, self.alice)
        historique = lie.invoke.call_args_list[1].args[0]
        resultats_outil = [m for m in historique if isinstance(m, ToolMessage)]
        self.assertEqual(len(resultats_outil), 1)
        self.assertEqual(resultats_outil[0].tool_call_id, "appel-1")
        self.assertIn("En cours", resultats_outil[0].content)

    @patch("assistant.services.outils.repondre_sur_ticket")
    @patch("assistant.services.chat.answer_question")
    def test_routage_dans_le_chat(self, documentaire, suivi):
        suivi.return_value = {"answer": "Ticket 3 : en cours.", "sources": [], "langue": "fr",
                              "type": "ticket", "ticket_suggere": False}
        self.client.force_login(self.alice)
        r = self.client.post(reverse("assistant:ask"), content_type="application/json",
                             data=json.dumps({"question": "Où en est mon ticket 3 ?"}))
        self.assertEqual(r.status_code, 200)
        documentaire.assert_not_called()
        self.assertEqual(Message.objects.last().type_reponse, "ticket")
