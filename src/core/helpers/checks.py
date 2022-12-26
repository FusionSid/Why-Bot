""" (module) checks
This module contains checks that will be run before most commands in the @commands.check() decorator
"""

import asyncio
import datetime

import aioredis
from discord.ext import commands
from discord import ApplicationContext  # for the autocomplete

from .client_functions import get_why_config
from core.utils import asyncpg_connect


async def blacklist_check(user_id: int) -> bool:
    """returns true if the user is not blacklisted"""

    config = get_why_config()

    redis_url = config["REDIS_URI"]
    redis_password = config["REDIS_PASSWORD"]
    database_url = config["DATABASE_URL"]

    # Caching
    redis = aioredis.from_url(
        redis_url, decode_responses=True, password=redis_password, port=6379
    )

    if await redis.exists("blacklisted"):  # if the key exists then do this:
        cached_blacklisted_users = await redis.lrange("blacklisted", 0, -1)
        return not str(user_id) in cached_blacklisted_users

    async with asyncpg_connect(database_url) as conn:
        data = await conn.fetch("SELECT * FROM blacklist;")
        users = [int(user[0]) for user in data]
        if users:
            await redis.lpush("blacklisted", *users)
            await redis.expire("blacklisted", datetime.timedelta(hours=12))
        return not str(user_id) in users


async def plugin_enabled(cog: commands.Cog) -> bool:
    # TODO 𐐘
    cog_name = cog.__cog_name__
    return True


async def update_stats(ctx: ApplicationContext):
    config = get_why_config()
    database_url = config["DATABASE_URL"]

    async with asyncpg_connect(database_url) as conn:
        data = await conn.fetch(
            "SELECT * FROM command_stats WHERE user_id=$1 AND command_name=$2",
            ctx.author.id,
            ctx.command.name,
        )
        if data:
            await conn.execute(
                "UPDATE command_stats SET usage_count=$1 WHERE user_id=$2 AND"
                " command_name=$3",
                data[0][3] + 1,
                ctx.author.id,
                ctx.command.name,
            )
        else:
            await conn.execute(
                "INSERT INTO command_stats (user_id, command_name, usage_count) VALUES"
                " ($1, $2, $3)",
                ctx.author.id,
                ctx.command.name,
                1,
            )


async def run_bot_checks(ctx: ApplicationContext):

    blacklisted_check = await blacklist_check(ctx.author.id)
    plugin_enabled_check = await plugin_enabled(ctx.cog)
    all_checks_successful = all([blacklisted_check, plugin_enabled_check])

    asyncio.get_event_loop().create_task(update_stats(ctx))

    return all_checks_successful
