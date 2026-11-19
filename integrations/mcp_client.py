"""Client MCP du backend FixIT.

Chaque appel lance le serveur MCP (python -m mcp_server.server) en
sous-processus, lui transmet l'identité de l'utilisateur dans son
environnement, appelle l'outil, puis ferme la connexion.
"""
import asyncio
import json
import logging
import os
import re
import sys
import time
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
DELAI_SECONDES = 30


PREFIXE_ERREUR = re.compile(r"^Error executing tool [\w-]+:\s*")


class ErreurMCP(Exception):
    """Outil refusé par le serveur : le message est affichable."""


class ServiceMCPIndisponible(ErreurMCP):
    """Le serveur MCP n'a pas pu être lancé ou n'a pas répondu."""


def parametres_serveur(actor_id):
    return StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.server"],
        cwd=str(BASE_DIR),
        env={
            "DJANGO_SETTINGS_MODULE": os.environ.get(
                "DJANGO_SETTINGS_MODULE", "config.settings"),
            "FIXIT_ACTOR_ID": str(actor_id),
            "PYTHONIOENCODING": "utf-8",
        },
    )


def _contenu(resultat):
    """Extraire la réponse d'un CallToolResult (structurée ou texte JSON)."""
    textes = [c.text for c in (resultat.content or []) if getattr(c, "text", None)]
    if resultat.is_error:
        message = PREFIXE_ERREUR.sub("", " ".join(textes)).strip()
        raise ErreurMCP(message or "L'outil a refusé la demande.")
    donnees = resultat.structured_content
    if donnees is None and textes:
        try:
            donnees = json.loads(textes[0])
        except json.JSONDecodeError:
            donnees = {"texte": textes[0]}
    if isinstance(donnees, dict) and set(donnees) == {"result"}:
        donnees = donnees["result"]
    return donnees


async def _session(actor_id, action):
    async with stdio_client(parametres_serveur(actor_id)) as (lecture, ecriture):
        async with ClientSession(lecture, ecriture) as session:
            await session.initialize()
            return await action(session)


def _executer(actor, action):
    debut = time.perf_counter()
    try:
        resultat = asyncio.run(asyncio.wait_for(
            _session(actor.pk, action), timeout=DELAI_SECONDES))
    except Exception as erreur:
        logger.exception("Serveur MCP indisponible")
        raise ServiceMCPIndisponible(
            "Le service de tickets est indisponible. Réessayez.") from erreur
    finally:
        logger.info("MCP : appel terminé en %.0f ms",
                    (time.perf_counter() - debut) * 1000)
    return resultat


def appeler_outil(nom, arguments, actor):
    """Appeler un outil MCP au nom de actor (appel synchrone, vues Django).

    La réponse est analysée après la fermeture de la session : une erreur
    métier levée à l'intérieur serait sinon emballée dans un groupe
    d'exceptions par la bibliothèque asynchrone.
    """
    async def action(session):
        return await session.call_tool(nom, arguments)
    return _contenu(_executer(actor, action))


def lister_outils(actor):
    """Noms des outils exposés par le serveur (démonstration)."""
    async def action(session):
        return [outil.name for outil in (await session.list_tools()).tools]
    return _executer(actor, action)
