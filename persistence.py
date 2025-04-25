"""
persistence.py

Gerencia o armazenamento de user_data no SQLite.
"""

import sqlite3
import aiosqlite
import json
import logging

import config

logger = logging.getLogger(__name__)

def init_db_sync():
    """
    Cria a tabela user_state se não existir.
    Função síncrona para ser chamada antes de levantar o bot.
    """
    conn = sqlite3.connect(config.DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_state (
            chat_id    INTEGER PRIMARY KEY,
            data       TEXT    NOT NULL,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Banco de dados inicializado (sync) em %s", config.DB_PATH)


async def load_state(chat_id: int) -> dict:
    """
    Carrega o JSON de user_data para este chat_id.
    Se não houver registro, retorna {}.
    """
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute(
            "SELECT data FROM user_state WHERE chat_id = ?", (chat_id,)
        )
        row = await cur.fetchone()
        await cur.close()

    if row:
        try:
            return json.loads(row[0])
        except json.JSONDecodeError:
            logger.warning("JSON inválido para chat_id=%s, reiniciando estado", chat_id)
    return {}


async def save_state(chat_id: int, state: dict) -> None:
    """
    Serializa e grava (INSERT ou UPDATE) o estado do usuário.
    """
    data_json = json.dumps(state)
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("""
            INSERT INTO user_state (chat_id, data)
            VALUES (?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET
                data = excluded.data,
                updated_at = CURRENT_TIMESTAMP
        """, (chat_id, data_json))
        await db.commit()
    logger.debug("Estado salvo para chat_id=%s", chat_id)


def with_state(func):
    """
    Decorator que, a cada chamada de handler, carrega do DB → context.user_data
    e, ao final, persiste o user_data de volta no DB.
    """
    async def wrapped(update, context):
        chat_id = update.effective_chat.id

        # 1) carrega do banco
        state = await load_state(chat_id)
        context.user_data.clear()
        context.user_data.update(state)

        # 2) executa o handler real
        await func(update, context)

        # 3) salva o estado atualizado
        await save_state(chat_id, context.user_data)

    return wrapped
