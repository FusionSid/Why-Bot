import asyncio

import asyncpg


async def setup_counting(db: asyncpg.Pool, guild_id: int):
    """
    Setup counting for the guild. basically adds to the counting table

    Parameters:
        db (asyncpg.Pool): The database connection pool
        guild_id (int): the id of the guild to create a row for
    """
    try:
        await db.execute(
            "INSERT INTO counting (guild_id, high_score) VALUES ($1, 0)", guild_id
        )
    except asyncpg.UniqueViolationError:
        return


async def setup_leveling_guild(db: asyncpg.Pool, guild_id: int):
    """
    Setup leveling for the guild. Creates a row with the default values in the leveling table

    Parameters:
        db (asyncpg.Pool): The database connection pool
        guild_id (int): the id of the guild to create a row for
    """
    default_data = [
        guild_id,
        False,
        "default",
        "black",
        None,
        "black",
        "green",
        [],
        [],
        "GG {member.mention} you just leveled up to {level}",
        True,
        "20",
    ]
    query = """
    INSERT INTO leveling_guild (
        guild_id, plugin_enabled, 
        text_font, text_color,
        background_image, background_color, progress_bar_color, 
        no_xp_roles, no_xp_channels, 
        level_up_text, level_up_enabled, per_minute
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
    """
    try:
        await db.execute(query, *default_data)
    except asyncpg.UniqueViolationError:
        return


async def setup_tickets(db: asyncpg.Pool, guild_id: int):
    """
    Setup ticketing for the guild.

    Parameters:
        db (asyncpg.Pool): The database connection pool
        guild_id (int): the id of the guild to create a row for
    """
    default_data = [guild_id, [], [], False, None, []]
    try:
        await db.execute(
            """INSERT INTO ticket_guild (
                guild_id, users_allowed, ping_roles, create_button, category, banned_users
            ) VALUES ($1, $2, $3, $4, $5, $6)""",
            *default_data,
        )
    except asyncpg.UniqueViolationError:
        return


async def create_db_tables(db: asyncpg.Pool, guild_id: int):
    """
    Function for running all the setup functions at once
    This will be used when a new guild is joined and will help with not having to run these functions later

    Parameters:
        db (asyncpg.Pool): The database connection pool
        guild_id (int): the id of the guild to setup
    """

    things_to_setup = [setup_counting, setup_leveling_guild, setup_tickets]
    tasks = [setup_function(db, guild_id) for setup_function in things_to_setup]
    await asyncio.gather(*tasks)
