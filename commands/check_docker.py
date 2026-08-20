import docker
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def check_docker_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = await update.message.reply_text("🔍 **Analyse des conteneurs Docker...**", parse_mode="Markdown")

    try:
        docker_socket = os.getenv("DOCKER_HOST", "unix://var/run/docker.sock")
        client = docker.DockerClient(base_url=docker_socket)
        containers = client.containers.list(all=True)

        if not containers:
            await msg.edit_text("ℹ️ Aucun conteneur Docker trouvé sur la machine.")
            return

        # Tri des conteneurs par nom
        containers.sort(key=lambda c: c.name)

        running_count = 0
        total_count = len(containers)
        lines = []

        for c in containers:
            status = c.status.lower()
            name = c.name

            # Détection de l'état avec émojis
            if status == "running":
                running_count += 1
                # Vérification de l'état de santé (healthcheck) s'il existe
                health = c.attrs.get("State", {}).get("Health", {}).get("Status")
                if health == "healthy":
                    badge = "✅ (healthy)"
                elif health == "unhealthy":
                    badge = "⚠️ (unhealthy)"
                else:
                    badge = "🟢 Up"
            elif status == "exited":
                badge = "🔴 Stopped"
            elif status == "paused":
                badge = "⏸️ Paused"
            elif status == "restarting":
                badge = "🔄 Restarting"
            else:
                badge = f"⚪ {status.capitalize()}"

            lines.append(f"• `{name}` — {badge}")

        summary = f"📦 **Statut Docker ({running_count}/{total_count} actifs)**\n\n"
        message_text = summary + "\n".join(lines)

        await msg.edit_text(message_text, parse_mode="Markdown")

    except Exception as e:
        await msg.edit_text(f"❌ **Erreur d'accès à Docker :**\n`{str(e)}`", parse_mode="Markdown")

# Enregistre la commande sous /check_docker ou /chack_containers
handler = CommandHandler(["check_docker", "docker"], check_docker_callback)
