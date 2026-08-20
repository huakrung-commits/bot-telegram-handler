from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
import os

ALLOWED_CHAT_ID = int(os.getenv("ALLOWED_CHAT_ID", "0"))

def restricted(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_chat.id != ALLOWED_CHAT_ID:
            await update.message.reply_text("⛔ Accès non autorisé.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped
