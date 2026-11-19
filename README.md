# FixIT — Assistant de dépannage PC et Wi-Fi

FixIT est une application web Django qui aide à résoudre les problèmes courants
d'un PC sous Windows 11 et des connexions Wi-Fi. L'utilisateur décrit son
problème dans un chat ; l'assistant recherche la procédure adaptée dans une base
documentaire technique et propose des étapes de dépannage accompagnées de leurs
sources. Si le problème persiste, l'utilisateur crée un ticket, transmis à un
technicien par l'intermédiaire d'un serveur MCP.

Projet de fin de cours AI Engineering.

## Fonctionnalités

- Chat de dépannage en français ou en anglais, selon la langue de la question.
- Réponses fondées sur 46 guides PDF (Microsoft Support et fabricants), avec
  citation du document, de la page et du lien d'origine.
- Question de clarification lorsque la demande est trop vague, puis réponse
  tenant compte de la précision apportée.
- Comptes utilisateurs, historique des conversations.
- Création de tickets après confirmation, via MCP, sans doublon possible.
- Suivi des tickets : « Mes tickets », détail, historique ; consultation du
  statut directement depuis le chat (tool calling).
- Espace technicien : prise en charge, notes, cycle ouvert → en cours → résolu
  → fermé, réouverture.

## Architecture

```
Navigateur ── Django (comptes, chat, tickets)
                 │
                 ├── RAG : embeddings multilingual-e5-small ── Qdrant (Docker)
                 │         génération LangChain + Groq, citations vérifiées
                 │
                 └── Client MCP ── serveur MCP (sous-processus stdio)
                                      └── tickets/services.py ── SQLite
```

| Composant | Technologie |
|---|---|
| Application web | Python 3.10+, Django 5.2, templates Django, CSS sur mesure |
| Recherche documentaire | sentence-transformers (`intfloat/multilingual-e5-small`), Qdrant |
| Génération | LangChain, Groq (modèle configurable dans `.env`) |
| Outils | SDK MCP 2.3 (serveur `MCPServer`, client stdio), tool calling LangChain |
| Données | SQLite (comptes, conversations, tickets) |

## Installation (Windows, PowerShell)

Prérequis : Python 3.10 ou plus récent, Git, Docker Desktop, une clé API Groq
(console.groq.com). Toutes les commandes se lancent à la racine du dépôt, là
où se trouve `manage.py`. Évitez un dossier synchronisé par OneDrive : le
chargement des bibliothèques y est nettement plus lent.

**1. Code et environnement Python**

```powershell
git clone <adresse-du-depot> FixIT
cd FixIT
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**2. Qdrant (base vectorielle)**

Docker Desktop doit être lancé. La première fois :

```powershell
docker run -d --name fixit-qdrant -p 127.0.0.1:6335:6333 -v fixit_qdrant_data:/qdrant/storage qdrant/qdrant
```

Les fois suivantes : `docker start fixit-qdrant`.

**3. Indexation des documents**

Les PDF (`data/raw/`) et leur registre (`data/sources.csv`) sont versionnés.
Les fichiers générés (`data/processed/`) ne le sont pas : il faut les produire.

```powershell
python -m documents.services.ingesting
python -m documents.services.indexing
```

La première exécution télécharge le modèle d'embedding (environ 470 Mo).
Vérification : la commande suivante doit renvoyer `DOC001` en premier résultat.

```powershell
python -m assistant.services.retrieval "Mon ordinateur ne trouve aucun réseau Wi-Fi."
```

**4. Configuration**

```powershell
Copy-Item .env.example .env
```

Ouvrir `.env` et renseigner la clé Groq (le fichier n'est jamais versionné).

**5. Base de données et comptes**

```powershell
python manage.py migrate
python manage.py creer_comptes_demo --mot-de-passe "choisir-un-mot-de-passe"
python manage.py createsuperuser
```

`creer_comptes_demo` crée les groupes `utilisateur` et `technicien` et trois
comptes : `demo` et `demo2` (utilisateurs) et `technicien` (technicien).

**6. Lancement**

```powershell
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/ et se connecter avec l'un des comptes. La console
affiche « modèle et connexion prêts » quelques secondes après le démarrage, puis
la durée de recherche et de génération de chaque question.

## Variables d'environnement

| Variable | Rôle |
|---|---|
| `GROQ_API_KEY` | Clé de l'API Groq (obligatoire). |
| `GROQ_MODEL` | Modèle de génération, par exemple `openai/gpt-oss-20b`. |
| `FIXIT_PRECHARGEMENT` | `0` pour désactiver le préchargement du modèle au démarrage. |

## Démonstration du passage par MCP

```powershell
python manage.py demo_mcp --utilisateur demo --autre demo2
```

La commande liste les outils exposés par le serveur MCP, crée un ticket, renvoie
la même demande (aucun doublon), lit le statut via MCP, puis vérifie que le
second utilisateur (`demo2`) ne peut pas lire ce ticket.

## Tests

```powershell
python manage.py test
```

Les tests n'appellent ni Groq ni Qdrant (ces services sont simulés) et couvrent
le format des réponses, la latence, les vues, les comptes, le service de
tickets, le serveur et le client MCP, l'agent de suivi et l'évaluation.

## Évaluation

| Script | Mesure |
|---|---|
| `python -m evaluation.evaluate_retrieval --questions evaluation/questions_final.jsonl` | Recherche : Recall@5, Recall@10, MRR@10 (Qdrant seul). |
| `python -m evaluation.evaluate_retrieval --questions evaluation/questions_final.jsonl --rerank` | Même mesure avec reranking, pour comparaison. |
| `python -m evaluation.evaluate_generation` | Réponses : langue, citations, repli hors corpus, durée ; grille CSV à noter 0, 1 ou 2. |
| `python -m evaluation.juge_llm` | Notes 0, 1 ou 2 données par un modèle juge (colonnes `note_auto_llm`), à compléter par une relecture humaine. `--modele ... --suffixe _2` pour un second juge. |

Résultats et décision de configuration : `evaluation/RESULTATS.md`.

## Structure du dépôt

```
accounts/        rôles, commande creer_comptes_demo
assistant/       chat : vues, modèles Conversation/Message
  services/      chat.py (génération), retrieval.py (recherche), outils.py (suivi de ticket)
documents/       ingestion, embeddings, indexation, modèle Document
tickets/         services.py (règles métier), vues, commande demo_mcp
mcp_server/      serveur MCP (outils create_ticket, get_ticket_status)
integrations/    client MCP, outils LangChain
evaluation/      jeux de questions, scripts et résultats d'évaluation
templates/, static/   interface
data/            PDF, registre des sources, fichiers générés
```

## Dépannage rapide

| Symptôme | Cause et solution |
|---|---|
| `ModuleNotFoundError` sur une bibliothèque installée | L'environnement n'est pas activé : `.\.venv\Scripts\Activate.ps1` (l'invite doit afficher `(.venv)`). |
| `WinError 10061` ou « connexion refusée » | Qdrant n'est pas démarré : `docker start fixit-qdrant`. |
| « Collection introuvable » | Collection absente sur ce poste : relancer `python -m documents.services.indexing`. |
| « Configure GROQ_API_KEY et GROQ_MODEL » | Fichier `.env` absent ou incomplet. |
| Longue pause au premier lancement | Chargement de `transformers` et du modèle : patienter, ne pas interrompre. |

## Sources documentaires

Les guides proviennent de Microsoft Support et de sites de fabricants ; chaque
document est référencé dans `data/sources.csv` (URL, titre, date de collecte).
Ils restent la propriété de leurs auteurs et ne sont redistribués que dans le
cadre de ce projet pédagogique.
