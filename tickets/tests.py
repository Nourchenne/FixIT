import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from accounts.roles import GROUPE_TECHNICIEN
from integrations.mcp_client import ErreurMCP, ServiceMCPIndisponible
from tickets import services
from tickets.models import Ticket


def demande(**extra):
    donnees = {"titre": "Aucun réseau Wi-Fi", "description": "Le portable ne voit aucun réseau.",
               "essais": "Wi-Fi activé.", "categorie": "wifi", "cle_creation": "cle-0001-test"}
    donnees.update(extra)
    return donnees


class Base(TestCase):
    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user("alice", password="motdepasse-alice")
        self.bob = User.objects.create_user("bob", password="motdepasse-bob")
        self.tech = User.objects.create_user("tech", password="motdepasse-tech")
        groupe, _ = Group.objects.get_or_create(name=GROUPE_TECHNICIEN)
        self.tech.groups.add(groupe)


class ServiceTests(Base):
    def test_creation_et_premier_evenement(self):
        r = services.create_ticket(self.alice, demande())
        self.assertTrue(r["cree"])
        self.assertEqual(r["statut"], "ouvert")
        ticket = Ticket.objects.get(pk=r["id"])
        self.assertEqual(ticket.proprietaire, self.alice)
        self.assertEqual(ticket.evenements.count(), 1)

    def test_idempotence(self):
        premier = services.create_ticket(self.alice, demande())
        second = services.create_ticket(self.alice, demande())
        self.assertEqual(premier["id"], second["id"])
        self.assertFalse(second["cree"])
        self.assertEqual(Ticket.objects.count(), 1)

    def test_cle_deja_utilisee_par_un_autre(self):
        services.create_ticket(self.alice, demande())
        with self.assertRaises(services.DonneesInvalides):
            services.create_ticket(self.bob, demande())

    def test_validation(self):
        for mauvais in ({"titre": ""}, {"description": "  "}, {"categorie": "inconnue"},
                        {"cle_creation": "court"}, {"titre": "x" * 201}, {"titre": 12}):
            with self.subTest(mauvais=mauvais):
                with self.assertRaises(services.DonneesInvalides):
                    services.create_ticket(self.alice, demande(**mauvais))

    def test_visibilite(self):
        ticket_id = services.create_ticket(self.alice, demande())["id"]
        self.assertEqual(services.get_ticket(self.alice, ticket_id)["id"], ticket_id)
        self.assertEqual(services.get_ticket(self.tech, ticket_id)["id"], ticket_id)
        with self.assertRaises(services.TicketIntrouvable):
            services.get_ticket(self.bob, ticket_id)
        with self.assertRaises(services.TicketIntrouvable):
            services.get_ticket(self.alice, 9999)

    def test_cycle_de_vie_complet(self):
        ticket_id = services.create_ticket(self.alice, demande())["id"]
        for statut in ("en_cours", "resolu", "ferme"):
            services.changer_statut(self.tech, ticket_id, statut, f"Passage à {statut}")
        ticket = Ticket.objects.get(pk=ticket_id)
        self.assertEqual(ticket.statut, "ferme")
        self.assertEqual(ticket.technicien, self.tech)
        services.rouvrir(self.alice, ticket_id, "Le problème est revenu.")
        ticket.refresh_from_db()
        self.assertEqual(ticket.statut, "ouvert")
        self.assertEqual(ticket.evenements.count(), 5)

    def test_transitions_interdites(self):
        ticket_id = services.create_ticket(self.alice, demande())["id"]
        with self.assertRaises(services.ActionRefusee):
            services.changer_statut(self.tech, ticket_id, "ferme")
        with self.assertRaises(services.ActionRefusee):
            services.changer_statut(self.alice, ticket_id, "en_cours")
        with self.assertRaises(services.ActionRefusee):
            services.rouvrir(self.alice, ticket_id)

    def test_note_technicien(self):
        ticket_id = services.create_ticket(self.alice, demande())["id"]
        services.ajouter_note(self.tech, ticket_id, "Pilote Wi-Fi à mettre à jour.")
        with self.assertRaises(services.ActionRefusee):
            services.ajouter_note(self.alice, ticket_id, "Je veux noter.")

    def test_listes(self):
        services.create_ticket(self.alice, demande())
        services.create_ticket(self.bob, demande(cle_creation="cle-0002-test"))
        self.assertEqual(services.lister_tickets(self.alice).count(), 1)
        self.assertEqual(services.lister_tickets(self.tech, tous=True).count(), 2)
        with self.assertRaises(services.ActionRefusee):
            services.lister_tickets(self.alice, tous=True)


class PagesTests(Base):
    def test_liste_et_detail(self):
        ticket_id = services.create_ticket(self.alice, demande())["id"]
        self.client.force_login(self.alice)
        page = self.client.get(reverse("tickets:liste"))
        self.assertContains(page, "Aucun réseau Wi-Fi")
        page = self.client.get(reverse("tickets:detail", args=[ticket_id]))
        self.assertContains(page, "Ticket créé depuis FixIT.")
        self.assertNotContains(page, "Traiter le ticket")

    def test_isolement_et_espace_technicien(self):
        ticket_id = services.create_ticket(self.alice, demande())["id"]
        self.client.force_login(self.bob)
        self.assertEqual(self.client.get(reverse("tickets:detail", args=[ticket_id])).status_code, 404)
        self.assertEqual(self.client.get(reverse("tickets:technicien")).status_code, 403)
        self.client.force_login(self.tech)
        self.assertContains(self.client.get(reverse("tickets:technicien")), "alice")

    def test_traitement_par_le_technicien(self):
        ticket_id = services.create_ticket(self.alice, demande())["id"]
        self.client.force_login(self.tech)
        url = reverse("tickets:traiter", args=[ticket_id])
        self.client.post(url, {"statut": "en_cours", "note": "Pris en charge."})
        self.assertEqual(Ticket.objects.get(pk=ticket_id).statut, "en_cours")
        r = self.client.post(url, {"statut": "ferme"}, follow=True)
        self.assertContains(r, "impossible")

    def test_filtres(self):
        services.create_ticket(self.alice, demande())
        self.client.force_login(self.alice)
        self.assertContains(self.client.get(reverse("tickets:liste") + "?statut=resolu"),
                            "ne correspond")
        self.assertContains(self.client.get(reverse("tickets:liste") + "?q=wi-fi"),
                            "Aucun réseau Wi-Fi")


class CreationDepuisChatTests(Base):
    def poster(self, donnees):
        return self.client.post(reverse("tickets:creer"), data=json.dumps(donnees),
                                content_type="application/json")

    @patch("tickets.views.appeler_outil")
    def test_creation_passe_par_mcp(self, outil):
        outil.return_value = {"id": 7, "statut_libelle": "Ouvert", "cree": True}
        self.client.force_login(self.alice)
        r = self.poster(demande())
        self.assertEqual(r.json(), {"id": 7, "statut": "Ouvert", "cree": True,
                                    "url": reverse("tickets:detail", args=[7])})
        nom, arguments, acteur = outil.call_args.args
        self.assertEqual(nom, "create_ticket")
        self.assertEqual(acteur, self.alice)
        self.assertEqual(arguments["cle_creation"], "cle-0001-test")

    @patch("tickets.views.appeler_outil", side_effect=ErreurMCP("Catégorie inconnue."))
    def test_refus_metier(self, outil):
        self.client.force_login(self.alice)
        r = self.poster(demande(categorie="x"))
        self.assertEqual((r.status_code, r.json()["error"]), (400, "Catégorie inconnue."))

    @patch("tickets.views.appeler_outil", side_effect=ServiceMCPIndisponible("Indisponible."))
    def test_service_indisponible(self, outil):
        self.client.force_login(self.alice)
        self.assertEqual(self.poster(demande()).status_code, 503)

    def test_anonyme(self):
        self.assertEqual(self.poster(demande()).status_code, 401)
