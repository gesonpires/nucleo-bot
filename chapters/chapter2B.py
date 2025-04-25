"""
chapter2B.py

Ramo alternativo do Capítulo 2 (para estrelas massivas, ciclo CNO):
– Estado 'start': introdução ao pulso de convecção para salvar o núcleo.
– Estado 'decision': usuário escolhe tentar convecção ou abortar.
– Estado 'await_ch3B': botão Avançar para o Capítulo 3B (fusão CNO).
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from persistence import with_state

from chapters.chapter3B import chapter3B  # próximo capítulo do ramo massivo

logger = logging.getLogger(__name__)

@with_state
async def chapter2B(update: Update, context: CallbackContext) -> None:
    """
    Inicia ou continua o capítulo 2B (ciclo CNO / ramo massivo).

    Fluxo:
    ------
    seq2B == 'start'      → apresenta enredo e teclado [yes/no]
    seq2B == 'decision'   → trata escolha: 
        • 'yes' → confirma convecção e oferece botão Avançar
        • 'no'  → reinicia o capítulo
    seq2B == 'await_ch3B' → aguarda clique em 'go_ch3B' e dispara chapter3B()
    """
    chat_id = update.effective_chat.id
    seq     = context.user_data.get("seq2B", "start")

    # 2B.1 — INTRODUÇÃO
    if seq == "start":
        try:
            await context.bot.send_message(
                chat_id,
                "💥 Sua estrela massiva falhou no triplo-α! "
                "Vamos tentar salvar o núcleo com um pulso de convecção?"
            )
            kb = [
                [InlineKeyboardButton("Sim, resfriar a camada externa", callback_data="2B_yes")],
                [InlineKeyboardButton("Não, abandonar a missão",        callback_data="2B_no")],
            ]
            await context.bot.send_message(
                chat_id,
                "Sua escolha:",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["seq2B"] = "decision"

        except Exception:
            logger.error("Erro no capítulo 2B [start]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Erro ao iniciar o Capítulo 2B. Tente novamente mais tarde."
                )
            except:
                logger.critical("Falha ao notificar usuário sobre erro no capítulo 2B [start]",
                                exc_info=True)

    # 2B.2 — DECISÃO
    elif seq == "decision":
        try:
            choice = update.callback_query.data
            await update.callback_query.answer()

            if choice == "2B_yes":
                await update.callback_query.edit_message_text(
                    "✅ Convecção iniciada! Temperatura estabilizada, podemos tentar o ciclo CNO."
                )
                next_kb = [
                    [InlineKeyboardButton("➡️ Avançar para Capítulo 3B", callback_data="go_ch3B")]
                ]
                await context.bot.send_message(
                    chat_id,
                    "Preparado para o próximo estágio da fusão em estrelas massivas?",
                    reply_markup=InlineKeyboardMarkup(next_kb)
                )
                context.user_data["seq2B"] = "await_ch3B"

            else:  # '2B_no'
                await update.callback_query.edit_message_text(
                    "🔴 Missão abortada. A estrela colapsou em buraco negro."
                )
                # reinicia o capítulo caso queira tentar novamente
                context.user_data["seq2B"] = "start"

        except Exception:
            logger.error("Erro no capítulo 2B [decision]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Erro ao processar sua escolha no Capítulo 2B. Tente novamente."
                )
            except:
                logger.critical("Falha ao notificar usuário sobre erro no capítulo 2B [decision]",
                                exc_info=True)

    # 2B.3 — AVANÇAR PARA CAPÍTULO 3B
    elif seq == "await_ch3B" and update.callback_query.data == "go_ch3B":
        try:
            await update.callback_query.answer()
            context.user_data["seq2B"] = "done"
            context.user_data["seq3B"] = "start"
            await chapter3B(update, context)

        except Exception:
            logger.error("Erro no capítulo 2B [await_ch3B]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Não foi possível avançar para o Capítulo 3B. Tente novamente."
                )
            except:
                logger.critical("Falha ao notificar usuário sobre erro no capítulo 2B [await_ch3B]",
                                exc_info=True)
