import json
import asyncpg
import os

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .bot import Bot

class Database:
    """
    UniDB provides a simplified interface for using asyncpg with Discord bots.

    Attributes
    ----------
    pool : asyncpg.Pool
        The asyncpg connection pool.

    Methods
    -------
    async start(bot: Bot) -> asyncpg.Pool:
        Starts the UniDB and creates an asyncpg connection pool.

    async get(id: int, key: str, table: str)
        Retrieves a value from the specified table based on the given ID and key.

    async set(id: int, key: str, value, table: str) -> None
        Sets a value in the specified table based on the given ID and key.
    """

    def __init__(self, bot: 'Bot'):
        self.bot = bot
        self.pool = None
        
    async def init(self):
        async def init(con):
            await con.set_type_codec(
                "jsonb",
                schema="pg_catalog",
                encoder=lambda x: json.dumps(x),
                decoder=lambda x: json.loads(x),
                format="text",
            )

        self.pool = await asyncpg.create_pool(
            dsn=os.environ["POSTGRES_URI"],
            init=init,
            command_timeout=60,
            max_size=20,
            min_size=20,
            statement_cache_size=0
        )
        self.bot.pool = self.pool
        self.bot.db = self
        
    async def get(self, id: int, key: str, table: str):
        """
        Retrieves a value from the specified table based on the given ID and key.
        """
        try:
            query = await self.pool.fetchrow(
                """
                SELECT {0} FROM {1} WHERE id = $2
                """.format(key, table),
                id,
            )
            if query:
                return query[key]
        except Exception as e:
            print(e)
        return None

    async def set(self, id: int, key: str, value, table: str) -> None:
        """
        Sets a value in the specified table based on the given ID and key.
        """
        try:
            await self.pool.execute(
                """
                UPDATE {0} SET {1} = $1 WHERE id = $2
                """.format(table, key),
                value,
                id,
            )
        except Exception as e:
            print(e)

    def __await__(self):
        async def await_init():
            await self.init()

        return await_init().__await__()