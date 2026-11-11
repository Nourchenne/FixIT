from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("doc_id", "titre", "categorie", "etat_indexation", "revision")
    list_filter = ("etat_indexation", "categorie", "source")
    search_fields = ("doc_id", "titre", "fichier", "cas_couverts")
    ordering = ("doc_id",)
