from django.contrib import admin

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ("role", "contenu", "cree_le")
    readonly_fields = ("cree_le",)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "proprietaire", "cree_le", "maj_le")
    search_fields = ("titre", "proprietaire__username")
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "role", "cree_le")
    list_filter = ("role",)
