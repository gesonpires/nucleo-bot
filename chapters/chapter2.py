# chapters/chapter2.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from chapters.chapter3 import chapter3   # próximo capítulo

async def chapter2(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    seq     = context.user_data.get("seq2", "start")

    # 2.0 — INTRODUÇÃO
    if seq == "start":
        await context.bot.send_message(
            chat_id,
            "Sua estrela esgotou hidrogênio no núcleo, tornou-se gigante vermelha "
            "e o núcleo de hélio atingiu ~100 MK.\n"
            "Precisamos iniciar o processo **triplo-α** (³×He → ¹²C)."
        )
        kb = [
            [InlineKeyboardButton("A) Comprimir núcleo MUITO rápido", callback_data="ch2_a")],
            [InlineKeyboardButton("B) Aumentar pressão lentamente",   callback_data="ch2_b")],
            [InlineKeyboardButton("C) Resfriar o núcleo antes",       callback_data="ch2_c")],
        ]
        await context.bot.send_message(
            chat_id, "Qual estratégia escolher?",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        context.user_data["seq2"] = "decision"

    # 2.1 — DECISÃO
    elif seq == "decision":
        choice = update.callback_query.data
        await update.callback_query.answer()

        if choice == "ch2_b":  # ✔️ resposta correta
            await update.callback_query.edit_message_text(
                "🟢 Pressão moderada! ³×He → ¹²C e a estrela estabiliza."
            )
            quiz_kb = [
                [InlineKeyboardButton("8Be",  callback_data="ch2_q_be8")],
                [InlineKeyboardButton("12C",  callback_data="ch2_q_c12")],
                [InlineKeyboardButton("10C",  callback_data="ch2_q_c10")],
            ]
            await context.bot.send_message(
                chat_id,
                "Quiz: Qual núcleo instável serve de ponte no triplo-α?",
                reply_markup=InlineKeyboardMarkup(quiz_kb)
            )
            context.user_data["seq2"] = "quiz"

        else:  # ❌ respostas A ou C
            msg = ("🔴 Flash de hélio! Explosão descontrolada."
                   if choice == "ch2_a"
                   else "🔴 Núcleo esfriou; fusão não inicia.")
            await update.callback_query.edit_message_text(msg)

            # reenviar opções de decisão
            retry_kb = [
                [InlineKeyboardButton("A) Comprimir núcleo MUITO rápido", callback_data="ch2_a")],
                [InlineKeyboardButton("B) Aumentar pressão lentamente",   callback_data="ch2_b")],
                [InlineKeyboardButton("C) Resfriar o núcleo antes",       callback_data="ch2_c")],
            ]
            await context.bot.send_message(
                chat_id,
                "Tente outra estratégia:",
                reply_markup=InlineKeyboardMarkup(retry_kb)
            )
            context.user_data["seq2"] = "decision"

    # 2.2 — QUIZ
    elif seq == "quiz":
        ans = update.callback_query.data
        await update.callback_query.answer()

        if ans == "ch2_q_be8":  # ✔️ quiz correto
            await update.callback_query.edit_message_text(
                "✅ Correto! ⁸Be vive 10⁻¹⁶ s — tempo suficiente para capturar outro He e virar ¹²C."
            )
            # botão Avançar para Capítulo 3
            next_kb = [[InlineKeyboardButton(
                "➡️ Avançar para Capítulo 3", callback_data="go_ch3"
            )]]
            await context.bot.send_message(
                chat_id,
                "Pronto para descobrir como se formam bário e chumbo na fase AGB?",
                reply_markup=InlineKeyboardMarkup(next_kb)
            )
            context.user_data["seq2"] = "await_ch3"

        else:  # ❌ quiz errado
            await update.callback_query.edit_message_text(
                "❌ Ainda não. Lembre da ponte instável entre dois α."
            )
            # reenviar o quiz
            quiz_kb = [
                [InlineKeyboardButton("8Be",  callback_data="ch2_q_be8")],
                [InlineKeyboardButton("12C",  callback_data="ch2_q_c12")],
                [InlineKeyboardButton("10C",  callback_data="ch2_q_c10")],
            ]
            await context.bot.send_message(
                chat_id,
                "Quiz: Qual núcleo instável serve de ponte no triplo-α?",
                reply_markup=InlineKeyboardMarkup(quiz_kb)
            )
            context.user_data["seq2"] = "quiz"

    # 2.3 — AVANÇAR PARA CAPÍTULO 3
    elif seq == "await_ch3" and update.callback_query.data == "go_ch3":
        await update.callback_query.answer()
        context.user_data["seq2"] = "done"
        context.user_data["seq3"] = "start"
        await chapter3(update, context)
