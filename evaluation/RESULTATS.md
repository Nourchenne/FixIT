# Résultats du benchmark de recherche — FixIT

## Cadre de mesure

- Collection Qdrant : `fixit_19660c98de13ccc0` — 46 PDF, 400 passages, embeddings
  `multilingual-e5-small` (384 dimensions, similarité cosinus).
- Jeu de test final : `evaluation/questions_final.jsonl` — 50 questions : 40
  répondables couvrant les 10 cas (25 questions en français, 25 en anglais au
  total) et 10 questions hors corpus.
- Pertinence jugée au niveau document : un passage compte comme pertinent si
  son `doc_id` fait partie des guides attendus de la question.
  - Recall@k : part des questions répondables ayant au moins un guide attendu
    dans les k premiers résultats.
  - MRR@10 : moyenne de 1/rang du premier guide attendu (0 s'il est absent des
    10 premiers).
- 10 passages récupérés par question, pour toutes les configurations.

## Configurations comparées

| Configuration | Principe |
|---|---|
| Dense | Recherche sémantique : la question et les passages sont comparés par leurs embeddings `e5`. C'est la recherche utilisée par le chat. |
| BM25 | Recherche par mots-clés : un passage est bien classé s'il contient les mots de la question, surtout les mots rares dans le corpus. |
| Hybride | Dense et BM25 lancés ensemble, puis classements fusionnés par Reciprocal Rank Fusion (RRF) : un passage bien placé par les deux méthodes remonte en tête. |
| Dense + reranking | Les 10 premiers passages denses sont reclassés par un cross-encoder multilingue (`mmarco-mMiniLMv2-L12`). |
| Hybride + reranking | Même reranking, appliqué aux 10 premiers passages de l'hybride. |

Mise en œuvre :

- BM25 et hybride (technique des labs 15 et 15bis du cours) : les vecteurs
  creux BM25 sont calculés par `documents/services/bm25.py` et stockés dans une
  seconde collection Qdrant, `fixit_19660c98de13ccc0_hybride`, construite par
  `documents.services.indexing_hybride`. Elle reprend à l'identique les
  vecteurs denses de la collection principale. Qdrant applique l'IDF et réalise
  la fusion RRF, comme `RetrievalMode.HYBRID` dans le lab 15bis. La
  bibliothèque fastembed du cours n'a pas pu être utilisée : elle exige
  huggingface-hub < 2, incompatible avec la version dont dépend le modèle
  d'embedding.
- Reranking (technique du lab 16 du cours) : `assistant/services/reranking.py`.

## Résultats

| Mesure | Dense | BM25 | Hybride | Dense + reranking | Hybride + reranking |
|---|---|---|---|---|---|
| Recall@5 | 0,850 | 0,750 | 0,825 | 0,875 | 0,825 |
| Recall@10 | 0,900 | 0,775 | 0,900 | 0,900 | 0,900 |
| MRR@10 | **0,741** | 0,546 | 0,721 | 0,708 | 0,693 |
| Échecs (sur 40) | 4 | 9 | 4 | 4 | 4 |

MRR@10 par langue :

| Langue | Dense | BM25 | Hybride | Dense + reranking | Hybride + reranking |
|---|---|---|---|---|---|
| Français | 0,716 | 0,617 | 0,701 | 0,733 | 0,726 |
| Anglais | 0,767 | 0,475 | 0,741 | 0,684 | 0,661 |

Mesures du 19 novembre 2026, détaillées question par question dans
`evaluation/results/retrieval_<configuration>_20261119_*.json`. La recherche
dense et le dense + reranking redonnent exactement les valeurs d'une première
série mesurée le 11 novembre : le benchmark est reproductible.

La recherche dense est parfaite sur les quatre cas réseau (NET01 à NET04 :
Recall@5 = 1,0). Les cas les plus faibles sont PC01 (Recall@5 = 0,50) et, à un
moindre degré, PC02, PC03 et PER02.

## Lecture

### BM25 seul

BM25 est nettement en dessous du dense (MRR@10 0,546 contre 0,741) et compte
plus du double d'échecs (9 contre 4). L'écart vient surtout de l'anglais
(MRR@10 0,475) : la plupart des guides sont en français, et une question
anglaise partage peu de mots avec eux. BM25 échoue aussi sur les formulations
familières, qui n'emploient pas le vocabulaire des guides (« takes forever to
boot », « touchpad stopped working »).

### Hybride

La fusion ne fait pas mieux que le dense : même Recall@10 (0,900), Recall@5 et
MRR@10 légèrement plus bas. Elle récupère F007 (« Une application plante dès
que je l'ouvre »), que le dense manquait, mais perd F001 (« Windows met très
longtemps à démarrer le matin »), que le dense trouvait. Le cas PC01 baisse
nettement (MRR@10 0,336 → 0,167) : sur ce cas, BM25 se trompe souvent (une
seule question sur quatre trouvée) et la fusion fait descendre les bons guides
que le dense plaçait en tête.

### Reranking

Après le dense, le reranking améliore légèrement le Recall@5 (+0,025, surtout
en français) mais dégrade le MRR@10 (−0,033), surtout en anglais (−0,083). Le
cross-encoder remonte parfois un bon guide dans le top 5, mais il déclasse plus
souvent le bon guide de la première position, y compris sur des cas que la
recherche dense traitait déjà parfaitement (NET01 : MRR@10 1,0 → 0,875 ;
PER03 : 0,619 → 0,232). Après l'hybride, il produit le même effet (MRR@10
0,721 → 0,693).

Explication probable : le cross-encoder `mmarco` est entraîné sur des passages
web (MS MARCO) et s'adapte mal à des guides de dépannage courts, en français et
en anglais mélangés. L'embedding `e5` multilingue est déjà bien aligné avec ce
corpus ; le reranking introduit du bruit là où la recherche dense était déjà
bonne.

Le reranking a aussi un coût : un modèle supplémentaire d'environ 470 Mo et un
temps nettement plus élevé (plusieurs minutes pour les 40 questions, contre
quelques secondes en dense, BM25 ou hybride).

### Échecs communs

F002, F012 et F017 échouent dans toutes les configurations. Le guide attendu
n'est pas parmi les candidats : aucun reclassement ne peut donc le récupérer.
Ce sont des écarts de vocabulaire ou de langue que ni le sens ni les mots-clés
ne comblent :

| Question | Guide attendu | Ce qui est trouvé à la place |
|---|---|---|
| F002 « My PC takes forever to boot up. » | DOC005, DOC004 (démarrage, performances) | DOC028 (Windows Update) et des guides Wi-Fi |
| F012 « My laptop warns there is not enough storage to update. » | DOC008, DOC009 (espace disque) | DOC028, Windows Update, attiré par le mot « update » |
| F017 « Personne ne m'entend pendant mes réunions en ligne. » | DOC011 (micro) | guides Wi-Fi et Windows Update : la question ne mentionne pas le micro |

## Décision

La configuration retenue est la **recherche dense seule**, qui obtient le
meilleur MRR@10 (0,741) avec le meilleur Recall@10 (0,900), sans modèle ni
index supplémentaires.

- BM25 seul est moins bon partout.
- L'hybride ne corrige aucun des trois échecs communs et échange un succès
  contre un autre (F007 gagné, F001 perdu) ; il ajoute une seconde collection à
  maintenir.
- Le reranking, après le dense comme après l'hybride, dégrade le MRR@10 et
  ralentit fortement la recherche.

Le code des autres configurations est conservé pour pouvoir refaire les
mesures : `documents/services/bm25.py`,
`documents/services/indexing_hybride.py`,
`assistant/services/recherche_hybride.py`,
`assistant/services/reranking.py`, et les options `--mode` et `--rerank` du
benchmark.

Piste d'amélioration pour les échecs restants : enrichir les métadonnées des
guides (mots-clés anglais, synonymes familiers) plutôt que changer de méthode
de recherche.

## Évaluation de la génération

Les mesures précédentes jugent uniquement la recherche (le bon guide est-il
retrouvé ?). Elles ne disent rien de la réponse elle-même : le modèle peut
retrouver le bon passage et quand même ajouter une étape qu'il n'y a pas lu.
`evaluation/evaluate_generation.py` complète donc le benchmark avec deux
mesures de la génération, jugées par Ragas et un modèle plus gros que celui
qui répond (`openai/gpt-oss-120b` contre `openai/gpt-oss-20b`) :

- **faithfulness** : chaque affirmation de la réponse est-elle appuyée par les
  passages réellement envoyés au modèle ? (détecte l'invention de détails) ;
- **answer_relevancy** : la réponse répond-elle à la question posée ?

`questions_final.jsonl` ne contient pas de réponse de référence rédigée à la
main (seulement des `gold_doc_ids`) : les métriques qui en ont besoin
(`context_recall`, `factual_correctness`) ne sont donc pas mesurées ici — le
Recall@k et le MRR@10 ci-dessus couvrent déjà, avec les `gold_doc_ids`, la
question « les bons passages sont-ils trouvés ? ».

### Résultats

Sur les 15 premières questions répondables de `questions_final.jsonl`
(pipeline complet : recherche dense, filtre par marque, génération réelle) :

| Mesure | Score moyen | Questions exploitables |
|---|---|---|
| faithfulness | 0,557 | 14 / 15 (un appel au juge a expiré, compte gratuit Groq) |
| answer_relevancy | 0,891 | 15 / 15 |

Détail par question : `evaluation/results/generation_20261126_220439.csv`.

### Lecture

`answer_relevancy` est solide : les réponses adressent bien la question
posée, dans les deux langues.

`faithfulness` est plus bas et c'est informatif plutôt qu'alarmant. Deux cas
distincts, à ne pas confondre :

- **F002 et F007 sont des échecs de recherche déjà connus** (section
  « Échecs communs » ci-dessus) : le bon guide n'est jamais retrouvé. F007
  reçoit donc le repli (« Les guides disponibles ne suffisent pas pour
  répondre »), ce qui est le comportement attendu — faithfulness vaut 0 sans
  que le modèle ait inventé quoi que ce soit. F002 a expiré côté juge avant
  d'avoir un score.
- **F001 et F003 sont des échecs de génération, pas de recherche** : le bon
  guide est bien retrouvé (F003 : Recall@5 = 1,0), mais la réponse ajoute des
  détails précis absents du passage cité — par exemple, pour F003 (« Le
  processeur de mon PC est constamment à 100 % »), l'étape 1 recommande une
  analyse Windows Defender que le passage [S1] ne mentionne pas forcément en
  ces termes. Le modèle complète avec des connaissances générales plutôt que
  de s'en tenir strictement au guide cité.

C'est le genre d'écart qu'aucune mesure de retrieval ne peut détecter : les
bons documents sont là, c'est la rédaction qui déborde du contenu fourni.

### Limites de cette mesure

- Échantillon de 15 questions sur 40 répondables (pas les 40 : chaque
  question coûte plusieurs appels Groq, et le compte gratuit limite les
  tokens par minute — voir `--n` dans la commande ci-dessous).
- Un appel a expiré pendant le jugement (TimeoutError, absorbé par le
  réessai intégré de Ragas pour les 29 autres, mais pas pour celui-là) :
  faithfulness n'a donc que 14 valeurs sur 15.
- Pas de mesure de factualité contre une réponse de référence (voir
  ci-dessus) : seule la fidélité aux passages fournis est vérifiée, pas
  l'exactitude technique absolue de chaque étape.

## Reproduire les mesures

Depuis la racine du dépôt, environnement activé et Qdrant démarré :

```
python -m documents.services.indexing_hybride
python -m evaluation.evaluate_retrieval --questions evaluation/questions_final.jsonl --mode dense
python -m evaluation.evaluate_retrieval --questions evaluation/questions_final.jsonl --mode bm25
python -m evaluation.evaluate_retrieval --questions evaluation/questions_final.jsonl --mode hybride
python -m evaluation.evaluate_retrieval --questions evaluation/questions_final.jsonl --mode dense --rerank --candidates 10
python -m evaluation.evaluate_retrieval --questions evaluation/questions_final.jsonl --mode hybride --rerank --candidates 10

python -m evaluation.evaluate_generation --n 15
```

La première commande n'est nécessaire qu'une fois (ou après une réindexation).
Les scores affichés pour l'hybride sont des scores RRF : ils ne se comparent pas
aux scores cosinus du dense, seul le classement se compare.

`evaluate_generation.py` demande `GROQ_API_KEY` dans `.env` et consomme du
quota Groq à chaque question (génération + jugement) ; augmenter `--n`
jusqu'à 40 donne une mesure plus large mais prend plus longtemps sur le
compte gratuit.
