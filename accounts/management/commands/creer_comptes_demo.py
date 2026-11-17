from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError

from accounts.roles import GROUPE_TECHNICIEN, GROUPE_UTILISATEUR


COMPTES = [
    ("demo", GROUPE_UTILISATEUR),
    ("demo2", GROUPE_UTILISATEUR),  # second utilisateur : vérifier l'isolement
    ("technicien", GROUPE_TECHNICIEN),
]


class Command(BaseCommand):
    help = "Créer les groupes et les comptes de démonstration de FixIT."

    def add_arguments(self, parser):
        parser.add_argument(
            "--mot-de-passe", required=True, dest="mot_de_passe",
            help="Mot de passe commun aux comptes de démonstration.",
        )

    def handle(self, *args, mot_de_passe, **options):
        if len(mot_de_passe) < 8:
            raise CommandError("Le mot de passe doit contenir au moins 8 caractères.")

        User = get_user_model()
        for nom_groupe in (GROUPE_UTILISATEUR, GROUPE_TECHNICIEN):
            Group.objects.get_or_create(name=nom_groupe)

        for identifiant, nom_groupe in COMPTES:
            user, cree = User.objects.get_or_create(username=identifiant)
            user.set_password(mot_de_passe)  # mot de passe haché par Django
            user.save()
            user.groups.add(Group.objects.get(name=nom_groupe))
            etat = "créé" if cree else "mis à jour"
            self.stdout.write(f"Compte {identifiant} ({nom_groupe}) {etat}.")
