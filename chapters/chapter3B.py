# chapters/chapter3B.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def chapter3B(update, context):
    """Ramo alternativo do Capítulo 3 – exemplo simplificado."""
    chat_id = update.effective_chat.id
    seq = context.user_data.get('seq3B', 'start')

    if seq == 'start':
        context.bot.send_message(
            chat_id,
            "🌌 Capítulo 3B: Você optou por resfriar a estrela antes de formar oxigênio."
        )
        kb = [
            [InlineKeyboardButton("A) Tentar queimar carbono", callback_data='a')],
            [InlineKeyboardButton("B) Elevar temperatura primeiro", callback_data='b')]
        ]
        context.bot.send_message(chat_id, "Qual estratégia agora?",
                                 reply_markup=InlineKeyboardMarkup(kb))
        context.user_data['seq3B'] = 'decision'

    elif seq == 'decision':
        choice = update.callback_query.data
        if choice == 'a':
            update.callback_query.edit_message_text(
                "✅ Combustão de carbono iniciada. Núcleo alcança 600 MK, formando ¹⁶O.")
            context.user_data['chapter3B_done'] = True
            # … avance para capítulo 4
        else:
            update.callback_query.edit_message_text(
                "🔴 Temperatura subiu rápido demais; a estrela expulsa o envelope.")
            context.user_data['seq3B'] = 'start'   # reinicia ramo
