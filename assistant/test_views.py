import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from assistant.models import Conversation, Message


def reponse(type_reponse="etapes", answer="1. Active le Wi-Fi. [S1]"):
    sources = [] if type_reponse != "etapes" else [
        {"ref": "S1", "doc_id": "DOC001", "titre": "Guide Wi-Fi",
         "page": 8, "url": "https://example.org/wifi"}]
    return {"answer": answer, "sources": sources, "langue": "fr",
            "type": type_reponse, "ticket_suggere": False}


SERVICE = "assistant.services.chat.answer_question"


class VuesChatTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user("alice", password="motdepasse-alice")
        self.bob = User.objects.create_user("bob", password="motdepasse-bob")
        self.client.force_login(self.alice)

    def poser(self, question, conversation_id=None):
        return self.client.post(
            reverse("assistant:ask"),
            data=json.dumps({"question": question, "conversation_id": conversation_id}),
            content_type="application/json",
        )

    def test_page_exige_une_connexion(self):
        self.client.logout()
        r = self.client.get(reverse("assistant:chat"))
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse("login"), r["Location"])

    def test_question_anonyme_refusee(self):
        self.client.logout()
        r = self.poser("Wi-Fi absent")
        self.assertEqual(r.status_code, 401)

    @patch(SERVICE, return_value=reponse())
    def test_echange_enregistre(self, service):
        r = self.poser("Mon PC ne trouve aucun réseau Wi-Fi.")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        conversation = Conversation.objects.get(pk=data["conversation_id"])
        self.assertEqual(conversation.proprietaire, self.alice)
        roles = list(conversation.messages.values_list("role", flat=True))
        self.assertEqual(roles, ["user", "assistant"])
        reponse_fixit = conversation.messages.last()
        self.assertEqual(reponse_fixit.references[0]["doc_id"], "DOC001")
        self.assertEqual(reponse_fixit.type_reponse, "etapes")

    @patch(SERVICE, return_value=reponse())
    def test_suite_de_conversation(self, service):
        premiere = self.poser("Wi-Fi absent").json()["conversation_id"]
        seconde = self.poser("Toujours rien", premiere).json()["conversation_id"]
        self.assertEqual(premiere, seconde)
        self.assertEqual(Message.objects.filter(conversation_id=premiere).count(), 4)

    @patch(SERVICE, return_value=reponse())
    def test_conversation_d_un_autre_utilisateur(self, service):
        autre = Conversation.objects.create(proprietaire=self.bob, titre="Bob")
        r = self.poser("Wi-Fi absent", autre.pk)
        self.assertEqual(r.status_code, 404)
        service.assert_not_called()

    def test_historique_isole(self):
        Conversation.objects.create(proprietaire=self.alice, titre="Conversation d'Alice")
        bob = Conversation.objects.create(proprietaire=self.bob, titre="Conversation de Bob")
        page = self.client.get(reverse("assistant:chat"))
        self.assertContains(page, "Conversation d&#x27;Alice")
        self.assertNotContains(page, "Conversation de Bob")
        r = self.client.get(reverse("assistant:chat") + f"?conversation={bob.pk}")
        self.assertEqual(r.status_code, 404)
        r = self.client.get(reverse("assistant:chat") + "?conversation=abc")
        self.assertEqual(r.status_code, 404)

    @patch(SERVICE)
    def test_clarification_reliee_a_la_question(self, service):
        service.return_value = reponse("clarification", "Sur quel appareil ?")
        conversation_id = self.poser("Wi-Fi ?").json()["conversation_id"]
        service.return_value = reponse()
        self.poser("Mon portable ne voit aucun réseau.", conversation_id)
        service.assert_called_with("Wi-Fi ? — Mon portable ne voit aucun réseau.")

    @patch(SERVICE, side_effect=RuntimeError("Groq indisponible"))
    def test_erreur_technique(self, service):
        r = self.poser("Wi-Fi absent")
        self.assertEqual(r.status_code, 500)
        self.assertEqual(Conversation.objects.count(), 0)

    def test_question_trop_longue(self):
        self.assertEqual(self.poser("x" * 1001).status_code, 400)

    def test_page_de_connexion(self):
        self.client.logout()
        page = self.client.get(reverse("login"))
        self.assertContains(page, "Connexion à FixIT")
        r = self.client.post(reverse("login"),
                             {"username": "alice", "password": "motdepasse-alice"})
        self.assertRedirects(r, reverse("assistant:chat"), fetch_redirect_response=False)
        r = self.client.post(reverse("logout"))
        self.assertRedirects(r, reverse("login"), fetch_redirect_response=False)
