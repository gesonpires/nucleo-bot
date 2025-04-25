"""
chapter4.py

Este módulo implementa o Capítulo 4 da narrativa, com duas rotas:
– chapter4A (ramo Solar / nebulosa planetária)
– chapter4B (ramo Massivo / Supernova II + r-process)
Além disso, fornece a escolha de ramo antes do início de 4A ou 4B.

callbacks:
  ch4a_a, ch4a_b, ch4a_c, ch4a_q_wd, go_ch5
  ch4b_a, ch4b_b, ch4b_c, ch4b_q_ok, go_ch5
  solar, massive
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from persistence import with_state

from chapters.chapter5 import chapter5  # próximo capítulo

logger = logging.getLogger(__name__)

# ───────────────── UTILITÁRIOS ─────────────────

async def _send_image(bot, chat_id, path: str):
    """
    Tenta enviar uma imagem de arquivo local.
    Se não encontrar, avisa o usuário.
    """
    try:
        with open(path, "rb") as f:
            await bot.send_photo(chat_id, f)
    except FileNotFoundError:
        await bot.send_message(chat_id, "(Imagem não encontrada)")

def _set_seq(user_data: dict, key: str, value: str):
    """Define o estado seqX no user_data."""
    user_data[key] = value

def _get_seq(user_data: dict, key: str, default: str="start") -> str:
    """Recupera o estado seqX do user_data."""
    return user_data.get(key, default)


# ──────────────── CAPÍTULO 4A ────────────────

@with_state
async def chapter4A(update: Update, context: CallbackContext) -> None:
    """
    Capítulo 4A (ramo Solar):
    seq4A == 'start'       → introdução + teclado A/B/C
    seq4A == 'decision'    → trata escolha; em caso de acerto, segue para quiz
    seq4A == 'quiz'        → trata resposta; em caso de acerto, mostra botão Avançar
    seq4A == 'await_ch5'   → aguarda go_ch5 e dispara chapter5()
    """
    chat_id = update.effective_chat.id
    seq     = _get_seq(context.user_data, "4A")

    # 4A.1 – introdução
    if seq == "start":
        try:
            await context.bot.send_message(
                chat_id,
                "Pulsos térmicos expulsam as camadas externas da estrela. "
                "Um anel incandescente forma uma belíssima “nebulosa planetária”."
            )
            await _send_image(context.bot, chat_id, "assets/Planetary_Nebula.png")
            kb = [
                [InlineKeyboardButton("A) Impulsionar vento muito forte", callback_data="ch4a_a")],
                [InlineKeyboardButton("B) Manter pulso natural",          callback_data="ch4a_b")],
                [InlineKeyboardButton("C) Reduzir vento",                 callback_data="ch4a_c")],
            ]
            await context.bot.send_message(
                chat_id,
                "Como controlar a ejeção de massa?",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            _set_seq(context.user_data, "4A", "decision")

        except Exception:
            logger.error("Erro no Capítulo 4A [start]", exc_info=True)
            try:
                await context.bot.send_message(chat_id,
                    "⚠️ Ocorreu um problema ao iniciar o Capítulo 4A. Tente novamente mais tarde.")
            except:
                logger.critical("Falha ao notificar usuário no Capítulo 4A [start]", exc_info=True)

    # 4A.2 – decisão
    elif seq == "decision":
        try:
            choice = update.callback_query.data
            await update.callback_query.answer()

            if choice == "ch4a_b":
                await update.callback_query.edit_message_text(
                    "🟢 Pulso equilibrado! As camadas ricas em elementos s-process brilham, "
                    "enquanto o núcleo vira uma anã branca."
                )
                quiz_kb = [
                    [InlineKeyboardButton("1) Anã branca",        callback_data="ch4a_q_wd")],
                    [InlineKeyboardButton("2) Estrela de nêutrons", callback_data="ch4a_q_ns")],
                    [InlineKeyboardButton("3) Buraco negro",       callback_data="ch4a_q_bh")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Mini-quiz: O objeto compacto que fica no centro da nebulosa é…",
                    reply_markup=InlineKeyboardMarkup(quiz_kb)
                )
                _set_seq(context.user_data, "4A", "quiz")

            else:
                msg = ("🔴 Vento forte demais: o gás escapa rápido, a nebulosa fica difusa."
                       if choice == "ch4a_a"
                       else "🔴 Vento fraco: as camadas não saem e a nebulosa não se forma.")
                await update.callback_query.edit_message_text(msg)
                retry_kb = [
                    [InlineKeyboardButton("A) Impulsionar vento muito forte", callback_data="ch4a_a")],
                    [InlineKeyboardButton("B) Manter pulso natural",           callback_data="ch4a_b")],
                    [InlineKeyboardButton("C) Reduzir vento",                  callback_data="ch4a_c")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Tente novamente:",
                    reply_markup=InlineKeyboardMarkup(retry_kb)
                )
                _set_seq(context.user_data, "4A", "decision")

        except Exception:
            logger.error("Erro no Capítulo 4A [decision]", exc_info=True)
            try:
                await context.bot.send_message(chat_id,
                    "⚠️ Ocorreu um problema ao processar sua escolha no Capítulo 4A.")
            except:
                logger.critical("Falha ao notificar usuário no Capítulo 4A [decision]", exc_info=True)

    # 4A.3 – quiz
    elif seq == "quiz":
        try:
            ans = update.callback_query.data
            await update.callback_query.answer()

            if ans == "ch4a_q_wd":
                await update.callback_query.edit_message_text(
                    "✅ Correto! Uma anã branca de carbono-oxigênio brilha no centro. 🌟"
                )
                next_kb = [[
                    InlineKeyboardButton("➡️ Avançar para Capítulo 5", callback_data="go_ch5")
                ]]
                await context.bot.send_message(
                    chat_id,
                    "Pronto para o capítulo final?",
                    reply_markup=InlineKeyboardMarkup(next_kb)
                )
                _set_seq(context.user_data, "4A", "await_ch5")

            else:
                await update.callback_query.edit_message_text("❌ Tente novamente.")
                quiz_kb = [
                    [InlineKeyboardButton("1) Anã branca",        callback_data="ch4a_q_wd")],
                    [InlineKeyboardButton("2) Estrela de nêutrons", callback_data="ch4a_q_ns")],
                    [InlineKeyboardButton("3) Buraco negro",       callback_data="ch4a_q_bh")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Mini-quiz: O objeto compacto é…",
                    reply_markup=InlineKeyboardMarkup(quiz_kb)
                )
                _set_seq(context.user_data, "4A", "quiz")

        except Exception:
            logger.error("Erro no Capítulo 4A [quiz]", exc_info=True)
            try:
                await context.bot.send_message(chat_id,
                    "⚠️ Ocorreu um problema ao processar o quiz do Capítulo 4A.")
            except:
                logger.critical("Falha ao notificar usuário no Capítulo 4A [quiz]", exc_info=True)

    # 4A.4 – avançar para Capítulo 5
    elif seq == "await_ch5" and update.callback_query.data == "go_ch5":
        try:
            await update.callback_query.answer()
            _set_seq(context.user_data, "4A", "done")
            context.user_data["seq5"] = "start"
            await chapter5(update, context)

        except Exception:
            logger.error("Erro no Capítulo 4A [await_ch5]", exc_info=True)
            try:
                await context.bot.send_message(chat_id,
                    "⚠️ Não foi possível avançar para o Capítulo 5.")
            except:
                logger.critical("Falha ao notificar usuário no Capítulo 4A [await_ch5]", exc_info=True)


# ──────────────── CAPÍTULO 4B ────────────────

async def chapter4B(update: Update, context: CallbackContext) -> None:
    """
    Capítulo 4B (ramo Massivo):
    seq4B == 'start'       → introdução + teclado A/B/C
    seq4B == 'decision'    → trata escolha; em caso de acerto, segue para quiz
    seq4B == 'quiz'        → trata resposta; em caso de acerto, mostra botão Avançar
    seq4B == 'await_ch5'   → aguarda go_ch5 e dispara chapter5()
    """
    chat_id = update.effective_chat.id
    seq     = _get_seq(context.user_data, "4B")

    # 4B.1 – introdução
    if seq == "start":
        try:
            await context.bot.send_message(
                chat_id,
                "O núcleo de ferro colapsa até densidade nuclear. "
                "Estamos prestes a presenciar uma Supernova Tipo II!"
            )
            await _send_image(context.bot, chat_id, "assets/Supernova_TypeII.png")
            kb = [
                [InlineKeyboardButton("A) Aumentar massa lentamente", callback_data="ch4b_a")],
                [InlineKeyboardButton("B) Permitir colapso natural",  callback_data="ch4b_b")],
                [InlineKeyboardButton("C) Remover massa do núcleo",   callback_data="ch4b_c")],
            ]
            await context.bot.send_message(
                chat_id,
                "Como proceder antes do colapso?",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            _set_seq(context.user_data, "4B", "decision")

        except Exception:
            logger.error("Erro no Capítulo 4B [start]", exc_info=True)
            try:
                await context.bot.send_message(chat_id,
                    "⚠️ Ocorreu um problema ao iniciar o Capítulo 4B.")
            except:
                logger.critical("Falha ao notificar usuário no Capítulo 4B [start]", exc_info=True)

    # 4B.2 – decisão
    elif seq == "decision":
        try:
            choice = update.callback_query.data
            await update.callback_query.answer()

            if choice == "ch4b_b":
                await update.callback_query.edit_message_text(
                    "💥 BOOM! Choque reverso e processo r: ouro, urânio e platina nascem."
                )
                quiz_kb = [
                    [InlineKeyboardButton("1) Múltiplas capturas antes do β", callback_data="ch4b_q_ok")],
                    [InlineKeyboardButton("2) Reduzir temperatura",             callback_data="ch4b_q_lowT")],
                    [InlineKeyboardButton("3) Formar lítio",                   callback_data="ch4b_q_li")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Mini-quiz: Por que a densidade de nêutrons é essencial no processo r?",
                    reply_markup=InlineKeyboardMarkup(quiz_kb)
                )
                _set_seq(context.user_data, "4B", "quiz")

            else:
                msg = ("🔴 Colapso falhou: neutrinos dissipam energia."
                       if choice == "ch4b_a"
                       else "🔴 Sem massa crítica, sem supernova.")
                await update.callback_query.edit_message_text(msg)
                retry_kb = [
                    [InlineKeyboardButton("A) Aumentar massa lentamente", callback_data="ch4b_a")],
                    [InlineKeyboardButton("B) Permitir colapso natural",  callback_data="ch4b_b")],
                    [InlineKeyboardButton("C) Remover massa do núcleo",   callback_data="ch4b_c")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Tente novamente:",
                    reply_markup=InlineKeyboardMarkup(retry_kb)
                )
                _set_seq(context.user_data, "4B", "decision")

        except Exception:
            logger.error("Erro no Capítulo 4B [decision]", exc_info=True)
            try:
                await context.bot.send_message(chat_id,
                    "⚠️ Ocorreu um problema ao processar sua escolha no Capítulo 4B.")
            except:
                logger.critical("Falha ao notificar usuário no Capítulo 4B [decision]", exc_info=True)

    # 4B.3 – quiz
    elif seq == "quiz":
        try:
            ans = update.callback_query.data
            await update.callback_query.answer()

            if ans == "ch4b_q_ok":
                await update.callback_query.edit_message_text(
                    "✅ Exato! Múltiplas capturas rápidas sucedem o decaimento β. 🌠"
                )
                next_kb = [[
                    InlineKeyboardButton("➡️ Avançar para Capítulo 5", callback_data="go_ch5")
                ]]
                await context.bot.send_message(
                    chat_id,
                    "Pronto para o capítulo final?",
                    reply_markup=InlineKeyboardMarkup(next_kb)
                )
                _set_seq(context.user_data, "4B", "await_ch5")

            else:
                await update.callback_query.edit_message_text(
                    "❌ Pense na ordem captura → decaimento."
                )
                quiz_kb = [
                    [InlineKeyboardButton("1) Múltiplas capturas antes do β", callback_data="ch4b_q_ok")],
                    [InlineKeyboardButton("2) Reduzir temperatura",             callback_data="ch4b_q_lowT")],
                    [InlineKeyboardButton("3) Formar lítio",                   callback_data="ch4b_q_li")],
                ]
                await context.bot.send_message(
                    chat_id,
                    "Mini-quiz: Por que precisa alta densidade de nêutrons?",
                    reply_markup=InlineKeyboardMarkup(quiz_kb)
                )
                _set_seq(context.user_data, "4B", "quiz")

        except Exception:
            logger.error("Erro no Capítulo 4B [quiz]", exc_info=True)
            try:
                await context.bot.send_message(chat_id,
                    "⚠️ Ocorreu um problema ao processar o quiz do Capítulo 4B.")
            except:
                logger.critical("Falha ao notificar usuário no Capítulo 4B [quiz]", exc_info=True)

    # 4B.4 – avançar para Capítulo 5
    elif seq == "await_ch5" and update.callback_query.data == "go_ch5":
        try:
            await update.callback_query.answer()
            _set_seq(context.user_data, "4B", "done")
            context.user_data["seq5"] = "start"
            await chapter5(update, context)

        except Exception:
            logger.error("Erro no Capítulo 4B [await_ch5]", exc_info=True)
            try:
                await context.bot.send_message(chat_id,
                    "⚠️ Não foi possível avançar para o Capítulo 5.")
            except:
                logger.critical("Falha ao notificar usuário no Capítulo 4B [await_ch5]", exc_info=True)


# ──────────────── ESCOLHA DE RAMO ────────────────

async def choose_branch(update: Update, context: CallbackContext) -> None:
    """
    Exibe botão para escolher: ramo Solar (4A) ou ramo Massivo (4B).
    callback_data: 'solar' ou 'massive'
    """
    chat_id = update.effective_chat.id
    try:
        kb = [
            [InlineKeyboardButton("⭐ Estrela tipo Solar (~1 M☉)", callback_data="solar")],
            [InlineKeyboardButton("🌟 Estrela Massiva (~10 M☉)",  callback_data="massive")],
        ]
        await context.bot.send_message(
            chat_id,
            "Qual trajetória estelar deseja seguir?",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        _set_seq(context.user_data, "branch", "choose")

    except Exception:
        logger.error("Erro em choose_branch", exc_info=True)
        try:
            await context.bot.send_message(chat_id,
                "⚠️ Não foi possível exibir escolha de ramo. Tente novamente.")
        except:
            logger.critical("Falha ao notificar usuário em choose_branch", exc_info=True)

async def branch_handler(update: Update, context: CallbackContext) -> None:
    """
    Recebe o callback de escolha de ramo:
    - 'solar' → chama chapter4A
    - 'massive' → chama chapter4B
    """
    chat_id = update.effective_chat.id
    branch = update.callback_query.data
    try:
        await update.callback_query.answer()
        context.user_data["branch"] = branch

        if branch == "solar":
            await update.callback_query.edit_message_text("Você escolheu estrela tipo solar. Vamos!")
            _set_seq(context.user_data, "4A", "start")
            await chapter4A(update, context)
        else:
            await update.callback_query.edit_message_text("Você escolheu estrela massiva. Avante!")
            _set_seq(context.user_data, "4B", "start")
            await chapter4B(update, context)

    except Exception:
        logger.error("Erro em branch_handler", exc_info=True)
        try:
            await context.bot.send_message(chat_id,
                "⚠️ Não foi possível processar sua escolha de ramo.")
        except:
            logger.critical("Falha ao notificar usuário em branch_handler", exc_info=True)
