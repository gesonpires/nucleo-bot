"""
chapter1.py

Este módulo implementa o capítulo 1 da narrativa:
– Estado 'start': introdução à ignição da primeira estrela do tipo solar.
– Estado 'decision': usuário escolhe entre comprimir rápido, contrair naturalmente ou injetar matéria escura.
– Estado 'quiz': mini-quiz sobre a partícula que escapa da fusão p+p.
– Estado 'await_ch2': botão de avanço para o Capítulo 2.

callback_data usados: 'ch1_a', 'ch1_b', 'ch1_c', 'ch1_q_photon', 'ch1_q_neutrino', 
'ch1_q_neutron', 'go_ch2'
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from persistence import with_state


from chapters.chapter2 import chapter2

logger = logging.getLogger(__name__)

@with_state
async def chapter1(update: Update, context: CallbackContext) -> None:
    """
    Inicia ou continua o capítulo 1.

    Parâmetros:
    -----------
    update : Update
        Objeto contendo mensagem ou callback.
    context : CallbackContext
        Contexto com user_data e acesso ao bot.

    Fluxo:
    ------
    seq1 == 'start'      → apresenta texto e teclado [A/B/C]
    seq1 == 'decision'   → trata escolha, envia quiz em caso de acerto ou repete opções
    seq1 == 'quiz'       → trata resposta do quiz, envia botão Avançar em caso de acerto
    seq1 == 'await_ch2'  → aguarda clique em 'go_ch2' e dispara chapter2()
    """
    chat_id = update.effective_chat.id
    seq     = context.user_data.get("seq1", "start")

    # 1.0 — INTRODUÇÃO ---------------------------------------------------
    if seq == "start":
        try:
            await context.bot.send_message(
                chat_id,
                "Ótimo trabalho com o Universo primordial! "
                "Agora precisamos acender a primeira estrela semelhante ao Sol."
            )
            await context.bot.send_message(
                chat_id,
                "Para iniciar a *cadeia pp*, o núcleo estelar deve chegar a ≈ 15 milhões de Kelvin."
            )

            keyboard = [
                [InlineKeyboardButton("A) Comprimir núcleo muito rápido",     callback_data="ch1_a")],
                [InlineKeyboardButton("B) Deixar contrair naturalmente",       callback_data="ch1_b")],
                [InlineKeyboardButton("C) Injetar matéria escura exotérmica",  callback_data="ch1_c")],
            ]
            await context.bot.send_message(
                chat_id,
                "Qual estratégia escolher?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            context.user_data["seq1"] = "decision"

        except Exception:
            logger.error("Erro no capítulo 1 [start]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao iniciar o Capítulo 1. Tente novamente mais tarde."
                )
            except:
                logger.critical("Falha ao notificar usuário sobre erro no capítulo 1 [start]",
                                exc_info=True)

    # 1.1 — DECISÃO -------------------------------------------------------
    elif seq == "decision":
        try:
            choice = update.callback_query.data
            await update.callback_query.answer()

            if choice == "ch1_b":  # ✔️ resposta correta
                await update.callback_query.edit_message_text(
                    "🟢 Perfeito! Temperatura ≈ 15 MK liga a fusão p+p → ²H + e⁺ + νₑ."
                )

                qkb = [
                    [InlineKeyboardButton("1) Fóton",    callback_data="ch1_q_photon")],
                    [InlineKeyboardButton("2) Neutrino", callback_data="ch1_q_neutrino")],
                    [InlineKeyboardButton("3) Nêutron",  callback_data="ch1_q_neutron")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Mini-quiz: Qual partícula escapa quase sem interagir e revela que a fusão ocorreu?",
                    reply_markup=InlineKeyboardMarkup(qkb)
                )
                context.user_data["seq1"] = "quiz"

            else:  # ❌ respostas A ou C
                msg = (
                    "🔴 Compressão extrema: temperatura sobe demais; a estrela se desestabiliza."
                    if choice == "ch1_a"
                    else "🔴 Matéria escura? Hipótese interessante, mas sem efeito prático nesta fase."
                )
                await update.callback_query.edit_message_text(msg)

                retry_kb = [
                    [InlineKeyboardButton("A) Comprimir núcleo muito rápido",     callback_data="ch1_a")],
                    [InlineKeyboardButton("B) Deixar contrair naturalmente",      callback_data="ch1_b")],
                    [InlineKeyboardButton("C) Injetar matéria escura exotérmica", callback_data="ch1_c")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Tente outra estratégia:",
                    reply_markup=InlineKeyboardMarkup(retry_kb)
                )
                context.user_data["seq1"] = "decision"

        except Exception:
            logger.error("Erro no capítulo 1 [decision]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao processar sua escolha. Tente novamente."
                )
            except:
                logger.critical("Falha ao notificar usuário sobre erro no capítulo 1 [decision]",
                                exc_info=True)

    # 1.2 — QUIZ ---------------------------------------------------------
    elif seq == "quiz":
        try:
            ans = update.callback_query.data
            await update.callback_query.answer()

            if ans == "ch1_q_neutrino":
                await update.callback_query.edit_message_text(
                    "✅ Neutrino! Detectores na Terra captam milhões vindos do Sol a cada segundo."
                )
                next_kb = [
                    [InlineKeyboardButton("➡️ Avançar para Capítulo 2", callback_data="go_ch2")]
                ]
                await context.bot.send_message(
                    chat_id,
                    "Pronto para a próxima fase da evolução estelar?",
                    reply_markup=InlineKeyboardMarkup(next_kb),
                )
                context.user_data["seq1"] = "await_ch2"

            else:
                await update.callback_query.edit_message_text(
                    "❌ Não exatamente. Tente de novo: qual partícula quase não interage?"
                )
                retry_qkb = [
                    [InlineKeyboardButton("1) Fóton",    callback_data="ch1_q_photon")],
                    [InlineKeyboardButton("2) Neutrino", callback_data="ch1_q_neutrino")],
                    [InlineKeyboardButton("3) Nêutron",  callback_data="ch1_q_neutron")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Escolha novamente:",
                    reply_markup=InlineKeyboardMarkup(retry_qkb)
                )
                # permanece em 'quiz'

        except Exception:
            logger.error("Erro no capítulo 1 [quiz]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Ocorreu um problema ao processar o quiz. Tente novamente."
                )
            except:
                logger.critical("Falha ao notificar usuário sobre erro no capítulo 1 [quiz]",
                                exc_info=True)

    # 1.3 — AVANÇAR PARA CAP.2 -----------------------------------------
    elif seq == "await_ch2":
        try:
            if update.callback_query.data == "go_ch2":
                await update.callback_query.answer()
                context.user_data["seq1"] = "done"
                context.user_data["seq2"] = "start"
                await chapter2(update, context)

        except Exception:
            logger.error("Erro no capítulo 1 [await_ch2]", exc_info=True)
            try:
                await context.bot.send_message(
                    chat_id,
                    "⚠️ Não foi possível avançar para o Capítulo 2. Tente novamente."
                )
            except:
                logger.critical("Falha ao notificar usuário sobre erro no capítulo 1 [await_ch2]",
                                exc_info=True)
