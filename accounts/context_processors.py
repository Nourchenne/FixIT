from accounts.roles import est_technicien


def roles(request):
    """Rend « est_technicien » disponible dans tous les templates (menu)."""
    return {"est_technicien": est_technicien(getattr(request, "user", None))}
