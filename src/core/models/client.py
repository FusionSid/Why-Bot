""" (module) whybot

This contains the WhyBot commands.Bot client Class and the get_prefix function
"""

__version__ = "2.0.0"
__author__ = "FusionSid"
__licence__ = "MIT License"

import datetime
from typing import Optional

import discord
import aioredis
import asyncpg
from rich.console import Console
from discord.ext import commands

from core.helpers.checks import blacklist_check
from core.utils.formatters import format_seconds
from core.helpers.exception import UserAlreadyBlacklisted, UserAlreadyWhitelisted


class WhyBot(commands.Bot):
    """
    The Why Bot Class (subclass of: `discord.ext.commands.Bot`)
    """

    def __init__(self, config: dict):

        self.cogs_list = []
        self.db: asyncpg.Pool = None
        self.redis: aioredis.Redis = None

        self.config = config
        self.version = __version__
        self.console = Console()
        self.last_login_time = datetime.datetime.now()

        intents = discord.Intents.all()
        allowed_mentions = discord.AllowedMentions(everyone=False)

        super().__init__(
            intents=intents,
            help_command=None,
            case_insensitive=True,
            command_prefix="?",  # gonna use slash commands anyways so this only for owner cmds
            owner_id=config["BOT_OWNER_ID"],
            allowed_mentions=allowed_mentions,
        )

    @property
    async def uptime(self):
        """
        This function returns the uptime for the bot.

        Returns:
            str : Formated string with the uptime
        """
        time_right_now = datetime.datetime.now()
        seconds = (time_right_now - self.last_login_time).total_seconds()

        time = await format_seconds(seconds)
        return time

    @property
    def get_why_emojies(self):
        """
        This function returns the emojis for the bot

        Returns:
            Dict : A dictionary of emojis
        """
        emojis_dict = {}

        for emoji in self.get_guild(763348615233667082).emojis:
            emojis_dict[emoji.name] = str(emoji)

        return emojis_dict

    async def get_blacklisted_users(self, reasons=False):
        users = await self.db.fetch("SELECT * FROM blacklist;")

        if reasons:
            return users

        return [int(user[0]) for user in users]

    async def reset_redis_blacklisted_cache(self):
        await self.redis.delete("blacklisted")
        users = [int(user) for user in await self.get_blacklisted_users()]
        if len(users):
            await self.redis.lpush("blacklisted", *users)
            await self.redis.expire("blacklisted", datetime.timedelta(days=5))

        await self.redis.lpush("blacklisted", 0)
        await self.redis.expire("blacklisted", datetime.timedelta(days=5))

    async def blacklist_user(self, user_id: int, reason: Optional[str] = None):
        is_user_blacklisted = user_id in await self.get_blacklisted_users()
        if is_user_blacklisted:  # check if they are already blacklisted
            raise UserAlreadyBlacklisted

        if reason is not None:
            await self.db.execute(
                "INSERT INTO public.blacklist (user_id) VALUES ($1)", user_id
            )
        else:
            await self.db.execute(
                "INSERT INTO public.blacklist (user_id, reason) VALUES ($1, $2)",
                user_id,
                reason,
            )

        # Reset cache
        await self.reset_redis_blacklisted_cache()

    async def whitelist_user(self, user_id: int):
        is_user_blacklisted = user_id in await self.get_blacklisted_users()
        if not is_user_blacklisted:  # check if they are already whitelisted
            raise UserAlreadyWhitelisted

        await self.db.execute("DELETE FROM public.blacklist WHERE user_id=$1", user_id)

        # Reset cache
        await self.reset_redis_blacklisted_cache()
