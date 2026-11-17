from django.conf import settings
from django.db import models


class Conversation(models.Model):
    """Fil de discussion d'un utilisateur avec l'assistant."""

    proprietaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    titre = models.CharField(max_length=200, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    maj_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "conversation"
        ordering = ["-maj_le"]

    def __str__(self):
        return self.titre or f"Conversation {self.pk}"


class Message(models.Model):
    """Message d'une conversation (question de l'utilisateur ou réponse FixIT)."""

    class Role(models.TextChoices):
        UTILISATEUR = "user", "Utilisateur"
        ASSISTANT = "assistant", "Assistant"

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    contenu = models.TextField()
    # Citations renvoyées par answer_question : liste de dicts
    # {ref, doc_id, titre, page, url}. Vide pour les messages utilisateur.
    references = models.JSONField(default=list, blank=True)
    # Type de réponse de FixIT : "etapes", "repli" ou "clarification".
    # Permet de relier la réponse de l'utilisateur à une clarification.
    type_reponse = models.CharField(max_length=20, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "message"
        # "id" départage deux messages créés dans la même milliseconde
        # (fréquent sous Windows, où l'horloge est peu précise).
        ordering = ["cree_le", "id"]

    def __str__(self):
        return f"[{self.get_role_display()}] {self.contenu[:40]}"
