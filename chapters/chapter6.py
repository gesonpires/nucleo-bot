# chapters/chapter6.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def chapter6(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    seq     = context.user_data.get("seq6", "start")

    # 6.1 — INTRODUÇÃO
    if seq == "start":
        await context.bot.send_message(
            chat_id,
            "O disco protoplanetário gira em torno da jovem estrela. "
            "Grãos de poeira de silicato e metais começam a se juntar, formando planetesimais."
        )
        # se tiver imagem, descomente e ajuste o path:
        # with open("assets/protoplanetary_disk.png", "rb") as img:
        #     await context.bot.send_photo(chat_id, img)

        kb = [
            [InlineKeyboardButton("A) Agitar fortemente o disco",       callback_data="ch6_a")],
            [InlineKeyboardButton("B) Deixar aglutinação natural",      callback_data="ch6_b")],
            [InlineKeyboardButton("C) Formar gigantes gasosos cedo",   callback_data="ch6_c")],
        ]
        await context.bot.send_message(
            chat_id,
            "Qual estratégia adotar?",
            reply_markup=InlineKeyboardMarkup(kb),
        )
        context.user_data["seq6"] = "decision"

    # 6.2 — DECISÃO
    elif seq == "decision":
        await update.callback_query.answer()
        choice = update.callback_query.data

        if choice == "ch6_b":
            await update.callback_query.edit_message_text(
                "🟢 Boa! Planetesimais crescem, alguns se tornam embriões planetários."
            )
            quiz_kb = [
                [InlineKeyboardButton("1) Mais sólidos disponíveis (gelo)", callback_data="ch6_q_ok")],
                [InlineKeyboardButton("2) Menos gravidade",                  callback_data="ch6_q_grav")],
                [InlineKeyboardButton("3) Temperatura maior",                callback_data="ch6_q_temp")],
            ]
            await context.bot.send_message(
                chat_id,
                "Mini-quiz: Por que a região além da linha de gelo favorece planetas gigantes?",
                reply_markup=InlineKeyboardMarkup(quiz_kb),
            )
            context.user_data["seq6"] = "quiz"

        else:
            msg = (
                "🔴 Turbulência extrema fragmenta planetesimais. Tente outra abordagem."
                if choice == "ch6_a"
                else "🔴 Núcleos gasosos migram para dentro e engolem materiais rochosos."
            )
            await update.callback_query.edit_message_text(msg)

            # reenviar opções de decisão
            retry_kb = [
                [InlineKeyboardButton("A) Agitar fortemente o disco",       callback_data="ch6_a")],
                [InlineKeyboardButton("B) Deixar aglutinação natural",      callback_data="ch6_b")],
                [InlineKeyboardButton("C) Formar gigantes gasosos cedo",   callback_data="ch6_c")],
            ]
            await context.bot.send_message(
                chat_id,
                "Tente outra estratégia:",
                reply_markup=InlineKeyboardMarkup(retry_kb),
            )
            context.user_data["seq6"] = "decision"

    # 6.3 — QUIZ
    elif seq == "quiz":
        await update.callback_query.answer()
        ans = update.callback_query.data

        if ans == "ch6_q_ok":
            await update.callback_query.edit_message_text(
                "✅ Exato! O gelo aumenta a massa dos núcleos, que capturam gás rapidamente.\n\n"
                "🌍 Sua poeira estelar virou mundos — possivelmente com oceanos e vida futura. "
                "Fim da jornada, mas o ciclo cósmico continua!"
            )
            context.user_data["chapter6_done"] = True
        else:
            await update.callback_query.edit_message_text(
                "❌ Não. Pense em quanta matéria sólida existe além da linha de gelo."
            )
            # repropor o quiz
            quiz_kb = [
                [InlineKeyboardButton("1) Mais sólidos disponíveis (gelo)", callback_data="ch6_q_ok")],
                [InlineKeyboardButton("2) Menos gravidade",                  callback_data="ch6_q_grav")],
                [InlineKeyboardButton("3) Temperatura maior",                callback_data="ch6_q_temp")],
            ]
            await context.bot.send_message(
                chat_id,
                "Tente novamente:",
                reply_markup=InlineKeyboardMarkup(quiz_kb),
            )
            context.user_data["seq6"] = "quiz"
