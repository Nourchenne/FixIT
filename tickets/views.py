import json
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from accounts.roles import est_technicien
from integrations.mcp_client import ErreurMCP, ServiceMCPIndisponible, appeler_outil

from . import services
from .models import Ticket


logger = logging.getLogger(__name__)

CHAMPS_CREATION = ("titre", "description", "essais", "categorie", "cle_creation")


def _liste(request, tous):
    statut = request.GET.get("statut") or ""
    recherche = request.GET.get("q", "").strip()
    try:
        tickets = services.lister_tickets(request.user, statut or None, tous=tous)
    except services.DonneesInvalides:
        statut = ""
        tickets = services.lister_tickets(request.user, None, tous=tous)
    if recherche:
        tickets = (tickets.filter(pk=int(recherche)) if recherche.isdigit()
                   else tickets.filter(titre__icontains=recherche))
    return render(request, "tickets/liste.html", {
        "tickets": tickets,
        "statut": statut,
        "recherche": recherche,
        "statuts": Ticket.Statut.choices,
        "espace_technicien": tous,
    })


@login_required
def mes_tickets(request):
    return _liste(request, tous=False)


@login_required
def espace_technicien(request):
    if not est_technicien(request.user):
        raise PermissionDenied
    return _liste(request, tous=True)


@login_required
def detail(request, pk):
    try:
        ticket = services.charger_ticket(request.user, pk)
    except services.TicketIntrouvable:
        raise Http404
    technicien = est_technicien(request.user)
    return render(request, "tickets/detail.html", {
        "ticket": ticket,
        "evenements": ticket.evenements.select_related("auteur").order_by("cree_le", "id"),
        "technicien": technicien,
        "transitions": services.transitions_possibles(ticket) if technicien else [],
        "peut_rouvrir": ticket.statut in (Ticket.Statut.RESOLU, Ticket.Statut.FERME),
    })


@login_required
@require_POST
def traiter(request, pk):
    """Technicien : changer le statut et/ou ajouter une note."""
    nouveau = request.POST.get("statut", "")
    note = request.POST.get("note", "")
    try:
        if nouveau:
            services.changer_statut(request.user, pk, nouveau, note)
        else:
            services.ajouter_note(request.user, pk, note)
        messages.success(request, "Ticket mis à jour.")
    except services.TicketIntrouvable:
        raise Http404
    except services.TicketErreur as erreur:
        messages.error(request, str(erreur))
    return redirect("tickets:detail", pk=pk)


@login_required
@require_POST
def rouvrir(request, pk):
    try:
        services.rouvrir(request.user, pk, request.POST.get("note", ""))
        messages.success(request, "Ticket rouvert.")
    except services.TicketIntrouvable:
        raise Http404
    except services.TicketErreur as erreur:
        messages.error(request, str(erreur))
    return redirect("tickets:detail", pk=pk)


@require_POST
def creer_depuis_chat(request):
    """Création confirmée par l'utilisateur dans le chat : passage par MCP."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Votre session a expiré. Reconnectez-vous."}, status=401)
    try:
        payload = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Requête invalide."}, status=400)
    if not isinstance(payload, dict):
        return JsonResponse({"error": "Requête invalide."}, status=400)

    arguments = {champ: payload.get(champ) or "" for champ in CHAMPS_CREATION}
    try:
        ticket = appeler_outil("create_ticket", arguments, request.user)
    except ServiceMCPIndisponible as erreur:
        return JsonResponse({"error": str(erreur)}, status=503)
    except ErreurMCP as erreur:
        return JsonResponse({"error": str(erreur)}, status=400)

    return JsonResponse({
        "id": ticket["id"],
        "statut": ticket["statut_libelle"],
        "cree": ticket["cree"],
        "url": reverse("tickets:detail", args=[ticket["id"]]),
    })
