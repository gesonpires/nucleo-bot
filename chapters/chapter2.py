"""
chapter2.py

Este módulo implementa o capítulo 2 da narrativa (estrela solar, processo triplo-α):
– Estado 'start': introdução ao triplo-α e apresentação das opções de estratégia.
– Estado 'decision': usuário escolhe A/B/C; em caso de acerto, avança para o quiz.
– Estado 'quiz': quiz sobre o núcleo instável ⁸Be; em caso de acerto, oferece botão Avançar.
– Estado 'await_ch3': aguarda clique em 'go_ch3' para iniciar o Capítulo 3.

callback_data usados: 
 ch2_a, ch2_b, ch2_c, 
 ch2_q_be8, ch2_q_c12, ch2_q_c10, 
 go_ch3
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from persistence import with_state


from chapters.chapter3 import chapter3   # próximo capítulo

logger = logging.getLogger(__name__)

@with_state
async def chapter2(update: Update, context: CallbackContext) -> None:
    """
    Inicia ou continua o capítulo 2 (triplo-α).

    Fluxo:
    ------
    seq2 == 'start'      → apresenta texto e teclado [A/B/C]
    seq2 == 'decision'   → trata escolha, envia quiz em caso de acerto ou repete opções
    seq2 == 'quiz'       → trata resposta do quiz, envia botão Avançar em caso de acerto
    seq2 == 'await_ch3'  → aguarda clique em 'go_ch3' e dispara chapter3()
    """
    chat_id = update.effective_chat.id
    seq     = context.user_data.get("seq2", "start")

    # 2.0 — INTRODUÇÃO
    if seq == "start":
        try:
            await context.bot.send_message(
                chat_id,
                "Sua estrela esgotou hidrogênio no núcleo, tornou-se gigante vermelha "
                "e o núcleo de hélio atingiu ~100 MK.\n"
                "Precisamos iniciar o processo **triplo-α** (³×He → ¹²C)."
            )
            kb = [
                [InlineKeyboardButton("A) Comprimir núcleo MUITO rápido", callback_data="ch2_a")],
                [InlineKeyboardButton("B) Aumentar pressão lentamente",    callback_data="ch2_b")],
                [InlineKeyboardButton("C) Resfriar o núcleo antes",        callback_data="ch2_c")],
            ]
            await context.bot.send_message(
                chat_id,
                "Qual estratégia escolher?",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["seq2"] = "decision"

        except Exception:
            logger.error("Erro no capítulo 2 [start]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Houve um problema ao iniciar o Capítulo 2. Por favor, tente novamente mais tarde."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 2 [start]",
                    exc_info=True
                )

    # 2.1 — DECISÃO
    elif seq == "decision":
        try:
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
                msg = (
                    "🔴 Flash de hélio! Explosão descontrolada."
                    if choice == "ch2_a"
                    else "🔴 Núcleo esfriou; fusão não inicia."
                )
                await update.callback_query.edit_message_text(msg)

                retry_kb = [
                    [InlineKeyboardButton("A) Comprimir núcleo MUITO rápido", callback_data="ch2_a")],
                    [InlineKeyboardButton("B) Aumentar pressão lentamente",    callback_data="ch2_b")],
                    [InlineKeyboardButton("C) Resfriar o núcleo antes",        callback_data="ch2_c")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Tente outra estratégia:",
                    reply_markup=InlineKeyboardMarkup(retry_kb)
                )
                context.user_data["seq2"] = "decision"

        except Exception:
            logger.error("Erro no capítulo 2 [decision]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao processar sua escolha no Capítulo 2."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 2 [decision]",
                    exc_info=True
                )

    # 2.2 — QUIZ
    elif seq == "quiz":
        try:
            ans = update.callback_query.data
            await update.callback_query.answer()

            if ans == "ch2_q_be8":  # ✔️ quiz correto
                await update.callback_query.edit_message_text(
                    "✅ Correto! ⁸Be vive 10⁻¹⁶ s — tempo suficiente para capturar outro He e virar ¹²C."
                )
                next_kb = [[
                    InlineKeyboardButton("➡️ Avançar para Capítulo 3", callback_data="go_ch3")
                ]]
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

        except Exception:
            logger.error("Erro no capítulo 2 [quiz]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao processar o quiz do Capítulo 2."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 2 [quiz]",
                    exc_info=True
                )

    # 2.3 — AVANÇAR PARA CAPÍTULO 3
    elif seq == "await_ch3" and update.callback_query.data == "go_ch3":
        try:
            await update.callback_query.answer()
            context.user_data["seq2"] = "done"
            context.user_data["seq3"] = "start"
            await chapter3(update, context)

        except Exception:
            logger.error("Erro no capítulo 2 [await_ch3]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Não foi possível avançar para o Capítulo 3. Tente novamente."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 2 [await_ch3]",
                    exc_info=True
                )
