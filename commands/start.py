from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

description = "Affiche ce message d'accueil et la liste des commandes"

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Récupération de la liste dynamique stockée lors du démarrage
    commands_list = context.application.bot_data.get("commands_help", {})
    
    lines = ["👋 <b>Bonjour ! Le bot est en ligne.</b>\n", "<b>Commandes disponibles :</b>"]
    for cmd, desc in commands_list.items():
        lines.append(f"• /{cmd} — {desc}")
        
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

handler = CommandHandler(["start"], start_callback)