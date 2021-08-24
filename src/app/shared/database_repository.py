import aiomysql
import logging
import json
from src.app.shared.json_log import log_debug

logger = logging.getLogger(__name__)

class DatabaseRepository:

    def __init__(self, conn):
        self.conn = conn

    async def query(self, sql_query, params=()):
        log_debug(logger, {'message': 'Executing query without side effects', 'query':sql_query, 'params': str(params)})
        async with self.conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql_query, params)
            result = await cur.fetchall()

            log_debug(logger, {'message': 'Result of query without side effect', 'query':sql_query, 'params': str(params), 'result': str(result)})

            return result

    async def update(self, sql_query, params=()):
        log_debug(logger, {'message': 'Executing query with side effects', 'query':sql_query, 'params': str(params)})
        async with self.conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql_query, params)
        await self.conn.commit()

    async def execute(self, cursor, sql_query, params=()):
        log_debug(logger, {'message': 'Executing query', 'query':sql_query, 'params': str(params)})
        await cursor.execute(sql_query, params)
        