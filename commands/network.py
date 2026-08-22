import os
import httpx
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.security import restricted

description = "Vérification du réseau proxy-net"

API_URL = os.getenv("PI_API_URL", "http://172.17.0.1:8000")
API_KEY = os.getenv("PI_API_KEY", "")

@restricted
async def network_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = await update.message.reply_text("🔍 **Vérification du réseau proxy-net...**", parse_mode="Markdown")

    headers = {"X-API-Key": API_KEY}

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_URL}/network/proxy-net", headers=headers, timeout=5.0)

            if res.status_code != 200:
                await msg.edit_text(f"❌ **Erreur API ({res.status_code})**", parse_mode="Markdown")
                return

            data = res.json()
            containers = data.get("containers", {})
            repair_needed = data.get("repair_needed", False)
            repair_commands = data.get("repair_commands", [])

            lines = []
            for name, details in containers.items():
                icon = "✅" if details.get("connected") else "❌"
                lines.append(f"• `{name}` : {icon} `{details.get('status_txt')}`")

            text = "🌐 **Isolation réseau (`proxy-net`)**\n\n" + "\n".join(lines) + "\n\n"

            if repair_needed and repair_commands:
                text += "⚠️ **Anomalie détectée !** Commandes de réparation :\n"
                for cmd in repair_commands:
                    text += f"```bash\n{cmd}\n```\n"
            else:
                text += "✨ **Isolation réseau 100% conforme !**"

            await msg.edit_text(text, parse_mode="Markdown")

    except Exception as e:
        await msg.edit_text(f"❌ Erreur lors de l'appel API : `{e}`")

handler = CommandHandler(["network"], network_callback)
