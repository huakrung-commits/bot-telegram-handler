import os
import httpx
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.security import restricted

description = "Affiche l'état des jails et des IPs bannies dans Fail2ban"

API_URL = os.getenv("PI_API_URL", "http://localhost:8000")
API_KEY = os.getenv("PI_API_KEY", "")

@restricted
async def fail2ban_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = await update.message.reply_text("🛡️ **Analyse de Fail2ban en cours...**", parse_mode="Markdown")

    headers = {"X-API-Key": API_KEY}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/security/fail2ban/status", headers=headers, timeout=5.0)

            if response.status_code != 200:
                await msg.edit_text(f"❌ **Erreur API ({response.status_code}) :**\n`{response.text}`", parse_mode="Markdown")
                return

            data = response.json()
            details = data.get("details", {})

            if not details:
                await msg.edit_text("ℹ️ Aucune jail active configurée sur Fail2ban.")
                return

            lines = ["🛡️ **Statut Fail2ban**\n"]
            total_bans = 0

            for jail, info in details.items():
                count = info.get("currently_banned", 0)
                total_bans += count
                ips = info.get("banned_ips", [])
                
                if count > 0:
                    ips_str = ", ".join([f"`{ip}`" for ip in ips])
                    lines.append(f"• **{jail}** : {count} bannie(s) ({ips_str})")
                else:
                    lines.append(f"• **{jail}** : 🟢 0 bannie")

            lines.append(f"\n📊 **Total IPs bannies :** {total_bans}")
            await msg.edit_text("\n".join(lines), parse_mode="Markdown")

    except httpx.ConnectError:
        await msg.edit_text("❌ **Erreur :** Impossible de joindre l'API du Pi (`PI_API_URL`).")
    except Exception as e:
        await msg.edit_text(f"❌ **Erreur :** `{str(e)}`", parse_mode="Markdown")

# Accepte /fail2ban et /security
handler = CommandHandler(["fail2ban", "security"], fail2ban_callback)
