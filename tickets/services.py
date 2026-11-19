"""Service métier des tickets.

Seule porte d'entrée pour créer, consulter et faire évoluer un ticket : les
vues Django et le serveur MCP l'utilisent tous les deux, et les droits sont
toujours vérifiés ici (cahier technique, §6.4).
"""

from django.db import IntegrityError, transaction

from accounts.roles import est_technicien

from .models import Ticket, TicketEvent


class TicketErreur(Exception):
    """Erreur métier dont le message peut être affiché à l'utilisateur."""


class TicketIntrouvable(TicketErreur):
    pass


class ActionRefusee(TicketErreur):
    pass


class DonneesInvalides(TicketErreur):
    pass


Statut = Ticket.Statut

# Cycle de vie : ouvert -> en cours -> résolu -> fermé ; un ticket résolu ou
# fermé peut être rouvert.
TRANSITIONS = {
    Statut.OUVERT: {Statut.EN_COURS},
    Statut.EN_COURS: {Statut.RESOLU},
    Statut.RESOLU: {Statut.FERME, Statut.OUVERT},
    Statut.FERME: {Statut.OUVERT},
}

LIBELLES_CHAMPS = {
    "titre": "titre", "description": "description", "essais": "essais",
    "cle_creation": "clé de création", "note": "note",
}


def _texte(donnees, cle, maximum, obligatoire=True):
    valeur = donnees.get(cle, "")
    nom = LIBELLES_CHAMPS.get(cle, cle)
    if valeur is None:
        valeur = ""
    if not isinstance(valeur, str):
        raise DonneesInvalides(f"Le champ « {nom} » doit être un texte.")
    valeur = valeur.strip()
    if obligatoire and not valeur:
        raise DonneesInvalides(f"Le champ « {nom} » est obligatoire.")
    if len(valeur) > maximum:
        raise DonneesInvalides(f"Le champ « {nom} » dépasse {maximum} caractères.")
    return valeur


def _exiger_utilisateur(actor):
    if not getattr(actor, "is_authenticated", False) or not actor.is_active:
        raise ActionRefusee("Utilisateur non authentifié.")


def serialiser(ticket, avec_evenements=False):
    """Représentation JSON d'un ticket (réponses MCP et API)."""
    donnees = {
        "id": ticket.pk,
        "titre": ticket.titre,
        "description": ticket.description,
        "essais": ticket.essais,
        "categorie": ticket.categorie,
        "categorie_libelle": ticket.get_categorie_display(),
        "statut": ticket.statut,
        "statut_libelle": ticket.get_statut_display(),
        "proprietaire": ticket.proprietaire.get_username(),
        "technicien": ticket.technicien.get_username() if ticket.technicien else None,
        "cree_le": ticket.cree_le.isoformat(),
        "maj_le": ticket.maj_le.isoformat(),
    }
    if avec_evenements:
        donnees["evenements"] = [
            {
                "auteur": e.auteur.get_username() if e.auteur else None,
                "note": e.note,
                "ancien_statut": e.ancien_statut,
                "nouveau_statut": e.nouveau_statut,
                "cree_le": e.cree_le.isoformat(),
            }
            for e in ticket.evenements.select_related("auteur").order_by("cree_le", "id")
        ]
    return donnees


def _reprise(ticket, actor):
    """Même clé de création : renvoyer le ticket déjà créé, sans doublon."""
    if ticket.proprietaire_id != actor.pk:
        raise DonneesInvalides("Cette clé de création est déjà utilisée.")
    return {**serialiser(ticket), "cree": False}


def create_ticket(actor, payload):
    """Créer un ticket pour actor. Renvoie le ticket et "cree" (False si la
    même demande avait déjà été enregistrée avec cette clé)."""
    _exiger_utilisateur(actor)
    if not isinstance(payload, dict):
        raise DonneesInvalides("Données de ticket invalides.")

    titre = _texte(payload, "titre", 200)
    description = _texte(payload, "description", 5000)
    essais = _texte(payload, "essais", 5000, obligatoire=False)
    cle = _texte(payload, "cle_creation", 64)
    if len(cle) < 8:
        raise DonneesInvalides("La clé de création doit contenir au moins 8 caractères.")
    categorie = payload.get("categorie") or Ticket.Categorie.AUTRE
    if categorie not in Ticket.Categorie.values:
        raise DonneesInvalides("Catégorie inconnue.")

    existant = Ticket.objects.filter(cle_creation=cle).first()
    if existant is not None:
        return _reprise(existant, actor)

    try:
        with transaction.atomic():
            ticket = Ticket.objects.create(
                proprietaire=actor, titre=titre, description=description,
                essais=essais, categorie=categorie, cle_creation=cle,
            )
            TicketEvent.objects.create(
                ticket=ticket, auteur=actor, note="Ticket créé depuis FixIT.",
                nouveau_statut=ticket.statut,
            )
    except IntegrityError:
        # Deux envois simultanés avec la même clé : le premier a été enregistré.
        return _reprise(Ticket.objects.get(cle_creation=cle), actor)

    return {**serialiser(ticket), "cree": True}


def charger_ticket(actor, ticket_id):
    """Ticket visible par actor (propriétaire ou technicien).

    Un ticket existant mais non autorisé est signalé « introuvable » pour ne
    pas révéler son existence.
    """
    _exiger_utilisateur(actor)
    try:
        ticket_id = int(ticket_id)
    except (TypeError, ValueError):
        raise TicketIntrouvable("Numéro de ticket invalide.")
    ticket = (Ticket.objects.select_related("proprietaire", "technicien")
              .filter(pk=ticket_id).first())
    if ticket is None or (ticket.proprietaire_id != actor.pk
                          and not est_technicien(actor)):
        raise TicketIntrouvable(f"Ticket {ticket_id} introuvable.")
    return ticket


def get_ticket(actor, ticket_id):
    """Statut et historique d'un ticket (utilisé par l'outil MCP)."""
    return serialiser(charger_ticket(actor, ticket_id), avec_evenements=True)


def lister_tickets(actor, statut=None, tous=False):
    """Tickets de actor, ou tous les tickets pour l'espace technicien."""
    _exiger_utilisateur(actor)
    tickets = Ticket.objects.select_related("proprietaire", "technicien")
    if tous:
        if not est_technicien(actor):
            raise ActionRefusee("Accès réservé aux techniciens.")
    else:
        tickets = tickets.filter(proprietaire=actor)
    if statut:
        if statut not in Statut.values:
            raise DonneesInvalides("Statut inconnu.")
        tickets = tickets.filter(statut=statut)
    return tickets


def transitions_possibles(ticket):
    """Statuts atteignables depuis le statut actuel, avec leur libellé."""
    return [(s.value, s.label) for s in Statut if s in TRANSITIONS.get(ticket.statut, ())]


def _changer(actor, ticket, nouveau, note):
    ancien = ticket.statut
    ticket.statut = nouveau
    if ticket.technicien_id is None and est_technicien(actor):
        ticket.technicien = actor
    ticket.save(update_fields=["statut", "technicien", "maj_le"])
    TicketEvent.objects.create(
        ticket=ticket, auteur=actor, note=note,
        ancien_statut=ancien, nouveau_statut=nouveau,
    )
    return ticket


def changer_statut(actor, ticket_id, nouveau_statut, note=""):
    """Technicien : faire avancer le ticket dans son cycle de vie."""
    if not est_technicien(actor):
        raise ActionRefusee("Seul un technicien peut changer le statut.")
    note = _texte({"note": note}, "note", 2000, obligatoire=False)
    with transaction.atomic():
        ticket = charger_ticket(actor, ticket_id)
        if nouveau_statut not in TRANSITIONS.get(ticket.statut, ()):
            raise ActionRefusee(
                f"Passage de « {ticket.get_statut_display()} » au statut demandé impossible."
            )
        return _changer(actor, ticket, nouveau_statut, note)


def ajouter_note(actor, ticket_id, note):
    """Technicien : ajouter une note sans changer le statut."""
    if not est_technicien(actor):
        raise ActionRefusee("Seul un technicien peut ajouter une note.")
    note = _texte({"note": note}, "note", 2000)
    ticket = charger_ticket(actor, ticket_id)
    TicketEvent.objects.create(ticket=ticket, auteur=actor, note=note)
    ticket.save(update_fields=["maj_le"])
    return ticket


def rouvrir(actor, ticket_id, note=""):
    """Propriétaire ou technicien : rouvrir un ticket résolu ou fermé."""
    note = _texte({"note": note}, "note", 2000, obligatoire=False)
    with transaction.atomic():
        ticket = charger_ticket(actor, ticket_id)
        if ticket.statut not in (Statut.RESOLU, Statut.FERME):
            raise ActionRefusee("Seul un ticket résolu ou fermé peut être rouvert.")
        return _changer(actor, ticket, Statut.OUVERT, note or "Ticket rouvert.")
