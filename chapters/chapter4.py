# chapters/chapter4.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# ───────────────── UTILITÁRIOS ─────────────────
async def _send_image(bot, chat_id, path):
    try:
        with open(path, "rb") as f:
            await bot.send_photo(chat_id, f)
    except FileNotFoundError:
        await bot.send_message(chat_id, "(Imagem não encontrada)")

def _set_seq(user_data, key, value):
    user_data[key] = value

def _get_seq(user_data, key, default="start"):
    return user_data.get(key, default)

# importa o próximo capítulo
from chapters.chapter5 import chapter5

# ──────────────── CAPÍTULO 4A ────────────────
async def chapter4A(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    seq     = _get_seq(context.user_data, "4A")

    # 4A.1 – introdução
    if seq == "start":
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
            chat_id, "Como controlar a ejeção de massa?",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        _set_seq(context.user_data, "4A", "decision")

    # 4A.2 – decisão
    elif seq == "decision":
        choice = update.callback_query.data
        await update.callback_query.answer()

        if choice == "ch4a_b":
            await update.callback_query.edit_message_text(
                "🟢 Pulso equilibrado! As camadas ricas em elementos s-process brilham, "
                "enquanto o núcleo vira uma anã branca."
            )
            quiz_kb = [
                [InlineKeyboardButton("1) Anã branca",       callback_data="ch4a_q_wd")],
                [InlineKeyboardButton("2) Estrela de nêutrons", callback_data="ch4a_q_ns")],
                [InlineKeyboardButton("3) Buraco negro",     callback_data="ch4a_q_bh")],
            ]
            await context.bot.send_message(
                chat_id,
                "Mini-quiz: O objeto compacto que fica no centro da nebulosa é…",
                reply_markup=InlineKeyboardMarkup(quiz_kb)
            )
            _set_seq(context.user_data, "4A", "quiz")
        else:
            msg = (
                "🔴 Vento forte demais: o gás escapa rápido, a nebulosa fica difusa."
                if choice == "ch4a_a"
                else "🔴 Vento fraco: as camadas não saem e a nebulosa não se forma."
            )
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

    # 4A.3 – quiz
    elif seq == "quiz":
        ans = update.callback_query.data
        await update.callback_query.answer()

        if ans == "ch4a_q_wd":
            await update.callback_query.edit_message_text(
                "✅ Correto! Uma anã branca de carbono-oxigênio brilha no centro. 🌟"
            )
            # botão Avançar para Capítulo 5
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
                [InlineKeyboardButton("1) Anã branca",       callback_data="ch4a_q_wd")],
                [InlineKeyboardButton("2) Estrela de nêutrons", callback_data="ch4a_q_ns")],
                [InlineKeyboardButton("3) Buraco negro",     callback_data="ch4a_q_bh")],
            ]
            await context.bot.send_message(
                chat_id,
                "Mini-quiz: O objeto compacto é…",
                reply_markup=InlineKeyboardMarkup(quiz_kb)
            )
            _set_seq(context.user_data, "4A", "quiz")

    # 4A.4 – avançar para Capítulo 5
    elif seq == "await_ch5" and update.callback_query.data == "go_ch5":
        await update.callback_query.answer()
        _set_seq(context.user_data, "4A", "done")
        context.user_data["seq5"] = "start"
        await chapter5(update, context)


# ──────────────── CAPÍTULO 4B ────────────────
async def chapter4B(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    seq     = _get_seq(context.user_data, "4B")

    # 4B.1 – introdução
    if seq == "start":
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
            chat_id, "Como proceder antes do colapso?",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        _set_seq(context.user_data, "4B", "decision")

    # 4B.2 – decisão
    elif seq == "decision":
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
            msg = (
                "🔴 Colapso falhou: neutrinos dissipam energia."
                if choice == "ch4b_a"
                else "🔴 Sem massa crítica, sem supernova."
            )
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

    # 4B.3 – quiz
    elif seq == "quiz":
        ans = update.callback_query.data
        await update.callback_query.answer()

        if ans == "ch4b_q_ok":
            await update.callback_query.edit_message_text(
                "✅ Exato! Múltiplas capturas rápidas sucedem o decaimento β. 🌠"
            )
            # botão Avançar para Capítulo 5
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

    # 4B.4 – avançar para Capítulo 5
    elif seq == "await_ch5" and update.callback_query.data == "go_ch5":
        await update.callback_query.answer()
        _set_seq(context.user_data, "4B", "done")
        context.user_data["seq5"] = "start"
        await chapter5(update, context)


# ──────────────── ESCOLHA DE RAMO ────────────────
async def choose_branch(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
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

async def branch_handler(update: Update, context: CallbackContext) -> None:
    branch = update.callback_query.data
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
