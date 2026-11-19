import unittest
from unittest.mock import patch

import numpy as np
from qdrant_client import QdrantClient, models

from assistant.services import recherche_hybride
from documents.services import bm25, indexing_hybride
from evaluation import evaluate_retrieval

PASSAGES = [
    ("DOC001", "Activez le Wi-Fi dans les paramètres réseau de Windows."),
    ("DOC028", "Windows Update affiche l'erreur 0x80070005 : relancez la mise à jour."),
    ("DOC030", "Libérez de l'espace disque avec le nettoyage de stockage."),
]


def vecteur(i):
    """Vecteurs denses factices mais distincts (un axe par passage)."""
    v = np.zeros(4)
    v[i] = 1.0
    return v


class Bm25Tests(unittest.TestCase):
    def test_mots(self):
        self.assertEqual(bm25.mots("Les RÉSEAUX Wi-Fi de mon PC"),
                         ["reseau", "wi", "fi", "pc"])
        self.assertIn("0x80070005", bm25.mots("Erreur 0x80070005"))

    def test_indice_stable(self):
        self.assertEqual(bm25.indice("reseau"), 3454348472)  # identique d'un lancement à l'autre
        self.assertNotEqual(bm25.indice("reseau"), bm25.indice("wifi"))

    def test_poids_du_passage(self):
        indices, poids = bm25.vecteur_passage("disque disque plein", longueur_moyenne=3)
        par_mot = dict(zip(indices, poids))
        self.assertGreater(par_mot[bm25.indice("disque")], par_mot[bm25.indice("plein")])
        self.assertEqual(indices, sorted(indices))

    def test_question_sans_mot_utile(self):
        self.assertEqual(bm25.vecteur_question("et le la ?"), ([], []))


class RechercheHybrideTests(unittest.TestCase):
    def setUp(self):
        self.client = QdrantClient(":memory:")
        self.client.create_collection(
            "dense", vectors_config=models.VectorParams(
                size=4, distance=models.Distance.COSINE))
        self.client.upsert("dense", [
            models.PointStruct(id=i, vector=vecteur(i).tolist(), payload={
                "page_content": texte, "metadata": {"doc_id": doc, "page": 1}})
            for i, (doc, texte) in enumerate(PASSAGES)])
        self.info = indexing_hybride.construire(self.client, "dense")
        for cible, valeur in [("get_client", lambda: self.client),
                              ("collection_hybride", lambda: self.info["collection_name"])]:
            patcher = patch.object(recherche_hybride, cible, valeur)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_collection_construite(self):
        self.assertEqual(self.info["collection_name"], "dense_hybride")
        self.assertEqual(self.info["point_count"], 3)
        point = self.client.retrieve("dense_hybride", [1], with_vectors=True)[0]
        self.assertEqual(point.vector["dense"], vecteur(1).tolist())
        self.assertTrue(point.vector["bm25"].indices)

    def test_bm25_trouve_le_code_d_erreur(self):
        r = recherche_hybride.search_bm25("erreur 0x80070005", limit=3)
        self.assertEqual(r[0]["metadata"]["doc_id"], "DOC028")

    def test_bm25_question_vide_de_sens(self):
        self.assertEqual(recherche_hybride.search_bm25("et le la ?"), [])

    def test_hybride_fusionne_les_deux_classements(self):
        # Le dense préfère DOC030 ; BM25 trouve DOC028 grâce au code d'erreur.
        with patch.object(recherche_hybride, "embed_query", return_value=vecteur(2)):
            r = recherche_hybride.search_hybride("erreur 0x80070005", limit=3)
        docs = [p["metadata"]["doc_id"] for p in r]
        self.assertEqual(set(docs[:2]), {"DOC028", "DOC030"})

    def test_question_vide(self):
        with self.assertRaises(ValueError):
            recherche_hybride.search_hybride("  ")

    def test_choix_de_la_configuration(self):
        _, nom = evaluate_retrieval.choisir_recherche("bm25")
        self.assertEqual(nom, "bm25")
        retrieve, nom = evaluate_retrieval.choisir_recherche("hybride")
        self.assertEqual(nom, "hybride")
        with patch.object(recherche_hybride, "embed_query", return_value=vecteur(0)):
            self.assertEqual(len(retrieve("Wi-Fi réseau", 2)), 2)
