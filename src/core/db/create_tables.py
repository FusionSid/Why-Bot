import asyncio

from core.utils.client_functions import create_connection_pool


blacklist_query = """
CREATE TABLE blacklist
(
    user_id integer NOT NULL,
    reason text,
    PRIMARY KEY (user_id)
);
"""

tables_to_create = [blacklist_query]


async def create_tables():
    pool = await create_connection_pool()
    tasks = [pool.execute(table) for table in tables_to_create]
    await asyncio.gather(*tasks)
