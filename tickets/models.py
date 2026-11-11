from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """Demande de support créée depuis le chat et suivie par un technicien."""

    class Statut(models.TextChoices):
        OUVERT = "ouvert", "Ouvert"
        EN_COURS = "en_cours", "En cours"
        RESOLU = "resolu", "Résolu"
        FERME = "ferme", "Fermé"

    class Categorie(models.TextChoices):
        WIFI = "wifi", "Wi-Fi / réseau"
        PERFORMANCE = "performance", "Performance"
        APPLICATIONS = "applications", "Applications"
        STOCKAGE = "stockage", "Stockage"
        PERIPHERIQUES = "peripheriques", "Périphériques"
        AUTRE = "autre", "Autre"

    proprietaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    titre = models.CharField(max_length=200)
    description = models.TextField()
    essais = models.TextField("étapes déjà essayées", blank=True)
    categorie = models.CharField(
        max_length=20, choices=Categorie.choices, default=Categorie.AUTRE
    )
    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.OUVERT
    )
    technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets_affectes",
    )
    # Clé d'idempotence : empêche de créer deux fois le même ticket si la
    # demande est renvoyée (voir cahier des charges, §6.4).
    cle_creation = models.CharField(max_length=64, unique=True)

    cree_le = models.DateTimeField(auto_now_add=True)
    maj_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ticket"
        ordering = ["-cree_le"]

    def __str__(self):
        return f"#{self.pk} {self.titre} [{self.get_statut_display()}]"


class TicketEvent(models.Model):
    """Historique d'un ticket : note du technicien et changement de statut."""

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="evenements",
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    note = models.TextField(blank=True)
    ancien_statut = models.CharField(max_length=20, blank=True)
    nouveau_statut = models.CharField(max_length=20, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "événement de ticket"
        ordering = ["cree_le"]

    def __str__(self):
        return f"Ticket {self.ticket_id} : {self.ancien_statut} → {self.nouveau_statut}"
