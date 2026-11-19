"""Serveur MCP de FixIT : expose les outils de tickets.

Le backend Django le lance comme sous-processus (transport stdio) à chaque
appel d'outil. L'identité de l'utilisateur arrive par la variable
d'environnement FIXIT_ACTOR_ID, fixée par le backend à partir de la session
authentifiée : elle ne fait jamais partie des arguments choisis par le modèle.

Lancement manuel (test) : python -m mcp_server.server
SDK MCP 2.x : la classe s'appelle MCPServer (FastMCP dans les tutoriels 1.x).
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402

from tickets import services  # noqa: E402


serveur = MCPServer(
    "fixit-tickets",
    instructions="Création et suivi des tickets de support FixIT.",
    log_level="WARNING",  # un refus métier n'est pas une anomalie du serveur
)


def executer(fonction, *args):
    """Traduire une erreur métier en ToolError : le client reçoit le message
    lisible (« Ticket 3 introuvable. ») au lieu d'une erreur technique."""
    try:
        return fonction(*args)
    except services.TicketErreur as erreur:
        raise ToolError(str(erreur)) from erreur


def acteur():
    """Utilisateur au nom duquel le backend a lancé ce serveur."""
    identifiant = os.environ.get("FIXIT_ACTOR_ID", "")
    if not identifiant.isdigit():
        raise services.ActionRefusee("Contexte utilisateur absent.")
    user = get_user_model().objects.filter(pk=int(identifiant), is_active=True).first()
    if user is None:
        raise services.ActionRefusee("Utilisateur inconnu ou désactivé.")
    return user


@serveur.tool()
def create_ticket(titre: str, description: str, cle_creation: str,
                  categorie: str = "autre", essais: str = "") -> dict:
    """Créer un ticket de support pour l'utilisateur connecté.

    cle_creation : identifiant unique de la demande ; renvoyer la même clé ne
    crée pas de second ticket. categorie : wifi, performance, applications,
    stockage, peripheriques ou autre. essais : étapes déjà essayées.
    """
    return executer(lambda: services.create_ticket(acteur(), {
        "titre": titre, "description": description, "cle_creation": cle_creation,
        "categorie": categorie, "essais": essais,
    }))


@serveur.tool()
def get_ticket_status(ticket_id: int) -> dict:
    """Consulter le statut et l'historique d'un ticket de l'utilisateur."""
    return executer(lambda: services.get_ticket(acteur(), ticket_id))


if __name__ == "__main__":
    serveur.run("stdio")
