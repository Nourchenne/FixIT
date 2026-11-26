"""Calcule l'empreinte d'un PDF pour détecter une nouvelle version."""
import hashlib


def hash_fichier(chemin_pdf):
    """Empreinte SHA-256 du contenu d'un PDF.

    Deux fichiers identiques donnent la même empreinte ; si le PDF d'un
    document est remplacé par une nouvelle version, l'empreinte change,
    ce qui permet à l'import de détecter la révision.
    """
    sha256 = hashlib.sha256()
    with open(chemin_pdf, "rb") as fichier:
        for bloc in iter(lambda: fichier.read(8192), b""):
            sha256.update(bloc)
    return sha256.hexdigest()
