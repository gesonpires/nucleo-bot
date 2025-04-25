"""
chapter3.py

Este módulo implementa o capítulo 3 da narrativa (fase AGB, processo s lento):
– Estado 'start': introdução à fase AGB e apresentação das opções de injeção de ¹³C.
– Estado 'decision': usuário escolhe taxa de ¹³C; em caso de acerto, segue para quiz.
– Estado 'quiz': mini-quiz sobre ritmo captura vs decaimento β; em caso de acerto, oferece botão Avançar.
– Estado 'await_ch4': aguarda clique em 'go_ch4' e dispara a escolha de ramo (chapter4).
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from persistence import with_state


from chapters.chapter4 import choose_branch  # dispara escolha de ramo para Capítulo 4

logger = logging.getLogger(__name__)

@with_state
async def chapter3(update: Update, context: CallbackContext) -> None:
    """
    Inicia ou continua o capítulo 3 (fase AGB, processo s):

    seq3 == 'start'     → apresenta texto e teclado [A/B/C]
    seq3 == 'decision'  → trata escolha, envia quiz em caso de acerto ou repete opções
    seq3 == 'quiz'      → trata resposta do quiz, envia botão Avançar em caso de acerto
    seq3 == 'await_ch4' → aguarda clique em 'go_ch4' e dispara choose_branch()
    """
    chat_id = update.effective_chat.id
    seq     = context.user_data.get("seq3", "start")

    # 3.0 — INTRODUÇÃO À FASE AGB
    if seq == "start":
        try:
            await context.bot.send_message(
                chat_id,
                "Sua estrela entrou na fase AGB: núcleo de carbono-oxigênio, "
                "cascas queimando hélio e hidrogênio."
            )
            await context.bot.send_message(
                chat_id,
                "Pulsos térmicos liberam nêutrons via ¹³C(α,n)¹⁶O. "
                "Precisamos de taxa moderada para formar Sr → Ba → Pb sem ejetar o envelope."
            )
            kb = [
                [InlineKeyboardButton("A) Injetar muito ¹³C",       callback_data="ch3_a")],
                [InlineKeyboardButton("B) Controle moderado de ¹³C", callback_data="ch3_b")],
                [InlineKeyboardButton("C) Nenhum ¹³C",              callback_data="ch3_c")],
            ]
            await context.bot.send_message(
                chat_id,
                "Qual opção escolher?",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["seq3"] = "decision"

        except Exception:
            logger.error("Erro no capítulo 3 [start]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao iniciar o Capítulo 3. Tente novamente mais tarde."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 3 [start]",
                    exc_info=True
                )

    # 3.1 — DECISÃO DO USUÁRIO
    elif seq == "decision":
        try:
            choice = update.callback_query.data
            await update.callback_query.answer()

            if choice == "ch3_b":
                await update.callback_query.edit_message_text(
                    "🟢 Taxa moderada! Sr → Ba → Pb se formam e a estrela exibe fortes linhas de bário."
                )
                qkb = [
                    [InlineKeyboardButton("1) Captura mais lenta que β", callback_data="ch3_q_ok")],
                    [InlineKeyboardButton("2) Temperatura muito baixa",   callback_data="ch3_q_lowT")],
                    [InlineKeyboardButton("3) Dura bilhões de anos",      callback_data="ch3_q_time")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Mini-quiz: Por que o processo s é chamado ‘lento’?",
                    reply_markup=InlineKeyboardMarkup(qkb)
                )
                context.user_data["seq3"] = "quiz"

            else:
                msg = (
                    "🔴 Excesso de nêutrons: instabilidade e perda do envelope!"
                    if choice == "ch3_a"
                    else "🔴 Sem ¹³C, nenhum nêutron → nenhum elemento pesado."
                )
                await update.callback_query.edit_message_text(msg)

                retry_kb = [
                    [InlineKeyboardButton("A) Injetar muito ¹³C",       callback_data="ch3_a")],
                    [InlineKeyboardButton("B) Controle moderado de ¹³C", callback_data="ch3_b")],
                    [InlineKeyboardButton("C) Nenhum ¹³C",              callback_data="ch3_c")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Tente outra vez:",
                    reply_markup=InlineKeyboardMarkup(retry_kb)
                )
                context.user_data["seq3"] = "decision"

        except Exception:
            logger.error("Erro no capítulo 3 [decision]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Erro ao processar sua escolha no Capítulo 3. Tente novamente."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 3 [decision]",
                    exc_info=True
                )

    # 3.2 — QUIZ
    elif seq == "quiz":
        try:
            ans = update.callback_query.data
            await update.callback_query.answer()

            if ans == "ch3_q_ok":
                await update.callback_query.edit_message_text(
                    "✅ Correto! Cada captura é mais lenta que o decaimento β, "
                    "acompanhando a linha de estabilidade."
                )
                next_kb = [[
                    InlineKeyboardButton("➡️ Avançar para Capítulo 4", callback_data="go_ch4")
                ]]
                await context.bot.send_message(
                    chat_id,
                    "Pronto para escolher o próximo estágio da evolução estelar?",
                    reply_markup=InlineKeyboardMarkup(next_kb)
                )
                context.user_data["seq3"] = "await_ch4"

            else:
                await update.callback_query.edit_message_text(
                    "❌ Ainda não. Pense no ritmo entre captura e decaimento."
                )
                quiz_kb = [
                    [InlineKeyboardButton("1) Captura mais lenta que β", callback_data="ch3_q_ok")],
                    [InlineKeyboardButton("2) Temperatura muito baixa",   callback_data="ch3_q_lowT")],
                    [InlineKeyboardButton("3) Dura bilhões de anos",      callback_data="ch3_q_time")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Escolha novamente:",
                    reply_markup=InlineKeyboardMarkup(quiz_kb)
                )
                context.user_data["seq3"] = "quiz"

        except Exception:
            logger.error("Erro no capítulo 3 [quiz]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao processar o quiz do Capítulo 3. Tente novamente."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 3 [quiz]",
                    exc_info=True
                )

    # 3.3 — DISPARAR ESCOLHA DE RAMO PARA CAPÍTULO 4
    elif seq == "await_ch4" and update.callback_query.data == "go_ch4":
        try:
            await update.callback_query.answer()
            context.user_data["seq3"] = "done"
            await choose_branch(update, context)

        except Exception:
            logger.error("Erro no capítulo 3 [await_ch4]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Não foi possível avançar para o Capítulo 4. Tente novamente."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 3 [await_ch4]",
                    exc_info=True
                )
