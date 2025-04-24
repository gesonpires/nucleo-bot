# chapters/chapter2B.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def chapter2B(update, context):
    """
    Ramo alternativo do Capítulo 2 – fusão de hélio falhou
    (exemplo simples; personalize o enredo como quiser)
    """
    chat_id = update.effective_chat.id
    seq = context.user_data.get('seq2B', 'start')

    if seq == 'start':
        context.bot.send_message(
            chat_id,
            "💥 A expansão rápida desestabilizou sua estrela! "
            "Vamos tentar salvar o núcleo com um pulso de convecção?"
        )
        kb = [
            [InlineKeyboardButton("Sim, resfriar a camada externa", callback_data='yes')],
            [InlineKeyboardButton("Não, abandonar a missão",        callback_data='no')]
        ]
        context.bot.send_message(chat_id, "Sua escolha:",
                                 reply_markup=InlineKeyboardMarkup(kb))
        context.user_data['seq2B'] = 'decision'

    elif seq == 'decision':
        choice = update.callback_query.data
        if choice == 'yes':
            update.callback_query.edit_message_text(
                "✅ Convecção iniciada! Temperatura estabilizada, podemos tentar o triplo-α novamente.")
            context.user_data['chapter2B_done'] = True
            # avance para capítulo 3, ou volte para chapter2...
        else:
            update.callback_query.edit_message_text("🔴 Missão abortada. A estrela colapsou.")
            context.user_data['seq2B'] = 'start'     # reinicia ramo
