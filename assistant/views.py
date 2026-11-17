import json
import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Conversation, Message


logger = logging.getLogger(__name__)

HISTORIQUE_MAX = 20
QUESTION_MAX = 1000


@login_required
def chat_page(request):
    """Page du chat : historique des conversations et conversation ouverte."""
    conversations = Conversation.objects.filter(
        proprietaire=request.user
    )[:HISTORIQUE_MAX]

    courante, historique = None, []
    identifiant = request.GET.get("conversation", "")
    if identifiant:
        if not identifiant.isdigit():
            raise Http404
        courante = get_object_or_404(
            Conversation, pk=int(identifiant), proprietaire=request.user
        )
        historique = courante.messages.all()

    return render(request, "assistant/chat.html", {
        "conversations": conversations,
        "courante": courante,
        "historique": historique,
    })


def _erreur(message, statut):
    return JsonResponse({"error": message}, status=statut)


def question_avec_contexte(conversation, question):
    """Si FixIT vient de demander une précision, relier la réponse de
    l'utilisateur à sa question de départ pour la recherche et le modèle."""
    if conversation is None:
        return question
    dernier = conversation.messages.filter(role=Message.Role.ASSISTANT).last()
    if dernier is None or dernier.type_reponse != "clarification":
        return question
    precedente = conversation.messages.filter(
        role=Message.Role.UTILISATEUR, cree_le__lte=dernier.cree_le
    ).last()
    if precedente is None:
        return question
    return f"{precedente.contenu} — {question}"


@require_POST
def ask(request):
    """Recevoir une question, interroger FixIT, enregistrer l'échange.

    L'import du service est fait ici (pas au chargement du module) pour éviter
    de charger les modèles lourds au démarrage de Django.
    """
    if not request.user.is_authenticated:
        return _erreur("Votre session a expiré. Reconnectez-vous.", 401)

    try:
        payload = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _erreur("Requête invalide.", 400)
    if not isinstance(payload, dict):
        return _erreur("Requête invalide.", 400)

    question = payload.get("question")
    if not isinstance(question, str) or not question.strip():
        return _erreur("Posez une question.", 400)
    question = question.strip()
    if len(question) > QUESTION_MAX:
        return _erreur("Question trop longue (1 000 caractères au maximum).", 400)

    conversation = None
    conversation_id = payload.get("conversation_id")
    if conversation_id not in (None, ""):
        try:
            conversation_id = int(conversation_id)
        except (TypeError, ValueError):
            return _erreur("Conversation invalide.", 400)
        conversation = Conversation.objects.filter(
            pk=conversation_id, proprietaire=request.user
        ).first()
        if conversation is None:
            return _erreur("Conversation introuvable.", 404)

    from assistant.services.chat import answer_question

    try:
        result = answer_question(question_avec_contexte(conversation, question))
    except ValueError as erreur:
        # Configuration Groq manquante, réponse illisible…
        return _erreur(str(erreur), 400)
    except Exception:
        # Erreur réseau ou API : message générique, détail dans la console.
        logger.exception("Échec de answer_question")
        return _erreur("Erreur technique lors de la recherche. Réessayez.", 500)

    with transaction.atomic():
        if conversation is None:
            conversation = Conversation.objects.create(
                proprietaire=request.user, titre=question[:80]
            )
        Message.objects.create(
            conversation=conversation, role=Message.Role.UTILISATEUR,
            contenu=question,
        )
        Message.objects.create(
            conversation=conversation, role=Message.Role.ASSISTANT,
            contenu=result["answer"], references=result["sources"],
            type_reponse=result["type"],
        )
        conversation.save(update_fields=["maj_le"])

    return JsonResponse({**result, "conversation_id": conversation.pk,
                         "titre": conversation.titre})
