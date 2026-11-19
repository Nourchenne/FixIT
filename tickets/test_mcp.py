import os
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from integrations import mcp_client
from mcp.server.mcpserver.exceptions import ToolError


def resultat(textes=(), erreur=False, structure=None):
    return SimpleNamespace(content=[SimpleNamespace(text=t) for t in textes],
                           is_error=erreur, structured_content=structure)


class ClientTests(TestCase):
    def test_reponse_structuree(self):
        self.assertEqual(mcp_client._contenu(resultat(structure={"id": 3})), {"id": 3})
        self.assertEqual(mcp_client._contenu(resultat(structure={"result": [1]})), [1])

    def test_reponse_texte_json(self):
        self.assertEqual(mcp_client._contenu(resultat(['{"id": 4}'])), {"id": 4})

    def test_erreur_metier_sans_prefixe_technique(self):
        with self.assertRaisesMessage(mcp_client.ErreurMCP, "Ticket 5 introuvable."):
            mcp_client._contenu(resultat(
                ["Error executing tool get_ticket_status: Ticket 5 introuvable."], erreur=True))

    def test_identite_transmise_par_l_environnement(self):
        p = mcp_client.parametres_serveur(42)
        self.assertEqual(p.env["FIXIT_ACTOR_ID"], "42")
        self.assertEqual(p.args, ["-m", "mcp_server.server"])


class ServeurTests(TestCase):
    """Les outils du serveur, appelés directement (sans transport)."""

    def setUp(self):
        from mcp_server import server
        self.server = server
        self.alice = get_user_model().objects.create_user("alice", password="motdepasse-alice")

    def test_creation_et_statut(self):
        with patch.dict(os.environ, {"FIXIT_ACTOR_ID": str(self.alice.pk)}):
            ticket = self.server.create_ticket("Wi-Fi absent", "Aucun réseau.", "cle-serveur-01",
                                               categorie="wifi")
            statut = self.server.get_ticket_status(ticket["id"])
        self.assertEqual(statut["statut"], "ouvert")
        self.assertEqual(len(statut["evenements"]), 1)

    def test_erreurs_traduites_en_tool_error(self):
        with patch.dict(os.environ, {"FIXIT_ACTOR_ID": str(self.alice.pk)}):
            with self.assertRaisesMessage(ToolError, "Ticket 999 introuvable."):
                self.server.get_ticket_status(999)
        with patch.dict(os.environ, {"FIXIT_ACTOR_ID": ""}):
            with self.assertRaisesMessage(ToolError, "Contexte utilisateur absent."):
                self.server.get_ticket_status(1)
