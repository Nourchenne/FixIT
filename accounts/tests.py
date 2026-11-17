from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from accounts.roles import est_technicien


class ComptesDemoTests(TestCase):
    def test_groupes_et_comptes(self):
        call_command("creer_comptes_demo", mot_de_passe="Demo-FixIT-2026")
        User = get_user_model()
        demo = User.objects.get(username="demo")
        tech = User.objects.get(username="technicien")
        self.assertTrue(demo.check_password("Demo-FixIT-2026"))
        self.assertFalse(est_technicien(demo))
        self.assertTrue(est_technicien(tech))
        self.assertEqual(set(Group.objects.values_list("name", flat=True)),
                         {"utilisateur", "technicien"})

    def test_commande_relancable(self):
        call_command("creer_comptes_demo", mot_de_passe="Demo-FixIT-2026")
        call_command("creer_comptes_demo", mot_de_passe="Autre-FixIT-2026")
        User = get_user_model()
        self.assertEqual(User.objects.count(), 3)
        self.assertTrue(User.objects.get(username="demo").check_password("Autre-FixIT-2026"))

    def test_mot_de_passe_trop_court(self):
        with self.assertRaises(CommandError):
            call_command("creer_comptes_demo", mot_de_passe="court")

    def test_roles_particuliers(self):
        admin = get_user_model().objects.create_superuser("admin", password="Admin-FixIT-2026")
        self.assertTrue(est_technicien(admin))
        self.assertFalse(est_technicien(AnonymousUser()))
