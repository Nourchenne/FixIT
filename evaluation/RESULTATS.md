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
