"""Vecteurs creux BM25 pour la recherche hybride.

Même principe que le modèle "Qdrant/bm25" utilisé dans les labs 15 et 15bis
du cours : chaque texte devient un vecteur creux (un indice par mot, un poids
par mot), et Qdrant applique lui-même l'IDF grâce à `Modifier.IDF`.

La bibliothèque fastembed du cours n'est pas utilisée : elle exige
huggingface-hub < 2, alors que le projet dépend de huggingface-hub 2.x pour le
modèle d'embedding. Le calcul est donc fait ici, sans dépendance.

Poids d'un mot dans un passage (partie « fréquence » de BM25) :
    tf * (k1 + 1) / (tf + k1 * (1 - b + b * longueur / longueur_moyenne))
Côté question, chaque mot distinct a le poids 1.
"""

import re
import unicodedata
import zlib
from collections import Counter

K1 = 1.2
B = 0.75

# Mots trop fréquents pour aider à distinguer les passages.
MOTS_VIDES = set("""
a au aux avec ce ces cet cette dans de des du elle en est et il ils je la le
les leur lui ma mais me mes mon ne nous on ou par pas pour qu que qui sa se
ses son sur ta te tes ton tu un une vos votre vous y ete etre avoir fait plus
peut peuvent si sont comme tout tous toutes puis cela ca
an and are as at be by can do does for from has have how i if in into is it
its my no not of on or so than that the then there these this to was we what
when which why will with you your
""".split())


def normaliser(texte):
    """Minuscules et accents retirés : « Réseau » et « reseau » se rejoignent."""
    texte = unicodedata.normalize("NFKD", texte.lower())
    return "".join(c for c in texte if not unicodedata.combining(c))


def mots(texte):
    """Découper un texte en mots utiles (chiffres et codes d'erreur compris)."""
    resultat = []
    for mot in re.findall(r"[a-z0-9]+", normaliser(texte)):
        if len(mot) < 2 or mot in MOTS_VIDES:
            continue
        # Pluriel simple : « reseaux » -> « reseau », « drivers » -> « driver ».
        if len(mot) > 4 and mot.endswith(("s", "x")) and not mot.endswith("ss"):
            mot = mot[:-1]
        resultat.append(mot)
    return resultat


def indice(mot):
    """Indice stable d'un mot (le hash() de Python change à chaque lancement)."""
    return zlib.crc32(mot.encode("utf-8"))


def vecteur_passage(texte, longueur_moyenne):
    """Vecteur creux d'un passage : (indices, poids)."""
    liste = mots(texte)
    if not liste:
        return [], []
    frequences = Counter(liste)
    longueur = len(liste)
    norme = K1 * (1 - B + B * longueur / longueur_moyenne)
    poids = {}
    for mot, tf in frequences.items():
        poids[indice(mot)] = tf * (K1 + 1) / (tf + norme)
    indices = sorted(poids)
    return indices, [poids[i] for i in indices]


def vecteur_question(texte):
    """Vecteur creux d'une question : poids 1 par mot distinct."""
    indices = sorted({indice(m) for m in mots(texte)})
    return indices, [1.0] * len(indices)


def longueur_moyenne(textes):
    """Nombre moyen de mots utiles par passage."""
    longueurs = [len(mots(t)) for t in textes]
    return sum(longueurs) / len(longueurs) if longueurs else 1.0
