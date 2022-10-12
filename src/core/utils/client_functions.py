""" (module) client_functions
Useful functions for the WhyBot client
"""

import os
import json

import yaml
import discord
import asyncpg
import aioredis
from discord.ext import commands

import __main__
from core.helpers.exception import ConfigNotFound


async def update_activity(client: commands.Bot):
    """
    Updates the bot's activity with the amount of servers

    Parameters:
        client (WhyBot): The bot to update presence for
    """

    await client.change_presence(
        activity=discord.Game(f"On {len(client.guilds)} servers! | /help")
    )


def get_why_config() -> dict:
    """
    Gets the why bot config

    Returns:
        dict: The parsed result of config.yaml file
    """

    path = os.path.join(os.path.dirname(__main__.__file__), "config.yaml")

    if not os.path.exists(path):
        raise ConfigNotFound

    with open(path) as f:
        data = yaml.load(f, Loader=yaml.Loader)

    return data


async def create_connection_pool() -> asyncpg.Pool:
    """
    Creates a connection pool to the bots postgresql db

    Returns:
        asyncpg.Pool: an asyncpg connection pool.
    """

    async def init(conn):
        # Set up auto json encoder/decoder:
        await conn.set_type_codec(
            "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
        )

    config = get_why_config()
    pool = await asyncpg.create_pool(dsn=config["DATABASE_URL"], init=init)

    return pool


async def create_redis_connection() -> aioredis.Redis:
    """
    Creates a connection the the redis database

    Returns:
        aioredis.Redis: the connection to the db
    """
    config = get_why_config()

    redis = aioredis.from_url(
        config["REDIS_URI"],
        decode_responses=True,
        password=config["REDIS_PASSWORD"],
        port=6379,
    )

    return redis
