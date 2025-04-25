from telegram import Update
from telegram.ext import CallbackContext
from persistence import with_state

@with_state
async def status_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    data = context.user_data
    # mapeia chaves para nomes legíveis
    mapping = {
        "seq":   "Capítulo 0",
        "seq1":  "Capítulo 1",
        "seq2":  "Capítulo 2",
        "seq2B":  "Capítulo 2 (B)",
        "seq3":  "Capítulo 3",
        "seq3B":  "Capítulo 3 (B)",
        "seq4": "Capítulo 4",
        "seq5":  "Capítulo 5",
        "seq6":  "Capítulo 6",
        "branch":"Ramo escolhido"
    }
    lines = []
    for key,name in mapping.items():
        if key in data:
            lines.append(f"*{name}* → `{data[key]}`")
    if not lines:
        lines = ["Você ainda não iniciou nenhuma missão. Use /start."]
    txt = "🔍 *Seu status atual:*\n\n" + "\n".join(lines)
    await context.bot.send_message(
        chat_id,
        txt,
        parse_mode="Markdown"
    )
