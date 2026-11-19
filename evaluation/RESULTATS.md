# Résultats du benchmark de recherche — FixIT

## Cadre de mesure

- Collection Qdrant : `fixit_19660c98de13ccc0` — 46 PDF, 400 passages, embeddings
  `multilingual-e5-small` (384 dimensions, similarité cosinus).
- Jeu de test final : `evaluation/questions_final.jsonl` — 50 questions : 40
  répondables couvrant les 10 cas (25 en français, 25 en anglais) et 10
  questions hors corpus.
- Pertinence jugée au niveau document : un passage compte comme pertinent si
  son `doc_id` fait partie des guides attendus de la question.
  - Recall@k : part des questions répondables ayant au moins un guide attendu
    dans les k premiers résultats.
  - MRR@10 : moyenne de 1/rang du premier guide attendu (0 s'il est absent des
    10 premiers).
- Deux configurations comparées sur le même jeu : recherche dense seule, puis
  dense suivie d'un reranking par cross-encoder (`mmarco-mMiniLMv2-L12`, 10
  candidats reclassés).

## Résultats

| Mesure | Dense | Dense + reranking |
|---|---|---|
| Recall@5 | 0,850 | 0,875 |
| Recall@10 | 0,900 | 0,900 |
| MRR@10 | 0,741 | 0,708 |

MRR@10 par langue : français 0,716 → 0,733 ; anglais 0,767 → 0,684.

La recherche dense est parfaite sur les quatre cas réseau (NET01 à NET04 :
Recall@5 = 1,0). Les cas les plus faibles sont PC01 (Recall@5 = 0,50) et, à un
moindre degré, PC02, PC03 et PER02.

## Lecture

Le reranking améliore légèrement le Recall@5 (+0,025, surtout en français) mais
dégrade le MRR@10 (−0,033), surtout en anglais (−0,083). Le cross-encoder
remonte parfois un bon guide dans le top-5, mais il déclasse plus souvent le bon
guide de la première position — y compris sur des cas que la recherche dense
traitait déjà parfaitement (NET01 : MRR 1,0 → 0,875 ; PER03 : 0,619 → 0,232).

Les quatre échecs de la recherche dense (F002, F007, F012, F017) restent des
échecs après reranking : le guide attendu n'est pas dans les candidats, donc le
reranking ne peut pas le récupérer. Ce sont des trous de rappel (vocabulaire
familier ou question anglaise face à un guide français), pas des problèmes de
classement. Exemple : F012 « not enough storage to update » fait remonter le
guide Windows Update (DOC028) à cause du mot « update ».

Le reranking ajoute aussi un coût : un modèle supplémentaire d'environ 470 Mo et
un temps de réponse nettement plus élevé (plusieurs minutes pour les 40
questions, contre quelques secondes en dense).

Explication probable : le cross-encoder `mmarco` est entraîné sur des passages
web (MS MARCO) et s'adapte mal à des guides de dépannage courts, en français et
en anglais mélangés. L'embedding `e5` multilingue est déjà bien aligné avec ce
corpus ; le reranking introduit du bruit là où la recherche dense était déjà
bonne.

## Décision

La configuration retenue est la **recherche dense seule**. Le reranking a été
testé (technique du lab 16 du cours) et mesuré : il n'apporte pas de gain net
sur ce corpus et coûte en temps de réponse et en dépendance. Le code
(`assistant/services/reranking.py` et le mode `--rerank` du benchmark) est
conservé pour la traçabilité de l'expérience.

Note méthodologique : le reranking a reclassé les 10 premiers candidats denses.
Un vivier plus large (20) pourrait récupérer quelques documents au-delà du rang
10, mais au vu de la dégradation du MRR et du fait que les guides manquants ne
figurent pas parmi les premiers candidats denses, la conclusion ne change pas.

La recherche hybride (BM25) n'a pas été retenue non plus : les quatre échecs
sont des écarts de vocabulaire ou cross-lingues, que la correspondance par
mots-clés ne corrige pas de façon fiable.

## Qualité des réponses (génération)

### Cadre de mesure

- Les 50 questions du jeu final sont posées à `answer_question` (Qdrant et Groq
  `openai/gpt-oss-20b`), avec la recherche dense retenue ci-dessus, le 19
  novembre 2026. Script : `python -m evaluation.evaluate_generation`.
- Résultats par question : `evaluation/results/generation_20261119_153419.csv`
  (et sa synthèse `.json`).
- Une question (F027) a d'abord échoué sur une coupure de connexion vers Groq
  (`APIConnectionError`). Elle a été relancée seule et sa ligne remplace la
  ligne en erreur ; aucune autre ligne n'a été modifiée.
- Contrôles automatiques : langue de la réponse comparée à celle de la
  question ; au moins un guide attendu cité (questions répondables) ; repli sans
  source (questions hors corpus).

### Résultats automatiques

| Mesure | Résultat |
|---|---|
| Questions traitées | 50, erreurs : 0 |
| Langue correcte | 92 % (46 sur 50) |
| Répondables citant un guide attendu | 77,5 % (31 sur 40) |
| Répondables sans étapes (repli ou clarification) | 3 sur 40 |
| Hors corpus avec repli correct | 100 % (10 sur 10) |
| Durée médiane / maximale | 9,6 s / 49 s |

### Lecture

- **Hors corpus.** Les 10 questions hors corpus reçoivent le message de repli,
  sans source et sans procédure inventée : l'objectif interne (au moins 8 sur
  10) est atteint.
- **Langue.** Les 4 réponses en français à une question anglaise (F026, F032,
  F036, F038) concernent toutes le Wi-Fi. La règle « réponds dans la langue de la
  question » n'est donc pas respectée sur ce thème ; la consigne est à revoir.
- **Guides attendus.** 9 questions répondables ne citent aucun guide attendu.
  Quatre sont les échecs de rappel déjà identifiés plus haut (F002, F007, F012,
  F017) ; les cinq autres (F001, F004, F010, F011, F022) montrent que, même
  quand le bon guide figure dans les candidats, les passages proposés au modèle
  peuvent porter sur un autre sujet. Exemple : F001 (« Windows met très
  longtemps à démarrer ») reçoit des étapes sur le cache du Microsoft Store et
  Windows Update, fidèles aux passages lus mais hors sujet.
- **Sans étapes.** F007 et F022 reçoivent un repli et F017 une clarification
  alors que leur guide existe.
- **Temps de réponse.** La médiane (9,6 s) est bien supérieure à celle d'un
  essai à 5 questions (environ 1 s) : la latence de Groq varie fortement
  (6 questions au-dessus de 20 s). La mesure dépend du réseau et du moment.
- **Limite connue.** Un guide propre à une marque (SupportAssist de Dell) est
  proposé sans savoir si l'appareil correspond (filtrage par appareil non
  réalisé).

### Notation des 40 réponses répondables (0, 1, 2) : automatique, non vérifiée par un humain

**Méthode.** Chaque réponse est notée avec le barème du cahier des charges par
deux modèles « juges » (`python -m evaluation.juge_llm`). Le juge reçoit la
question, les guides attendus, les extraits lus par FixIT, la réponse et le
barème, puis renvoie une note et une raison. Température 0, sortie JSON.

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
relecture humaine n'a été faite.** Les résultats ci-dessous sont des mesures
automatiques ; leur validité n'a pas été contrôlée par un humain.

**Résultats.**

| Mesure | Juge 1 (Qwen) | Juge 2 (gpt-oss-120b) |
|---|---|---|
| Notes 0 / 1 / 2 | 5 / 18 / 17 | 5 / 13 / 22 |
| Note moyenne | 1,30 | 1,43 |
| Réponses notées 2 | 42,5 % (17/40) | 55 % (22/40) |

- **Accord entre les deux juges** : même note sur 33 réponses sur 40 (82,5 %),
  écart d'un point au plus sur les 40, aucune opposition 0 contre 2, kappa
  pondéré 0,76. Les 5 notes 0 sont identiques chez les deux juges : F001, F002,
  F007, F017, F022.
- **Les 7 désaccords** (F003, F004, F011, F014, F016, F029, F039) sont tous
  d'un point ; dans 6 cas sur 7, le juge 2 est plus indulgent (note plus haute).
  Le juge 2, de la même famille que le générateur, est le moins sévère.
- **Objectif interne non atteint.** L'objectif « au moins 80 % de réponses notées
  2 » est loin d'être atteint (42,5 % à 55 %). Les réponses sont en majorité
  utiles mais partielles ou avec une étape hors sujet.

**Exemples commentés.**

- **F001** (« Windows met très longtemps à démarrer le matin. »), note 0 chez les
  deux juges : les étapes portent sur le cache du Microsoft Store et Windows
  Update ; elles sont fidèles aux passages lus, mais les guides attendus sur les
  applications au démarrage et les performances n'ont pas été fournis au modèle.
  C'est un défaut de recherche, pas de rédaction.
- **F022** (« My touchpad stopped working on my laptop. »), note 0 chez les deux
  juges : FixIT répond par un repli alors que des guides sur le pavé tactile
  existent. De même F007 (repli) et F017 (clarification inutile).
- **F013** (« Le son de mon casque ne marche pas sur Windows. »), note 2 chez les
  deux juges : étapes pertinentes, présentes dans les extraits cités.
- **F003** (« Le processeur de mon PC est constamment à 100 %. »), désaccord : le
  juge 1 donne 1 (omet des solutions du guide attendu et s'appuie sur un guide
  hors sujet), le juge 2 donne 2 (étapes pertinentes et présentes dans les
  extraits).

**Limites de cette mesure.**

- Aucune notation humaine : un juge automatique peut se tromper, être trop
  indulgent ou trop sévère, et un accord entre deux juges n'est pas une preuve
  de justesse. Une relecture humaine d'un échantillon reste souhaitable ; une
  aide à la lecture (réponse, guides attendus, extraits lus) est fournie dans
  `evaluation/results/aide_notation_20261119.md`.
- Les juges lisent les extraits récupérés de nouveau par la recherche dense
  (déterministe), et non une copie enregistrée au moment de la génération.
- Les notes d'un même modèle peuvent varier légèrement d'un lancement à l'autre.
