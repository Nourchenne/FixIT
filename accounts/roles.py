"""Rôles de FixIT, portés par les groupes Django.

- utilisateur : pose des questions et suit ses propres tickets ;
- technicien  : consulte tous les tickets, ajoute des notes, change les statuts ;
- administrateur : compte superutilisateur Django.
"""

GROUPE_UTILISATEUR = "utilisateur"
GROUPE_TECHNICIEN = "technicien"


def est_technicien(user):
    """Vrai pour un technicien ou un administrateur connecté."""
    if not getattr(user, "is_authenticated", False):
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=GROUPE_TECHNICIEN).exists()
