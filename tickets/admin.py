from django.contrib import admin

from .models import Ticket, TicketEvent


class TicketEventInline(admin.TabularInline):
    model = TicketEvent
    extra = 0
    fields = ("auteur", "note", "ancien_statut", "nouveau_statut", "cree_le")
    readonly_fields = ("cree_le",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "titre", "proprietaire", "categorie", "statut", "technicien", "cree_le")
    list_filter = ("statut", "categorie")
    search_fields = ("titre", "description", "proprietaire__username")
    inlines = [TicketEventInline]


@admin.register(TicketEvent)
class TicketEventAdmin(admin.ModelAdmin):
    list_display = ("ticket", "auteur", "ancien_statut", "nouveau_statut", "cree_le")
    list_filter = ("nouveau_statut",)
