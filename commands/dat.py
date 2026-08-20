import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes
from telegram import WebAppInfo
from utils.security import restricted

description = "Ouvre la Mini App de documentation technique"

# URL publique/HTTPS gérée par ton Nginx Proxy Manager
DOC_URL = os.getenv("DOC_URL", "https://html.headlesspi.krung.duckdns.org/dat.html")

@restricted
async def doc_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton(
                "📚 Ouvrir la Documentation", 
                web_app=WebAppInfo(url=DOC_URL)
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Clique ci-dessous pour ouvrir la documentation technique complète :",
        reply_markup=reply_markup
    )

handler = CommandHandler(["dat"], doc_callback)