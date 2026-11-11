from django.db import models


class Document(models.Model):
    """Guide de dépannage du corpus FixIT.

    Les champs reprennent les colonnes de data/sources.csv, pour pouvoir
    charger le registre existant dans la base. Les passages et leurs vecteurs
    restent dans Qdrant ; ce modèle décrit le document et son état d'indexation.
    """

    class Indexation(models.TextChoices):
        A_INDEXER = "a_indexer", "À indexer"
        INDEXE = "indexe", "Indexé"
        RETIRE = "retire", "Retiré"

    doc_id = models.CharField("identifiant", max_length=20, unique=True)
    titre = models.CharField(max_length=300)
    fichier = models.CharField("nom du PDF", max_length=255)
    url_source = models.URLField("URL source", max_length=500)
    source = models.CharField(max_length=120, blank=True)
    type_doc = models.CharField("type de document", max_length=60, blank=True)
    categorie = models.CharField(max_length=60, blank=True)
    systeme = models.CharField(max_length=120, blank=True)
    marque = models.CharField(max_length=60, blank=True)
    modele = models.CharField(max_length=60, blank=True)
    version_connue = models.CharField(max_length=60, blank=True)
    cas_couverts = models.CharField(max_length=160, blank=True)
    date_collecte = models.DateField(null=True, blank=True)

    contenu_hash = models.CharField("empreinte du contenu", max_length=64, blank=True)
    revision = models.PositiveIntegerField(default=1)
    etat_indexation = models.CharField(
        max_length=20,
        choices=Indexation.choices,
        default=Indexation.A_INDEXER,
    )

    cree_le = models.DateTimeField(auto_now_add=True)
    maj_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "document"
        ordering = ["doc_id"]

    def __str__(self):
        return f"{self.doc_id} — {self.titre}"
