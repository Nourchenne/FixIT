from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.mes_tickets, name="liste"),
    path("technicien/", views.espace_technicien, name="technicien"),
    path("creer/", views.creer_depuis_chat, name="creer"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/traiter/", views.traiter, name="traiter"),
    path("<int:pk>/rouvrir/", views.rouvrir, name="rouvrir"),
]
