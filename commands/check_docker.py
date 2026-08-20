import os
import httpx
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# Récupération de l'URL et de la clé API depuis le .env du bot
API_URL = os.getenv("PI_API_URL", "http://172.17.0.1:8000")
API_KEY = os.getenv("PI_API_KEY", "")

async def containers_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = await update.message.reply_text("🔍 **Analyse des conteneurs via l'API...**", parse_mode="Markdown")

    headers = {"X-API-Key": API_KEY}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/docker/containers", headers=headers, timeout=5.0)

            if response.status_code != 200:
                await msg.edit_text(f"❌ **Erreur API ({response.status_code}) :**\n`{response.text}`", parse_mode="Markdown")
                return

            data = response.json()
            containers = data.get("containers", [])
            total_count = data.get("total", 0)
            running_count = data.get("running", 0)

            if not containers:
                await msg.edit_text("ℹ️ Aucun conteneur Docker trouvé.")
                return

            lines = []
            for c in containers:
                name = c.get("name")
                status = c.get("status", "").lower()
                health = c.get("health", "N/A")

                # Détection des badges avec émojis
                if status == "running":
                    if health == "healthy":
                        badge = "✅ (healthy)"
                    elif health == "unhealthy":
                        badge = "⚠️ (unhealthy)"
                    else:
                        badge = "🟢 Up"
                elif status == "exited":
                    badge = "🔴 Stopped"
                elif status == "paused":
                    badge = "⏸️ Paused"
                elif status == "restarting":
                    badge = "🔄 Restarting"
                else:
                    badge = f"⚪ {status.capitalize()}"

                lines.append(f"• `{name}` — {badge}")

            summary = f"📦 **Statut Docker ({running_count}/{total_count} actifs)**\n\n"
            message_text = summary + "\n".join(lines)

            await msg.edit_text(message_text, parse_mode="Markdown")

    except httpx.ConnectError:
        await msg.edit_text("❌ **Erreur :** Impossible de se connecter à l'API du Pi. Vérifiez l'adresse `PI_API_URL`.")
    except Exception as e:
        await msg.edit_text(f"❌ **Erreur lors de l'appel API :**\n`{str(e)}`", parse_mode="Markdown")

# Enregistre la commande pour /containers, /docker et /check_docker
handler = CommandHandler(["containers", "docker", "check_docker"], containers_callback)
