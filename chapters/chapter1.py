from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from chapters.chapter2 import chapter2

async def chapter1(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    seq = context.user_data.get('seq1', 'start')

    # 1. INTRODUÇÃO ------------------------------------------------------
    if seq == 'start':
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
            [InlineKeyboardButton("A) Comprimir núcleo muito rápido",      callback_data='ch1_a')],
            [InlineKeyboardButton("B) Deixar contrair naturalmente",       callback_data='ch1_b')],
            [InlineKeyboardButton("C) Injetar matéria escura exotérmica",  callback_data='ch1_c')],
        ]
        await context.bot.send_message(
            chat_id,
            "Qual estratégia escolher?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        context.user_data['seq1'] = 'decision'

    # 2. DECISÃO ---------------------------------------------------------
    elif seq == 'decision':
        choice = update.callback_query.data

        if choice == 'ch1_b':          # ✅ resposta correta
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                "🟢 Perfeito! Temperatura ≈ 15 MK liga a fusão p + p → ²H + e⁺ + νₑ."
            )

            qkeyboard = [
                [InlineKeyboardButton("1) Fóton",    callback_data='ch1_q_photon')],
                [InlineKeyboardButton("2) Neutrino", callback_data='ch1_q_neutrino')],
                [InlineKeyboardButton("3) Nêutron",  callback_data='ch1_q_neutron')],
            ]
            await context.bot.send_message(
                chat_id,
                "Mini-quiz: Qual partícula escapa quase sem interagir e revela que a fusão ocorreu?",
                reply_markup=InlineKeyboardMarkup(qkeyboard)
            )
            context.user_data['seq1'] = 'quiz'

        # ------------- trecho dentro de elif seq == 'decision' -------------
        else:                          # ❌ respostas A ou C
            await update.callback_query.answer()
            msg = (
                "🔴 Compressão extrema: temperatura sobe demais; a estrela se desestabiliza."
                if choice == "ch1_a"
                else "🔴 Matéria escura? Hipótese interessante, mas sem efeito prático nesta fase."
            )
            await update.callback_query.edit_message_text(msg)

            # reenviar as opções para nova tentativa
            keyboard = [
                [InlineKeyboardButton("A) Comprimir núcleo muito rápido",     callback_data="ch1_a")],
                [InlineKeyboardButton("B) Deixar contrair naturalmente",      callback_data="ch1_b")],
                [InlineKeyboardButton("C) Injetar matéria escura exotérmica", callback_data="ch1_c")],
            ]
            await context.bot.send_message(
                chat_id,
                "Tente outra estratégia:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            context.user_data["seq1"] = "decision"   # continua aguardando clique

    # 3. QUIZ ------------------------------------------------------------
    elif seq == 'quiz':
        ans = update.callback_query.data
        if ans == 'ch1_q_neutrino':
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                "✅ Neutrino! Detectores na Terra captam milhões vindos do Sol a cada segundo."
            )
            
            # Botão Avançar
            next_kb = [[InlineKeyboardButton("➡️ Avançar para Capítulo 2", callback_data="go_ch2")]]
            await context.bot.send_message(
                chat_id,
                "Pronto para a próxima fase da evolução estelar?",
                reply_markup=InlineKeyboardMarkup(next_kb),
            )
                        
            context.user_data['seq1'] = "await_ch2"
            
        else:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                "❌ Não exatamente. Tente de novo: qual partícula quase não interage?"
            )
            
            qkeyboard = [
                [InlineKeyboardButton("1) Fóton",    callback_data='ch1_q_photon')],
                [InlineKeyboardButton("2) Neutrino", callback_data='ch1_q_neutrino')],
                [InlineKeyboardButton("3) Nêutron",  callback_data='ch1_q_neutron')],
            ]
            await context.bot.send_message(
                chat_id,
                "Escolha novamente:",
                reply_markup=InlineKeyboardMarkup(qkeyboard)
            )
    # continua em 'quiz'
            
            # permanece em seq 'quiz'
    elif seq == "await_ch2":
        if update.callback_query.data == "go_ch2":
            await update.callback_query.answer()
            context.user_data["seq1"] = "done"     # encerra capítulo 1

            # INICIALIZAR Próximo Capítulo (ramo solar por padrão)
            context.user_data["seq2"] = "start"
            await chapter2(update, context)