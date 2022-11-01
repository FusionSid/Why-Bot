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
    usage_count integer NOT NULL DEFAULT 0
);
"""

counting_query = """
CREATE TABLE IF NOT EXISTS counting
(
    guild_id bigint NOT NULL PRIMARY KEY,
    last_counter bigint,
    current_number integer,
    counting_channel bigint,
    high_score integer,
    auto_calculate boolean,
    plugin_enabled boolean
);
"""

leveling_member_query = """
CREATE TABLE IF NOT EXISTS leveling_member
(
    guild_id bigint NOT NULL,
    member_id bigint NOT NULL,
    member_name text,
    member_xp integer,
    member_level integer,
    member_total_xp bigint
);
"""

leveling_guild_query = """
CREATE TABLE IF NOT EXISTS leveling_guild
(
    guild_id bigint NOT NULL PRIMARY KEY,
    plugin_enabled boolean,
    text_font text,
    text_color text,
    background_image text,
    background_color text,
    progress_bar_color text,
    no_xp_roles json,
    no_xp_channels json,
    level_up_text text,
    level_up_enabled boolean,
    per_minute text
);
"""

leveling_rewards_query = """
CREATE TABLE IF NOT EXISTS leveling_rewards
(
    guild_id bigint NOT NULL PRIMARY KEY,
    level integer,
    role bigint
);
"""

counters_query = """
CREATE TABLE IF NOT EXISTS counters
(
    key text NOT NULL PRIMARY KEY,
    value integer NOT NULL DEFAULT 0
);
"""

dmreply_query = """
CREATE TABLE IF NOT EXISTS dmreply
(
    user_id bigint NOT NULL PRIMARY KEY,
    thread_id bigint NOT NULL
);
"""

tags_query = """
CREATE TABLE IF NOT EXISTS tags
(
    guild_id bigint NOT NULL PRIMARY KEY,
    tag_name TEXT NOT NULL,
    tag_value TEXT NOT NULL,
    tag_author TEXT NOT NULL,
    time_created date NOT NULL default current_timestamp
);
"""

alerts_query = """
CREATE TABLE IF NOT EXISTS alerts
(
    id serial NOT NULL PRIMARY KEY,
    alert_title text NOT NULL,
    alert_message text NOT NULL,
    time_created date NOT NULL default current_timestamp,
    viewed integer NOT NULL DEFAULT 1
);
"""

alerts_user_query = """
CREATE TABLE IF NOT EXISTS alerts_users
(
    user_id bigint NOT NULL PRIMARY KEY,
    alert_viewed boolean NOT NULL DEFAULT false,
    ignore_alerts boolean NOT NULL default false
);
"""

# If you wish not to create one of these tables in the setup process
# Simply just remove that item from this list:
tables_to_create = [
    blacklist_query,
    command_stats_query,
    counting_query,
    leveling_member_query,
    leveling_guild_query,
    leveling_rewards_query,
    counters_query,
    dmreply_query,
    tags_query,
]


async def create_tables():
    """
    Runs all the table creation queries at once.
    To choose which tables to create add / remove the queries from the tables_to_create list
    """
    pool = await create_connection_pool()
    tasks = [pool.execute(table) for table in tables_to_create]
    await asyncio.gather(*tasks)
