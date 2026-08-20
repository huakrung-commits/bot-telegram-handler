import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes
from utils.security import restricted

description = "Affiche une page HTML (Usage: /page dat ou /page status)"
BASE_URL = os.getenv(
    "HTML_BASE_URL", "http://html.headlesspi.krung.duckdns.org"
)

# Dictionnaire des pages autorisées
PAGES = {
    "dat": {
        "title": "📚 Documentation Technique",
        "file": "dat.html",
        "btn": "Consulter la Documentation technique",
    },
    "status": {
        "title": "📊 Statut des Services",
        "file": "status.html",
        "btn": "Consulter le Statut",
    },
}


@restricted
async def page_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    # context.args contient la liste des mots tapés après /page
    if not context.args:
        # Aucun paramètre : on propose les boutons disponibles
        keyboard = [
            [
                InlineKeyboardButton(
                    info["title"], url=f"{BASE_URL}/{info['file']}"
                )
            ]
            for info in PAGES.values()
        ]
        await update.message.reply_text(
            "⚠️ **Veuillez préciser une page.** Exemple : `/page dat` ou `/page status`\n\nOu choisissez directement ci-dessous :",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
        return

    # On récupère le premier argument (en minuscules)
    page_key = context.args[0].lower()

    if page_key in PAGES:
        info = PAGES[page_key]
        url = f"{BASE_URL}/{info['file']}"
        keyboard = [[InlineKeyboardButton(info["btn"], url=url)]]

        await update.message.reply_text(
            f"{info['title']}\n🔗 Cliquez sur le bouton pour ouvrir la page :",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            f"❌ Page **'{page_key}'** inconnue. Les pages disponibles sont : `dat`, `status`.",
            parse_mode="Markdown",
        )


handler = CommandHandler("page", page_callback)
