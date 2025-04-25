# config.py
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# —————— Bot ——————
BOT_TOKEN    = os.getenv("BOT_TOKEN")
# se preferir, valide que não é None e lance um erro amigável

# —————— Assets ——————
ASSETS_DIR   = os.getenv("ASSETS_DIR", "assets")

# —————— Logging ——————
LOGGING_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
LOGGING_LEVEL  = logging.INFO  # ou logging.DEBUG para desenvolvimento

# —————— Log de arquivo ——————
LOG_FILE = os.getenv("LOG_FILE", "bot.log")

# —————— Persistência ——————
DB_PATH = os.getenv("DB_PATH", "bot_data.db")

