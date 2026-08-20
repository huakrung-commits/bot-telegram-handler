import os
import httpx
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

description = "Affiche l'état des ressources système (CPU, RAM, Disque)"

API_URL = os.getenv("PI_API_URL", "http://localhost:8000")
API_KEY = os.getenv("PI_API_KEY", "")

async def status_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    headers = {"X-API-Key": API_KEY}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_URL}/system/status", headers=headers, timeout=5.0)
            data = response.json()

            msg = (
                "📊 **Statut du Raspberry Pi**\n\n"
                f"⏱️ **Uptime :** `{data['uptime']}`\n"
                f"⚡ **CPU :** `{data['cpu_usage_percent']}%`\n"
                f"🧠 **RAM :** `{data['ram']['percent']}%` (`{data['ram']['used_mb']}` / `{data['ram']['total_mb']}` Mo)\n"
                f"💾 **Disque :** `{data['disk']['percent']}%` (Libre: `{data['disk']['free_gb']}` Go)"
            )
            await update.message.reply_text(msg, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur lors de l'appel API : `{e}`")

handler = CommandHandler("status", status_callback)
