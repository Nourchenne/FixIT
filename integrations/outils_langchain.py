"""Outils LangChain branchés sur le serveur MCP (cahier technique, §6.3).

Le modèle choisit l'outil et ses arguments (le numéro du ticket) ; l'identité
de l'utilisateur est fixée par le backend dans la fermeture ci-dessous et ne
fait jamais partie des arguments du modèle (§6.4).

La création de ticket n'est pas confiée au modèle : elle passe par la
confirmation explicite de l'utilisateur dans l'interface, puis par MCP.
"""
import json

from langchain_core.tools import StructuredTool

from integrations.mcp_client import ErreurMCP, appeler_outil


def outils_tickets(actor):
    def get_ticket_status(ticket_id: int) -> str:
        """Consulter le statut et l'historique d'un ticket FixIT à partir de son numéro."""
        try:
            resultat = appeler_outil("get_ticket_status", {"ticket_id": ticket_id}, actor)
        except ErreurMCP as erreur:
            return f"Erreur : {erreur}"
        return json.dumps(resultat, ensure_ascii=False)

    return [StructuredTool.from_function(get_ticket_status)]
