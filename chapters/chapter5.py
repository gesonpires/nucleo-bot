from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from chapters.chapter6 import chapter6  # próximo capítulo

def _get_seq5(user_data, default="start"):
    return user_data.get("seq5", default)

def _set_seq5(user_data, value):
    user_data["seq5"] = value

async def chapter5(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    branch = context.user_data.get("branch")  # 'solar' ou 'massive'
    seq = _get_seq5(context.user_data)

    if seq == "start":
        intro = (
            "Os átomos enriquecidos de bário, estrôncio e chumbo "
            "ejetados pela sua nebulosa planetária agora vagueiam pelo meio interestelar."
            if branch == "solar"
            else
            "O ouro, urânio e platina lançados pela sua supernova "
            "espalham-se pelo meio interestelar, prontos para novos ciclos."
        )
        await context.bot.send_message(chat_id, intro)
        await context.bot.send_message(
            chat_id,
            "Para formar a próxima geração de estrelas, precisamos escolher uma nuvem molecular "
            "com a metalicidade certa."
        )
        kb = [
            [InlineKeyboardButton("A) Z ≈ 0,03  (muito rica)",        callback_data="ch5_rich")],
            [InlineKeyboardButton("B) Z ≈ 0,02  (similar ao Sol)",    callback_data="ch5_solarZ")],
            [InlineKeyboardButton("C) Z ≈ 0,0001 (muito pobre)",      callback_data="ch5_poor")],
        ]
        await context.bot.send_message(
            chat_id, "Qual nuvem escolher?", reply_markup=InlineKeyboardMarkup(kb)
        )
        _set_seq5(context.user_data, "decision")

    elif seq == "decision":
        choice = update.callback_query.data
        await update.callback_query.answer()

        if choice == "ch5_solarZ":
            await update.callback_query.edit_message_text(
                "🟢 Metalicidade equilibrada! A nuvem esfria, colapsa e surge uma protoestrela com disco de detritos."
            )
            quiz_kb = [
                [InlineKeyboardButton("1) Silicatos e carbonatos", callback_data="ch5_q_ok")],
                [InlineKeyboardButton("2) Hidrogênio puro",        callback_data="ch5_q_h")],
                [InlineKeyboardButton("3) Núcleos de hélio",       callback_data="ch5_q_he")],
            ]
            await context.bot.send_message(
                chat_id,
                "Mini-quiz: A poeira sólida que forma planetas rochosos é composta principalmente de…",
                reply_markup=InlineKeyboardMarkup(quiz_kb)
            )
            _set_seq5(context.user_data, "quiz")
        else:
            msg = (
                "🔴 Metalicidade alta demais: opacidade elevada, nuvem se aquece e dispersa."
                if choice == "ch5_rich"
                else "🔴 Metalicidade muito baixa: resfriamento ineficiente, colapso não acontece."
            )
            await update.callback_query.edit_message_text(msg)
            _set_seq5(context.user_data, "start")

    elif seq == "quiz":
        ans = update.callback_query.data
        await update.callback_query.answer()

        if ans == "ch5_q_ok":
            await update.callback_query.edit_message_text(
                "✅ Correto! Grãos de silicatos e carbono são as sementes de planetas rochosos.\n\n"
                "🌌 Parabéns: o ciclo da matéria se completou — seus elementos podem, um dia, "
                "fazer parte de novos mundos e talvez de vida."
            )
            next_kb = [
                [InlineKeyboardButton("➡️ Avançar para Capítulo 6", callback_data="go_ch6")]
            ]
            await context.bot.send_message(
                chat_id,
                "Pronto para a última etapa da jornada?",
                reply_markup=InlineKeyboardMarkup(next_kb)
            )
            _set_seq5(context.user_data, "await_ch6")
        else:
            await update.callback_query.edit_message_text(
                "❌ Pense: planetas como a Terra não podem ser feitos só de gás."
            )
            quiz_kb = [
                [InlineKeyboardButton("1) Silicatos e carbonatos", callback_data="ch5_q_ok")],
                [InlineKeyboardButton("2) Hidrogênio puro",        callback_data="ch5_q_h")],
                [InlineKeyboardButton("3) Núcleos de hélio",       callback_data="ch5_q_he")],
            ]
            await context.bot.send_message(
                chat_id,
                "Tente de novo:",
                reply_markup=InlineKeyboardMarkup(quiz_kb)
            )
            _set_seq5(context.user_data, "quiz")

    elif seq == "await_ch6" and update.callback_query.data == "go_ch6":
        await update.callback_query.answer()
        context.user_data["seq5"] = "done"
        context.user_data["seq6"] = "start"
        await chapter6(update, context)
