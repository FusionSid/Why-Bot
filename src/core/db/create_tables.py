import asyncio

from core.utils.client_functions import create_connection_pool


blacklist_query = """
CREATE TABLE IF NOT EXISTS blacklist
(
    user_id integer NOT NULL,
    reason text,
    PRIMARY KEY (user_id)
);
"""

command_stats_query = """
CREATE TABLE IF NOT EXISTS command_stats
(
    id SERIAL PRIMARY KEY,
    user_id bigint NOT NULL,
    command_name text NOT NULL,
    usage_count integer NOT NULL DEFAULT 0,
);
"""

counting_query = """
CREATE TABLE IF NOT EXISTS public.counting
(
    guild_id bigint NOT NULL PRIMARY KEY,
    last_counter bigint NOT NULL DEFAULT 0,
    current_number integer NOT NULL DEFAULT 0,
    counting_channel bigint NOT NULL DEFAULT 0,
);
"""

# If you wish not to create one of these tables in the setup process
# Simply just remove that item from this list:
tables_to_create = [blacklist_query, command_stats_query, counting_query]


async def create_tables():
    pool = await create_connection_pool()
    tasks = [pool.execute(table) for table in tables_to_create]
    await asyncio.gather(*tasks)
