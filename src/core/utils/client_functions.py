""" (module) client_functions

Useful functions for the WhyBot client
"""
import os

import yaml
import discord
import asyncpg
from discord.ext import commands

import __main__
from core.helpers.exception import ConfigNotFound


async def update_activity(client: commands.Bot):
    """Updates the bot's activity"""
    await client.change_presence(
        activity=discord.Game(f"On {len(client.guilds)} servers! | ?help")
    )


def get_why_config() -> dict:
    """
    Gets the why config
    """
    path = os.path.join(os.path.dirname(__main__.__file__), "config.yaml")

    if not os.path.exists(path):
        raise ConfigNotFound

    with open(path) as f:
        data = yaml.load(f, Loader=yaml.Loader)

    return data


async def create_connection_pool() -> asyncpg.Pool:
    config = get_why_config()
    pool = await asyncpg.create_pool(dsn=config["DATABASE_URL"])

    return pool
