# ───────────────────────── main.py ──────────────────────────
import os, logging
from dotenv import load_dotenv
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler
)

# -------- IMPORTAR CAPÍTULOS (todos async) ------------------
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
logging.basicConfig(level=logging.INFO)  # use DEBUG para ver o handler de cada callback
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# ---------------------- /start ------------------------------
async def start(update, context):
    context.user_data["seq"] = "start"    # chave que chapter0 usa
    await chapter0(update, context)

# ---------------------- main() ------------------------------
def main() -> None:
    app = Application.builder().token(TOKEN).build()

    # comando /start
    app.add_handler(CommandHandler("start", start))

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

    # pergunta solar vs massiva
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
