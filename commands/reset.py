# commands/reset.py

from telegram import Update
from telegram.ext import CallbackContext

from persistence import with_state, save_state
from chapters.chapter0 import chapter0   # em vez de importar start()

@with_state
async def reset_command(update: Update, context: CallbackContext):
    """
    /reset – Reinicia toda a jornada do Capítulo 0.
    Limpa user_data, salva o estado e dispara chapter0().
    """
    chat_id = update.effective_chat.id

    # 1) limpa tudo
    context.user_data.clear()
    await context.bot.send_message(chat_id, "♻️ Reiniciando a jornada…")

    # 2) salva o estado zerado
    await save_state(chat_id, context.user_data)

    # 3) inicia novamente o Capítulo 0
    context.user_data["seq"] = "start"
    await chapter0(update, context)
