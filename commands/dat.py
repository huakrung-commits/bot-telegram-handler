import os
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.security import restricted

description = "Affiche le lien de la documentation technique de l'infrastructure"

# Remplace par ton URL publique/VPN ou l'IP locale du Pi
DOC_URL = os.getenv("DOC_URL", "http://192.168.1.38/dat.html")

@restricted
async def doc_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "📚 **Documentation Technique de l'Infrastructure**\n\n"
        f"🔗 Retrouve la documentation complète ici :\n{DOC_URL}"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

handler = CommandHandler(["dat","architecture"], doc_callback)
