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

## Qualité des réponses : grille, notes des juges et comparaison avant/après corrections

Cette section complète l'évaluation Ragas ci-dessus par une grille lisible, une
ligne par question, notée par deux modèles « juges ».

### Cadre de mesure

- **Mesure du 27 novembre 2026** : les 50 questions du jeu final sont posées à
  `answer_question` avec le chat de `main` après les corrections de langue, de
  réinitialisation et de fuseau, la recherche hybride, la gestion documentaire,
  le filtrage par marque et l'évaluation Ragas. Générateur :
  `openai/gpt-oss-20b`, recherche dense, Qdrant. Script :
  `python -m evaluation.evaluate_grille`. Résultats :
  `evaluation/results/grille_20261127_133603.csv` et `.json`.
- **Mesure du 19 novembre 2026**, conservée pour comparaison : même jeu de
  questions, chat à la fin de l'étape 4, donc avant le filtrage par marque et
  les corrections de langue. Résultats : `evaluation/results/grille_20261119_153419.csv`.
  La question F027, qui avait échoué sur une coupure de connexion vers Groq
  (`APIConnectionError`), a été relancée seule ; sa ligne remplace la ligne en
  erreur.
- Contrôles automatiques : langue de la réponse comparée à celle de la question ;
  au moins un guide attendu cité (questions répondables) ; repli sans source
  (questions hors corpus).

### Résultats automatiques

| Mesure | 19 novembre | 27 novembre |
|---|---|---|
| Questions traitées | 50, erreurs : 0 | 50, erreurs : 0 |
| Langue correcte | 92 % (46/50) | **100 %** (50/50) |
| Répondables citant un guide attendu | 77,5 % (31/40) | 72,5 % (29/40) |
| Répondables sans étapes (repli ou clarification) | 3/40 | 5/40 (F005, F017, F022, F030, F038) |
| Hors corpus avec repli correct | 100 % (10/10) | 100 % (10/10) |
| Durée médiane / maximale | 9,6 s / 49 s | 9,5 s / 31,6 s |

### Lecture

- **Langue.** Les quatre réponses en français à une question anglaise du 19
  novembre (F026, F032, F036, F038) ont disparu : la correction fonctionne.
- **Hors corpus.** Les 10 questions hors corpus reçoivent le message de repli,
  sans source et sans procédure inventée, aux deux dates.
- **Qualité des réponses répondables : en baisse entre les deux mesures** (voir
  les notes ci-dessous). Les repli passent de 2 à 4 et les réponses appuyées sur
  trois sources de 17 à 6.
- **Filtrage par marque.** Aucune réponse du 27 novembre ne cite un guide de
  marque (Dell, Acer, ASUS, Lenovo, HP), contre 13 le 19 novembre : le filtre
  agit comme prévu. Les 19 questions dont un guide attendu est propre à une marque
  baissent un peu plus (−0,24, moyenne des deux juges) que les 21 autres
  (−0,14). L'écart est faible et l'échantillon petit : ce n'est pas une preuve.
  Les cas les plus nets sont F005 et F008, dont le seul guide pertinent est
  celui d'Acer (DOC029) : F005 reçoit un repli, F008 une réponse tirée d'un autre
  guide. Hypothèse, non vérifiée : le filtre écarte un guide de marque même
  quand il est la seule source utile.
- **Cause non isolée.** Les deux mesures diffèrent par plusieurs changements du
  chat à la fois (langue, réinitialisation, filtrage, passages envoyés au
  modèle). Seul un test qui n'active qu'un changement à la fois permettrait
  d'attribuer la baisse. Le chat varie aussi légèrement d'un lancement à l'autre.

### Notation des 40 réponses répondables (0, 1, 2) : automatique, non vérifiée par un humain

**Méthode.** Chaque réponse est notée avec le barème du cahier des charges par
deux modèles « juges » (`python -m evaluation.juge_llm`). Le juge reçoit la
question, les guides attendus, les extraits lus par FixIT, la réponse et le
barème, puis renvoie une note et une raison. Température 0, sortie JSON. Depuis
le 27 novembre, le juge reçoit **la même sélection de passages que le chat**
(10 candidats, filtre par marque, 3 passages) ; le 19 novembre, le chat envoyait
simplement les trois premiers passages de la recherche, que le juge recevait
aussi.

| Note | Signification |
|---|---|
| 2 | Correcte et complète : les étapes traitent le problème posé et sont justifiées par les sources citées |
| 1 | Partielle : utile mais incomplète, ou une étape hors sujet, ou une source mal choisie |
| 0 | Incorrecte : mauvais problème, procédure inventée, ou repli alors que le guide existe |

- Juge 1 : `qwen/qwen3.8-27b`, d'une autre famille que le générateur
  (`openai/gpt-oss-20b`), pour limiter le biais en faveur de ses propres réponses.
- Juge 2 : `openai/gpt-oss-120b`, de la même famille que le générateur, ajouté
  pour mesurer l'accord entre deux juges.
- Colonnes du CSV : `note_auto_llm`, `raison_auto_llm`, `modele_juge` (juge 1) et
  les mêmes avec le suffixe `_2` (juge 2).

**La colonne `note_0_1_2`, réservée à une notation humaine, est vide : aucune
relecture humaine n'a encore été consignée dans ce fichier.** Les résultats
ci-dessous sont des mesures automatiques ; leur validité n'a pas été contrôlée par
un humain.

**Résultats.**

| Mesure | 19 nov., Qwen | 19 nov., gpt-oss-120b | 27 nov., Qwen | 27 nov., gpt-oss-120b |
|---|---|---|---|---|
| Notes 0 / 1 / 2 | 5 / 18 / 17 | 5 / 13 / 22 | 8 / 19 / 13 | 8 / 15 / 17 |
| Note moyenne | 1,30 | 1,43 | 1,12 | 1,23 |
| Réponses notées 2 | 42,5 % | 55 % | 32,5 % | 42,5 % |

- **Accord entre les deux juges (27 novembre)** : même note sur 30 réponses sur
  40 (75 %), écart d'un point au plus sur les 40, aucune opposition 0 contre 2,
  kappa pondéré 0,69. Les 8 notes 0 sont identiques chez les deux juges : F001,
  F002, F005, F007, F017, F022, F030, F038.
- **Les 10 désaccords** (F014, F015, F018, F021, F027, F031, F032, F034, F036,
  F040) sont tous d'un point ; le juge 2, de la même famille que le générateur,
  donne une note plus haute dans 7 cas sur 10.
- **Évolution entre les deux mesures.** Juge 1 : 26 notes stables, 4 en hausse,
  10 en baisse. Juge 2 : 21 stables, 6 en hausse, 13 en baisse. Par thème (moyenne
  des deux juges) : NET02 passe de 1,88 à 1,00, PC02 de 1,00 à 0,50, PER03 de
  1,50 à 1,12, PC01 de 0,75 à 0,50 ; NET01 reste stable (1,75 à 1,88).
- **Objectif interne non atteint.** L'objectif « au moins 80 % de réponses notées
  2 » est loin d'être atteint (32,5 % à 42,5 % le 27 novembre).

**Exemples commentés (27 novembre).**

- **F001** (« Windows met très longtemps à démarrer le matin. »), note 0 aux deux
  dates et chez les deux juges : les étapes portent sur Windows Update et le
  cache ; elles sont fidèles aux passages lus, mais les guides attendus sur les
  applications au démarrage n'ont pas été fournis au modèle. Défaut de
  recherche, pas de rédaction.
- **F005** (« Word ne répond plus et je n'arrive pas à le fermer. »), de 1 et 1 à
  0 et 0 : FixIT répond par un repli alors que le guide d'Acer (DOC029) donne la
  procédure ; ce guide est écarté par le filtre par marque.
- **F030** (« I select my Wi-Fi network but it won't connect. »), de 2 et 2 à 0 et
  0 : repli alors que les extraits contiennent des solutions concrètes.
- **F013** (« Le son de mon casque ne marche pas sur Windows. »), de 2 et 2 à 1 et
  1 : les étapes sont pertinentes, mais l'une est attribuée à un extrait qui ne la
  contient pas (une citation mal choisie).

**Limites de cette mesure.**

- Aucune notation humaine : un juge automatique peut se tromper, être trop
  indulgent ou trop sévère, et un accord entre deux juges n'est pas une preuve
  de justesse. Une aide à la lecture (réponse, guides attendus, extraits lus) est
  fournie dans `evaluation/results/aide_notation_20261127.md`.
- Les juges lisent les extraits récupérés de nouveau par la recherche (déterministe),
  et non une copie enregistrée au moment de la génération.
- Les notes d'un même modèle, et les réponses du chat, peuvent varier légèrement
  d'un lancement à l'autre.
- Les deux mesures ne sont comparables qu'avec prudence : le chat a changé, et la
  sélection de passages lue par le juge a été alignée sur celle du chat entre les
  deux dates.

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

python -m evaluation.evaluate_grille
python -m evaluation.juge_llm
python -m evaluation.juge_llm --modele openai/gpt-oss-120b --suffixe _2
```

La première commande n'est nécessaire qu'une fois (ou après une réindexation).
Les scores affichés pour l'hybride sont des scores RRF : ils ne se comparent pas
aux scores cosinus du dense, seul le classement se compare.

`evaluate_generation.py` demande `GROQ_API_KEY` dans `.env` et consomme du
quota Groq à chaque question (génération + jugement) ; augmenter `--n`
jusqu'à 40 donne une mesure plus large mais prend plus longtemps sur le
compte gratuit.
