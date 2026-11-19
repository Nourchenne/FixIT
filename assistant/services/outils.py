"""Suivi des tickets dans le chat : tool calling LangChain + MCP.

Même boucle que le lab 09 du cours : le modèle demande un outil, le backend
l'exécute (ici via le serveur MCP), renvoie le résultat au modèle, qui rédige
la réponse finale.
"""
import logging
import os
import re
from functools import lru_cache

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq

from assistant.services.chat import BASE_DIR
from integrations.outils_langchain import outils_tickets


logger = logging.getLogger(__name__)

TOURS_MAX = 3
MOTIF_TICKET = re.compile(r"\btickets?\b", re.IGNORECASE)
MOTIF_NUMERO = re.compile(r"\d+")
MOTIF_FRANCAIS = re.compile(
    r"[àâçéèêëîïôûùüÿœ]|\b(le|la|les|mon|ma|est|où|quel|quelle|statut)\b",
    re.IGNORECASE,
)

CONSIGNE_TICKETS = """Tu es FixIT. Tu aides l'utilisateur à suivre ses tickets de support.
Utilise l'outil get_ticket_status pour connaître l'état d'un ticket à partir de son numéro.
Réponds dans la langue de la question, en deux ou trois phrases : statut actuel,
dernier événement utile et prochaine étape. N'invente aucune information ; si
l'outil renvoie une erreur, explique-la simplement."""


def concerne_un_ticket(question):
    """Question de suivi : elle parle d'un ticket et donne un numéro."""
    return bool(MOTIF_TICKET.search(question) and MOTIF_NUMERO.search(question))


def langue_probable(question):
    return "fr" if MOTIF_FRANCAIS.search(question) else "en"


@lru_cache(maxsize=1)
def get_modele_outils():
    """Client Groq pour le tool calling (sans le mode JSON du chat documentaire)."""
    load_dotenv(BASE_DIR / ".env")
    if not os.getenv("GROQ_API_KEY") or not os.getenv("GROQ_MODEL"):
        raise ValueError("Configure GROQ_API_KEY et GROQ_MODEL dans .env.")
    return ChatGroq(model=os.environ["GROQ_MODEL"], temperature=0,
                    timeout=45, max_retries=1)


def repondre_sur_ticket(question, actor):
    outils = {outil.name: outil for outil in outils_tickets(actor)}
    modele = get_modele_outils().bind_tools(list(outils.values()))
    messages = [SystemMessage(CONSIGNE_TICKETS), HumanMessage(question)]

    texte = ""
    for _ in range(TOURS_MAX):
        reponse = modele.invoke(messages)
        messages.append(reponse)
        if not reponse.tool_calls:
            texte = (reponse.content or "").strip()
            break
        for appel in reponse.tool_calls:
            outil = outils.get(appel["name"])
            resultat = (outil.invoke(appel["args"]) if outil
                        else f"Outil inconnu : {appel['name']}")
            logger.info("Outil %s appelé avec %s", appel["name"], appel["args"])
            messages.append(ToolMessage(content=str(resultat),
                                        tool_call_id=appel["id"]))

    langue = langue_probable(question)
    if not texte:
        texte = ("Je n'ai pas pu retrouver ce ticket. Consultez la page « Mes tickets »."
                 if langue == "fr" else
                 "I could not retrieve this ticket. Please check the “My tickets” page.")
    return {"answer": texte, "sources": [], "langue": langue,
            "type": "ticket", "ticket_suggere": False}
