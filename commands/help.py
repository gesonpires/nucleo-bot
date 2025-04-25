from telegram import Update
from telegram.ext import CallbackContext
from persistence import with_state

@with_state
async def help_command(update: Update, context: CallbackContext):
    txt = (
        "🤖 *Comandos disponíveis*:\n\n"
        "/start – Inicia a jornada do Big Bang às exoplanetas\n"
        "/reset – Reinicia a história do capítulo 0\n"
        "/status – Mostra onde você está e suas escolhas até agora\n"
        "/help – Exibe esta mensagem de ajuda\n"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=txt,
        parse_mode="Markdown"
    )
