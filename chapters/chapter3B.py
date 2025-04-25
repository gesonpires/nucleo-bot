"""
chapter3B.py

Ramo alternativo do Capítulo 3 (fase AGB – ciclo CNO alternativo):
– Estado 'start': apresenta enredo e opções de estratégia.
– Estado 'decision': trata escolha; em caso de acerto, oferece botão Avançar para Capítulo 4.
– Estado 'await_ch4': aguarda clique em 'go_ch4' e dispara escolha de ramo.
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from persistence import with_state

from chapters.chapter4 import choose_branch  # para avançar ao capítulo 4

logger = logging.getLogger(__name__)
@with_state
async def chapter3B(update: Update, context: CallbackContext) -> None:
    """
    Inicia ou continua o capítulo 3B (ramo massivo alternativo).

    Fluxo:
    ------
    seq3B == 'start'      → apresenta texto e teclado [ch3b_a,ch3b_b]
    seq3B == 'decision'   → trata escolha:
        • 'ch3b_a' → sucesso, envia botão Avançar para Cap.4
        • 'ch3b_b' → falha, reinicia capítulo
    seq3B == 'await_ch4'  → aguarda callback_data 'go_ch4' e chama choose_branch()
    """
    chat_id = update.effective_chat.id
    seq     = context.user_data.get("seq3B", "start")

    # 3B.1 — INTRODUÇÃO
    if seq == "start":
        try:
            await context.bot.send_message(
                chat_id,
                "🌌 Capítulo 3B: Você optou por resfriar a estrela antes de formar oxigênio."
            )
            kb = [
                [InlineKeyboardButton("A) Tentar queimar carbono",          callback_data="ch3b_a")],
                [InlineKeyboardButton("B) Elevar temperatura antes demais", callback_data="ch3b_b")],
            ]
            await context.bot.send_message(
                chat_id,
                "Qual estratégia agora?",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["seq3B"] = "decision"

        except Exception:
            logger.error("Erro no capítulo 3B [start]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Erro ao iniciar o Capítulo 3B. Tente novamente mais tarde."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 3B [start]",
                    exc_info=True
                )

    # 3B.2 — DECISÃO
    elif seq == "decision":
        try:
            choice = update.callback_query.data
            await update.callback_query.answer()

            if choice == "ch3b_a":
                await update.callback_query.edit_message_text(
                    "✅ Combustão de carbono iniciada! Núcleo alcança 600 MK, formando ¹⁶O."
                )
                # botão Avançar para Capítulo 4
                next_kb = [[
                    InlineKeyboardButton("➡️ Avançar para Capítulo 4", callback_data="go_ch4")
                ]]
                await context.bot.send_message(
                    chat_id,
                    "Pronto para escolher o próximo estágio da evolução estelar?",
                    reply_markup=InlineKeyboardMarkup(next_kb)
                )
                context.user_data["seq3B"] = "await_ch4"

            else:  # ch3b_b
                await update.callback_query.edit_message_text(
                    "🔴 Temperatura subiu rápido demais; a estrela expulsa o envelope."
                )
                # reinicia o capítulo para nova tentativa
                context.user_data["seq3B"] = "start"

        except Exception:
            logger.error("Erro no capítulo 3B [decision]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Erro ao processar sua escolha no Capítulo 3B. Tente novamente."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 3B [decision]",
                    exc_info=True
                )

    # 3B.3 — AVANÇAR PARA ESCOLHA DE RAMO
    elif seq == "await_ch4" and update.callback_query.data == "go_ch4":
        try:
            await update.callback_query.answer()
            context.user_data["seq3B"] = "done"
            await choose_branch(update, context)

        except Exception:
            logger.error("Erro no capítulo 3B [await_ch4]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Não foi possível avançar para o Capítulo 4. Tente novamente."
                )
            except:
                logger.critical(
                    "Falha ao notificar usuário sobre erro no capítulo 3B [await_ch4]",
                    exc_info=True
                )
