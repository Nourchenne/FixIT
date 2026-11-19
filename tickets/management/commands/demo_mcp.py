from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from integrations.mcp_client import ErreurMCP, appeler_outil, lister_outils


class Command(BaseCommand):
    help = ("Démontrer le passage réel par MCP : liste des outils, création "
            "idempotente d'un ticket, consultation de son statut, accès refusé.")

    def add_arguments(self, parser):
        parser.add_argument("--utilisateur", default="demo")
        parser.add_argument("--autre", default="",
                            help="Second compte, pour vérifier l'isolement.")

    def handle(self, *args, utilisateur, autre, **options):
        User = get_user_model()
        user = User.objects.filter(username=utilisateur).first()
        if user is None:
            raise CommandError(f"Compte « {utilisateur} » introuvable "
                               "(lancer d'abord creer_comptes_demo).")

        self.stdout.write("1. Outils exposés par le serveur MCP : "
                          + ", ".join(lister_outils(user)))

        demande = {
            "titre": "Aucun réseau Wi-Fi visible",
            "description": "Le portable ne détecte aucun réseau Wi-Fi.",
            "essais": "Wi-Fi activé dans les paramètres ; redémarrage du PC.",
            "categorie": "wifi",
            "cle_creation": f"demo-{uuid4().hex}",
        }
        premier = appeler_outil("create_ticket", demande, user)
        second = appeler_outil("create_ticket", demande, user)
        self.stdout.write(
            f"2. Création : ticket n° {premier['id']} (créé : {premier['cree']}) ; "
            f"renvoi de la même demande : ticket n° {second['id']} (créé : {second['cree']})")
        if premier["id"] != second["id"]:
            raise CommandError("Idempotence non respectée : deux tickets créés.")

        statut = appeler_outil("get_ticket_status", {"ticket_id": premier["id"]}, user)
        self.stdout.write(
            f"3. Statut via MCP : {statut['statut_libelle']} — "
            f"{len(statut['evenements'])} événement(s) dans l'historique")

        if autre:
            intrus = User.objects.filter(username=autre).first()
            if intrus is None:
                raise CommandError(f"Compte « {autre} » introuvable.")
            try:
                appeler_outil("get_ticket_status", {"ticket_id": premier["id"]}, intrus)
            except ErreurMCP as refus:
                self.stdout.write(f"4. Accès par « {autre} » refusé : {refus}")
            else:
                raise CommandError("Un autre utilisateur a pu lire le ticket.")

        self.stdout.write(self.style.SUCCESS("Passage par MCP vérifié."))
