# Benchmark de la recherche documentaire — FixIT

Ce dossier mesure la qualité de la **recherche** (retrieval) de FixIT : quand on
pose une question de dépannage, est-ce que le bon guide ressort dans les premiers
résultats ? C'est un livrable du cahier des charges (§8) et c'est aussi ce qui
permet de **justifier ou non** l'ajout du reranking et de la recherche hybride :
on mesure d'abord la recherche dense actuelle, puis on compare.

## Fichiers

- `questions.jsonl` — jeu de questions annoté. Un objet JSON par ligne :
  `query_id`, `lang` (`fr`/`en`), `cas` (ex. `NET01`, ou `HORS` hors corpus),
  `question`, `gold_doc_ids` (les guides attendus), `answerable` (true/false).
  30 questions répondables couvrant les 10 cas, dans les deux langues, + 8
  questions hors corpus.
- `evaluate_retrieval.py` — interroge la collection Qdrant active (via
  `assistant.services.retrieval.search_documents`) et calcule les métriques.
- `results/` — résultats horodatés (un `.json` par exécution).

## Définitions des métriques

La pertinence est jugée au **niveau document** : un passage compte comme
pertinent si son `doc_id` fait partie des `gold_doc_ids` de la question.
Autrement dit, retrouver **l'un** des guides attendus suffit à répondre — ce qui
correspond au besoin réel d'un assistant de dépannage (trouver le bon guide), et
reste robuste à annoter.

- **Recall@k** — proportion de questions répondables pour lesquelles au moins un
  passage pertinent apparaît dans les `k` premiers résultats (hit-rate@k).
  Calculé pour k = 5 et k = 10.
- **MRR@10** — moyenne de `1/rang` du premier passage pertinent (0 s'il n'est pas
  dans les 10 premiers). Récompense le fait de placer le bon guide **en tête**.
- Les questions **hors corpus** sont exclues de Recall/MRR (le cahier demande la
  moyenne sur les questions répondables). On y mesure le score du meilleur
  passage, pour vérifier qu'il reste globalement plus bas que sur les questions
  répondables (séparation utile pour le message de repli du chat).

## Pré-requis

1. Docker Desktop lancé et le conteneur Qdrant démarré (`docker start fixit-qdrant`).
2. La collection indexée (`data/processed/vector_index.json` présent et à jour).
   Vérification rapide, qui doit retrouver DOC001 en tête :
   ```powershell
   python -m assistant.services.retrieval "Mon ordinateur ne trouve aucun réseau Wi-Fi."
   ```
3. Le `.venv` du projet activé.

> Aucune clé Groq n'est nécessaire : ce benchmark évalue **la recherche**, pas la
> génération. Le modèle d'embeddings se charge tout seul au premier appel.

## Lancer

Depuis la racine du dépôt (là où se trouve `manage.py`) :

```powershell
python -m evaluation.evaluate_retrieval
```

Options :
- `--limit 10` — nombre de passages récupérés par question (défaut 10 ; doit être
  ≥ 10 pour que Recall@10 ait un sens).
- `--questions chemin.jsonl` — utiliser un autre jeu de questions.

Le script affiche un résumé (Recall@5, Recall@10, MRR@10 ; détail par langue et
par cas ; questions ratées) et enregistre le détail complet dans
`results/retrieval_<horodatage>.json`.

## Comment lire les résultats

- **MRR@10 proche de 1** → le bon guide sort presque toujours en 1re position.
- **Recall@10 nettement > Recall@5** → le bon guide existe mais est mal classé :
  c'est exactement ce qu'un **reranking** corrige (on récupère large, on
  reclasse). Un gain confirmé ici justifierait de l'ajouter.
- **Écart fr vs en** → si l'anglais score moins bien (cf. cas B de
  `docs/validation_chat.md`), c'est un argument chiffré pour tester la recherche
  hybride / le reranking multilingue.
- **Cas faibles** (un `cas` avec Recall bas) → soit le corpus manque d'un guide,
  soit les questions de ce cas sont mal formulées.

Les questions hors corpus doivent idéalement avoir un top-score moyen plus bas
que les répondables : c'est ce qui permet au chat de répondre « les guides ne
suffisent pas » plutôt que d'inventer.

## Étendre le jeu (vers le jeu final du cahier)

Le cahier vise au moins 50 questions de test final (≈ 40 répondables + 10 hors
corpus), annotées et relues par l'autre membre du groupe. Ce fichier est un jeu
de développement : ajouter des lignes au même format, en gardant l'équilibre
fr/en et la couverture des 10 cas. **Figer** le jeu avant la mesure finale et ne
jamais ajuster le système sur ce jeu.
