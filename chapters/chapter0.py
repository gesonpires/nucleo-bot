from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from chapters.chapter1 import chapter1   # próximo capítulo

# ─────────────────── CAPÍTULO 0 ─────────────────── #
async def chapter0(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    seq = context.user_data.get("seq", "start")

    # 0.1 - INTRODUÇÃO --------------------------------
    if seq == "start":
        await context.bot.send_message(
            chat_id,
            "Olá, pesquisador 🚀 Sou a IA EOS-Σ. "
            "Sua primeira missão: reconstruir a química dos primeiros minutos do Universo."
        )

        with open("assets/H_He_donut.png", "rb") as img:
            await context.bot.send_photo(chat_id, img)

        await context.bot.send_message(
            chat_id,
            "Para obter 25 % de ⁴He, precisamos da razão nêutron/próton correta "
            "antes que o Universo esfrie demais."
        )

        keyboard = [
            [InlineKeyboardButton("A) Acelerar expansão",      callback_data="a")],
            [InlineKeyboardButton("B) Manter expansão natural", callback_data="b")],
            [InlineKeyboardButton("C) Diminuir expansão",      callback_data="c")],
        ]
        await context.bot.send_message(
            chat_id,
            "Qual estratégia escolher?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        context.user_data["seq"] = "decision"

    # 0.2 - DECISÃO ------------------------------------
    elif seq == "decision":
        choice = update.callback_query.data

        if choice == "b":                       # ✔️ resposta correta
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                "🟢 Boa! n/p≈1/7 gera 25 % de ⁴He. Baryon cookbook pronto."
            )

            next_kb = [
                [InlineKeyboardButton("➡️ Avançar para Capítulo 1",
                                      callback_data="go_ch1")]
            ]
            await context.bot.send_message(
                chat_id,
                "Pronto para acender a primeira estrela?",
                reply_markup=InlineKeyboardMarkup(next_kb),
            )
            context.user_data["seq"] = "await_ch1"

        else:                                   # ❌ respostas a ou c
            await update.callback_query.answer()
            msg = (
                "🔴 Expansão acelerada: n/p congela cedo; sobra menos He (15 %)."
                if choice == "a"
                else "🔴 Expansão lenta: nêutrons decaem demais; só 5 % de He."
            )
            await update.callback_query.edit_message_text(msg)

            keyboard = [
                [InlineKeyboardButton("A) Acelerar expansão",      callback_data="a")],
                [InlineKeyboardButton("B) Manter expansão natural", callback_data="b")],
                [InlineKeyboardButton("C) Diminuir expansão",      callback_data="c")],
            ]
            await context.bot.send_message(
                chat_id,
                "Tente outra estratégia:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
            # continua em 'decision'
            context.user_data["seq"] = "decision"

    # 0.3 - AVANÇAR PARA CAP.1 --------------------------
    elif seq == "await_ch1":
        if update.callback_query.data == "go_ch1":
            await update.callback_query.answer()

            # marca capítulo finalizado
            context.user_data["seq"] = "done"

            # inicia capítulo 1
            context.user_data["seq1"] = "start"
            await chapter1(update, context)
