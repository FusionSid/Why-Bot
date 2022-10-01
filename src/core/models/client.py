""" (module) whybot

This contains the WhyBot commands.Bot client Class and the get_prefix function
"""

__version__ = "2.0.0"
__author__ = "FusionSid"
__licence__ = "MIT License"

import datetime

import discord
from rich.console import Console
from discord.ext import commands

from core.utils import format_seconds


class WhyBot(commands.Bot):
    """
    The Why Bot Class (subclass of: `discord.ext.commands.Bot`)
    """

    def __init__(self, config: dict):

        self.cogs_list = []
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
            command_prefix="?",  # gonna use slash commands anyways
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
