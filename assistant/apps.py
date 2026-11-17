import logging
import os
import sys
import threading
import time

from django.apps import AppConfig


logger = logging.getLogger(__name__)


def doit_precharger(argv=None, environ=None):
    """Précharger uniquement dans le processus qui sert les requêtes web."""
    argv = sys.argv if argv is None else argv
    environ = os.environ if environ is None else environ

    if environ.get("FIXIT_PRECHARGEMENT", "1") == "0":
        return False
    if "runserver" not in argv:
        return False  # rien pendant migrate, test, shell, createsuperuser...
    if "--noreload" in argv:
        return True
    # Avec le rechargement automatique, runserver lance deux processus :
    # seul celui qui porte RUN_MAIN=true répond aux requêtes.
    return environ.get("RUN_MAIN") == "true"


def precharger():
    """Charger le modèle d'embedding et ouvrir la connexion Qdrant."""
    debut = time.perf_counter()
    try:
        from assistant.services.retrieval import get_client, load_index_info
        from documents.services.embeddings import embed_query

        embed_query("préchargement du modèle")
        load_index_info()
        get_client()
    except Exception as erreur:  # le serveur doit démarrer même si Qdrant est arrêté
        logger.warning("FixIT : préchargement incomplet (%s)", erreur)
        return
    logger.info("FixIT : modèle et connexion prêts en %.1f s",
                time.perf_counter() - debut)


class AssistantConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "assistant"

    def ready(self):
        if doit_precharger():
            threading.Thread(
                target=precharger, name="fixit-prechargement", daemon=True
            ).start()
