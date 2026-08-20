# Bot Telegram - Command Handler

Bot Telegram modulaire pour la supervision d'infrastructure Raspberry Pi, conteneurisé avec Docker.

## Architecture

Le projet utilise un chargement dynamique des commandes via le dossier `commands/`. Chaque nouvelle commande est un module indépendant exportant un objet `handler`.

```text
.
├── commands/           # Modules de commandes (/start, /status, etc.)
├── config.py           # Chargement des variables d'environnement
├── main.py             # Point d'entrée et registre dynamique
├── Dockerfile          # Image basée sur Python Alpine
└── docker-compose.yml  # Stack Docker
```

## 🚀 Installation & Déploiement

Prérequis
Docker & Docker Compose
Un token de bot créé via @BotFather
Configuration
Cloner le dépôt :
git clone https://github.com/huakrung-commits/bot-telegram-handler
cd bot-telegram-command-handler


Créer le fichier d'environnement à partir du modèle :
```text
cp .env.example .env
```


Renseigner TELEGRAM_TOKEN et ALLOWED_CHAT_ID dans le fichier .env.
Démarrage
```text
docker compose up -d --build
```

## ➕ Ajouter une nouvelle commande

Pour créer une nouvelle commande (ex: /ping) :
Crée un fichier commands/ping.py.
Définis la logique avec le décorateur de sécurité @restricted :

```text
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.security import restricted

@restricted
async def ping_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong 🏓")

handler = CommandHandler("ping", ping_callback)
```

Redémarre le conteneur (docker compose restart). La commande est automatiquement enregistrée.


## Automatiser avec un `Makefile` (Optionnel mais recommandé)

Ajoute un fichier **`Makefile`** à la racine pour simplifier les commandes quotidiennes :

```makefile
.PHONY: build up down restart logs clean

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

clean:
	docker system prune -f
