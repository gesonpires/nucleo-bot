# ───────────────────────── main.py ──────────────────────────
import asyncio
import logging
import config

from persistence import init_db_sync

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

# ─────── COMMAND HANDLERS ───────
from commands.help   import help_command
from commands.reset  import reset_command
from commands.status import status_command

# ─── IMPORTAR CAPÍTULOS (todos async) ───
from chapters.chapter0   import chapter0
from chapters.chapter1   import chapter1
from chapters.chapter2   import chapter2
from chapters.chapter2B  import chapter2B
from chapters.chapter3   import chapter3
from chapters.chapter3B  import chapter3B
from chapters.chapter4   import branch_handler, chapter4A, chapter4B
from chapters.chapter5   import chapter5
from chapters.chapter6   import chapter6

# ------------------------------------------------------------
logging.basicConfig(
    format= config.LOGGING_FORMAT,
    level=  config.LOGGING_LEVEL
)

file_handler = logging.FileHandler(config.LOG_FILE)
file_handler.setFormatter(logging.Formatter(config.LOGGING_FORMAT))
logging.getLogger().addHandler(file_handler)

TOKEN = config.BOT_TOKEN
if not TOKEN:
    raise RuntimeError("BOT_TOKEN não definido em .env")

# ---------------------- /start ------------------------------
async def start(update, context):
    context.user_data["seq"] = "start"    # chave que chapter0 usa
    await chapter0(update, context)

# ---------------------- main() ------------------------------
def main() -> None:
    # 1) garante que a tabela existe antes de receber atualizações
    init_db_sync()
    
    app = Application.builder().token(TOKEN).build()

    # ------ Comandos básicos ------
    app.add_handler(CommandHandler("start",  start))
    app.add_handler(CommandHandler("help",   help_command))
    app.add_handler(CommandHandler("reset",  reset_command))
    app.add_handler(CommandHandler("status", status_command))

    # cada capítulo só “escuta” seus próprios callbacks
    app.add_handler(CallbackQueryHandler(chapter0,
        pattern=r"^(a|b|c|go_ch1)$", block=False))

    app.add_handler(CallbackQueryHandler(chapter1,
        pattern=r"^(ch1_|go_ch2$)", block=False))

    app.add_handler(CallbackQueryHandler(chapter2,
        pattern=r"^(ch2_|go_ch3$)", block=False))

    app.add_handler(CallbackQueryHandler(chapter2B,
        pattern=r"^ch2b_", block=False))

    app.add_handler(CallbackQueryHandler(chapter3,
        pattern=r"^(ch3_|go_ch4$)", block=False))

    app.add_handler(CallbackQueryHandler(chapter3B,
        pattern=r"^ch3b_", block=False))

    # pergunta solar vs massiva (capítulo 4)
    app.add_handler(CallbackQueryHandler(
        branch_handler,
        pattern=r"^(solar|massive)$",
        block=False
    ))

    app.add_handler(CallbackQueryHandler(chapter4A,
        pattern=r"^(ch4a_|go_ch5$)", block=False))

    app.add_handler(CallbackQueryHandler(chapter4B,
        pattern=r"^(ch4b_|go_ch5$)", block=False))

    app.add_handler(CallbackQueryHandler(chapter5,
        pattern=r"^(ch5_|go_ch6$)", block=False))

    app.add_handler(CallbackQueryHandler(chapter6,
        pattern=r"^ch6_", block=False))

    logging.info("Bot running… Press Ctrl+C to stop")
    app.run_polling()

if __name__ == "__main__":
    main()
