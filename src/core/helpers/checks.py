from datetime import timedelta

import aioredis

from core.utils.asyncpg_context import asyncpg_connect
from core.utils.client_functions import get_why_config


async def blacklist_check(user_id):
    """
    returns true if the user is not blacklisted
    """
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
        users = [int(user) for user in data]
        if len(users):
            await redis.lpush("blacklisted", *users)
            await redis.expire("blacklisted", timedelta(hours=12))
        return not str(user_id) in users


async def run_bot_checks(ctx):
    blacklisted_check = await blacklist_check(ctx.author.id)
    all_checks_successful = all([blacklisted_check])

    return all_checks_successful
