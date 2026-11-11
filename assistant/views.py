import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST


def chat_page(request):
    """Afficher la page de chat."""
    return render(request, "assistant/chat.html")


@require_POST
def ask(request):
    """Recevoir une question, interroger FixIT, renvoyer réponse et sources.

    L'import du service est fait ici (pas au chargement du module) pour éviter
    de charger les modèles lourds au démarrage de Django.
    """
    try:
        payload = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Requête invalide."}, status=400)

    question = (payload.get("question") or "").strip()
    if not question:
        return JsonResponse({"error": "Pose une question."}, status=400)

    from assistant.services.chat import answer_question

    try:
        result = answer_question(question)
    except ValueError as erreur:
        # Question vide, configuration Groq manquante, réponse illisible…
        return JsonResponse({"error": str(erreur)}, status=400)
    except Exception:
        # Erreur réseau ou API : message générique, pas de détail technique.
        return JsonResponse(
            {"error": "Erreur technique lors de la recherche. Réessaie."},
            status=500,
        )

    return JsonResponse(result)
