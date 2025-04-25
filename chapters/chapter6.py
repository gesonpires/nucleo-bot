"""
chapter6.py

Este módulo implementa o Capítulo 6 da narrativa (formação de planetas):
– Estado 'start': introdução ao disco protoplanetário e opções de estratégia.
– Estado 'decision': trata escolha de aglutinação; em caso de acerto, segue para quiz.
– Estado 'quiz': trata resposta do quiz; em caso de acerto, encerra a jornada.

callback_data usados:
  ch6_a, ch6_b, ch6_c,
  ch6_q_ok, ch6_q_grav, ch6_q_temp
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from persistence import with_state

logger = logging.getLogger(__name__)

@with_state
async def chapter6(update: Update, context: CallbackContext) -> None:
    """
    Capítulo 6 – Formação de planetas.

    seq6 == 'start'    → apresenta texto e opções A/B/C
    seq6 == 'decision' → trata escolha, envia quiz em caso de acerto ou repete opções
    seq6 == 'quiz'     → trata resposta do quiz; encerra o fluxo com mensagem final
    """
    chat_id = update.effective_chat.id
    seq     = context.user_data.get("seq6", "start")

    # 6.1 — INTRODUÇÃO
    if seq == "start":
        try:
            await context.bot.send_message(
                chat_id,
                "O disco protoplanetário gira em torno da jovem estrela. "
                "Grãos de poeira de silicato e metais começam a se juntar, formando planetesimais."
            )
            # Se quiser enviar uma imagem, descomente e ajuste o caminho:
            # with open("assets/protoplanetary_disk.png", "rb") as img:
            #     await context.bot.send_photo(chat_id, img)

            kb = [
                [InlineKeyboardButton("A) Agitar fortemente o disco",     callback_data="ch6_a")],
                [InlineKeyboardButton("B) Deixar aglutinação natural",    callback_data="ch6_b")],
                [InlineKeyboardButton("C) Formar gigantes gasosos cedo", callback_data="ch6_c")],
            ]
            await context.bot.send_message(
                chat_id,
                "Qual estratégia adotar?",
                reply_markup=InlineKeyboardMarkup(kb),
            )
            context.user_data["seq6"] = "decision"

        except Exception:
            logger.error("Erro no Capítulo 6 [start]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao iniciar o Capítulo 6. Tente novamente mais tarde."
                )
            except Exception:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no Capítulo 6 [start]",
                    exc_info=True
                )

    # 6.2 — DECISÃO
    elif seq == "decision":
        try:
            await update.callback_query.answer()
            choice = update.callback_query.data

            if choice == "ch6_b":
                await update.callback_query.edit_message_text(
                    "🟢 Boa! Planetesimais crescem, alguns se tornam embriões planetários."
                )
                quiz_kb = [
                    [InlineKeyboardButton("1) Mais sólidos disponíveis (gelo)", callback_data="ch6_q_ok")],
                    [InlineKeyboardButton("2) Menos gravidade",                 callback_data="ch6_q_grav")],
                    [InlineKeyboardButton("3) Temperatura maior",               callback_data="ch6_q_temp")],
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

                retry_kb = [
                    [InlineKeyboardButton("A) Agitar fortemente o disco",     callback_data="ch6_a")],
                    [InlineKeyboardButton("B) Deixar aglutinação natural",    callback_data="ch6_b")],
                    [InlineKeyboardButton("C) Formar gigantes gasosos cedo", callback_data="ch6_c")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Tente outra estratégia:",
                    reply_markup=InlineKeyboardMarkup(retry_kb),
                )
                context.user_data["seq6"] = "decision"

        except Exception:
            logger.error("Erro no Capítulo 6 [decision]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao processar sua escolha no Capítulo 6."
                )
            except Exception:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no Capítulo 6 [decision]",
                    exc_info=True
                )

    # 6.3 — QUIZ
    elif seq == "quiz":
        try:
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
                quiz_kb = [
                    [InlineKeyboardButton("1) Mais sólidos disponíveis (gelo)", callback_data="ch6_q_ok")],
                    [InlineKeyboardButton("2) Menos gravidade",                 callback_data="ch6_q_grav")],
                    [InlineKeyboardButton("3) Temperatura maior",               callback_data="ch6_q_temp")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Tente novamente:",
                    reply_markup=InlineKeyboardMarkup(quiz_kb),
                )
                context.user_data["seq6"] = "quiz"

        except Exception:
            logger.error("Erro no Capítulo 6 [quiz]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao processar o quiz do Capítulo 6."
                )
            except Exception:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no Capítulo 6 [quiz]",
                    exc_info=True
                )
