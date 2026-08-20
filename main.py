import importlib
import logging
import os
import pkgutil
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

import commands

# S'assure que les variables d'environnement sont chargées
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

def load_commands(application):
    """Charge dynamiquement tous les handlers exportés dans le dossier commands/."""
    package = commands
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if is_pkg or module_name.startswith("_"):
            continue

        full_module_name = f"commands.{module_name}"
        try:
            module = importlib.import_module(full_module_name)
            if hasattr(module, "handler"):
                application.add_handler(module.handler)
                logger.info("Commande chargée : %s", module_name)
            else:
                logger.warning("Le module %s ne possède pas d'objet 'handler'.", module_name)
        except Exception as e:
            logger.error("Échec du chargement du module %s : %s", module_name, e)

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Le token TELEGRAM_BOT_TOKEN est manquant dans l'environnement.")

    application = ApplicationBuilder().token(token).build()

    load_commands(application)

    logger.info("Lancement du bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
