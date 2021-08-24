import aiomysql
import logging
import json

logger = logging.getLogger(__name__)

class DatabaseRepository:

    def __init__(self, conn):
        self.conn = conn

    async def query(self, sql_query, params=()):
        logger.debug(json.dumps({'message': 'Executing query without side effects', 'query':sql_query, 'params': str(params)}, indent=2))
        async with self.conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql_query, params)
            result = await cur.fetchall()

            logger.debug(json.dumps({'message': 'Result of query without side effect', 'query':sql_query, 'params': str(params), 'result': str(result)}, indent=2))

            return result

    async def update(self, sql_query, params=()):
        logger.debug(json.dumps({'message': 'Executing query with side effects', 'query':sql_query, 'params': str(params)}, indent=2))
        async with self.conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql_query, params)
        await self.conn.commit()

    async def execute(self, cursor, sql_query, params=()):
        logger.debug(json.dumps({'message': 'Executing query', 'query':sql_query, 'params': str(params)}, indent=2))
        await cursor.execute(sql_query, params)
        