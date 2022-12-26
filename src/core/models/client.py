""" (module) whybot

This contains the WhyBot commands.Bot client class and its class methods
Its also where most init tasks are done
"""

__author__ = "FusionSid"
__licence__ = "MIT License"

import datetime
from typing import Optional

import discord
import aioredis
import asyncpg
from pycord.ext import ipc
from rich.console import Console
from discord.ext import commands

from core.utils import format_seconds
from core.helpers import UserAlreadyBlacklisted, UserAlreadyWhitelisted


class WhyBot(commands.Bot):
    """
    The Why Bot Class (subclass of: `discord.ext.commands.Bot`)

    Parameters:
        config (dict): The parsed result of the config.yaml file
            this is usualy obtained from the get_why_config function

    Attributes:
        db Optional[asyncpg.Pool]: The connection to the postgres db
        redis Optional[aioredis.Redis]: The connection to the redis db
        config (dict): The bots config
        version (str): the bots version
        console (rich.console.Console): a Console object useful for rich printing
        last_login_time (datetime.datetime.now()): The last time the bot started, used for uptime

        + all the ones inherited from `discord.ext.commands.Bot`
    """

    def __init__(self, config: dict, version: str):

        self.cogs_list = {}
        self.db: asyncpg.Pool
        self.redis: aioredis.Redis

        self.config = config
        self.version = version
        self.console = Console()
        self.last_login_time = datetime.datetime.now()

        intents = discord.Intents.all()
        allowed_mentions = discord.AllowedMentions(everyone=False)

        super().__init__(
            intents=intents,
            help_command=None,
            case_insensitive=True,
            command_prefix=config.get("DEFAULT_PREFIX"),
            owner_id=config["BOT_OWNER_ID"],
            debug_guilds=config.get("DEBUG_GUILDS")
            if config.get("DEBUG_GUILD_MODE")
            else None,
            allowed_mentions=allowed_mentions,
        )
        self.ipc = ipc.Server(
            self, secret_key=config["IPC_KEY"], host=config["IPC_HOST"]
        )

    @property
    async def uptime(self) -> str:
        """
        This property returns the uptime for the bot.

        Returns:
            str : Formated string with the uptime
        """
        time_right_now = datetime.datetime.now()
        seconds = int((time_right_now - self.last_login_time).total_seconds())

        time = await format_seconds(seconds)
        return time

    @property
    def get_why_emojies(self) -> dict:
        """
        This property returns the emojis for the bot
            these emojis are the ones in the Why Bot guild

        Returns:
            dict : A dictionary of emojis
        """
        emojis_dict = {}

        for emoji in self.get_guild(self.config.get("MAIN_GUILD")).emojis:
            emojis_dict[emoji.name] = str(emoji)

        return emojis_dict

    async def get_blacklisted_users(
        self, reasons: Optional[bool] = False
    ) -> list[int] | list[asyncpg.protocol.Record]:
        """
        this function returns the blacklisted users for the bot from the db
            this is used when the cache is empty or needs to be updated

        Parameters:
            reasons (Optional[bool]): If this is True it will return a list
                blacklisted users with their userids and reason for being banned
                This default to false

        Returns:
            list[int] | list[asyncpg.Record]: it will return a list with user ids of people blacklisted
                but if reasons is True it will be a list of asyncpg.Records which will look like: list[list[int, str]]
        """
        users = await self.db.fetch("SELECT * FROM blacklist;")

        if reasons:
            return users

        return [int(user[0]) for user in users]

    async def reset_redis_blacklisted_cache(self):
        """This function resets the blacklisted cache for the bot"""

        await self.redis.delete("blacklisted")
        users = [int(user) for user in await self.get_blacklisted_users()]
        if users:
            await self.redis.lpush("blacklisted", *users)
            await self.redis.expire("blacklisted", datetime.timedelta(days=5))

        await self.redis.lpush("blacklisted", 0)
        await self.redis.expire("blacklisted", datetime.timedelta(days=5))

    async def blacklist_user(self, user_id: int, reason: Optional[str] = None):
        """
        This function is used to black list a user from using the bot

        Parameters:
            user_id (int): the user id to ban
            reason (Optional[str]): the optional reason why the user was blacklisted

        Raises:
            UserAlreadyBlacklisted: If the user is already blacklisted
        """
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
        """
        if a user was blacklisted from the bot it will whitelist them

        Parameters:
            user_id (int): The user_id to unban

        Raises:
            UserAlreadyWhitelisted: If the user is already whitelisted
        """
        is_user_blacklisted = user_id in await self.get_blacklisted_users()
        if not is_user_blacklisted:  # check if they are already whitelisted
            raise UserAlreadyWhitelisted

        await self.db.execute("DELETE FROM public.blacklist WHERE user_id=$1", user_id)

        # Reset cache
        await self.reset_redis_blacklisted_cache()

    @staticmethod
    async def on_ipc_error(endpoint, error):
        print(endpoint, "raised", error)
