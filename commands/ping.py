from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def ping_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Pong ! 🏓")

handler = CommandHandler("ping", ping_callback)
