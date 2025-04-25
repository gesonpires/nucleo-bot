"""
chapter5.py

Este módulo implementa o Capítulo 5 da narrativa (formação de nuvens e planetesimais):
– Estado 'start': introdução adaptativa ao ramo (solar vs. massivo) e escolha de nuvem.
– Estado 'decision': trata escolha de metalicidade; em caso de acerto, segue para quiz.
– Estado 'quiz': quiz sobre composição da poeira planetária; em caso de acerto, mostra botão Avançar.
– Estado 'await_ch6': aguarda clique em 'go_ch6' para iniciar o Capítulo 6.
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from persistence import with_state

from chapters.chapter6 import chapter6  # próximo capítulo

logger = logging.getLogger(__name__)

def _get_seq5(user_data: dict, default: str = "start") -> str:
    """Retorna o estado seq5 do usuário."""
    return user_data.get("seq5", default)

def _set_seq5(user_data: dict, value: str):
    """Define o estado seq5 do usuário."""
    user_data["seq5"] = value

@with_state
async def chapter5(update: Update, context: CallbackContext) -> None:
    """
    Inicia ou continua o capítulo 5 (formação da próxima geração).

    Fluxo:
    ------
    seq5 == 'start'      → apresenta texto adaptado e opções de nuvem (A/B/C)
    seq5 == 'decision'   → trata escolha; em caso de acerto, envia quiz
    seq5 == 'quiz'       → trata resposta do quiz; em caso de acerto, mostra botão Avançar
    seq5 == 'await_ch6'  → aguarda go_ch6 e dispara chapter6()
    """
    chat_id = update.effective_chat.id
    branch = context.user_data.get("branch")  # 'solar' ou 'massive'
    seq    = _get_seq5(context.user_data)

    # 5.1 — INTRODUÇÃO ADAPTATIVA
    if seq == "start":
        try:
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
                [InlineKeyboardButton("A) Z ≈ 0,03  (muito rica)",     callback_data="ch5_rich")],
                [InlineKeyboardButton("B) Z ≈ 0,02  (similar ao Sol)", callback_data="ch5_solarZ")],
                [InlineKeyboardButton("C) Z ≈ 0,0001 (muito pobre)",   callback_data="ch5_poor")],
            ]
            await context.bot.send_message(
                chat_id,
                "Qual nuvem escolher?",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            _set_seq5(context.user_data, "decision")

        except Exception:
            logger.error("Erro no Capítulo 5 [start]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao iniciar o Capítulo 5. Tente novamente mais tarde."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no Capítulo 5 [start]",
                    exc_info=True
                )

    # 5.2 — DECISÃO
    elif seq == "decision":
        try:
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

        except Exception:
            logger.error("Erro no Capítulo 5 [decision]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao processar sua escolha no Capítulo 5."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no Capítulo 5 [decision]",
                    exc_info=True
                )

    # 5.3 — QUIZ
    elif seq == "quiz":
        try:
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

        except Exception:
            logger.error("Erro no Capítulo 5 [quiz]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao processar o quiz do Capítulo 5."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no Capítulo 5 [quiz]",
                    exc_info=True
                )

    # 5.4 — AVANÇAR PARA CAPÍTULO 6
    elif seq == "await_ch6" and update.callback_query.data == "go_ch6":
        try:
            await update.callback_query.answer()
            context.user_data["seq5"] = "done"
            context.user_data["seq6"] = "start"
            await chapter6(update, context)

        except Exception:
            logger.error("Erro no Capítulo 5 [await_ch6]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Não foi possível avançar para o Capítulo 6."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no Capítulo 5 [await_ch6]",
                    exc_info=True
                )
