from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bonjour ! Le bot est en ligne.")

# Export explicite de l'objet handler
handler = CommandHandler("start", start_callback)
