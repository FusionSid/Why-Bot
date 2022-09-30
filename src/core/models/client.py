""" (module) whybot

This contains the WhyBot commands.Bot client Class and the get_prefix function
"""

__version__ = "2.0.0"
__author__ = "FusionSid"
__licence__ = "MIT License"

import json
import datetime

import discord
from rich.console import Console
from discord.ext import commands


class WhyBot(commands.Bot):
    """
    The Why Bot Class (subclass of: `discord.ext.commands.Bot`)

    Parameters
        void
    """

    def __init__(self):

        self.cogs_list = []
        self.version = __version__
        self.console = Console()
        self.last_login_time = datetime.datetime.now()

        intents = discord.Intents.all()
        allowed_mentions = discord.AllowedMentions(everyone=False)

        super().__init__(
            intents=intents,
            help_command=None,
            case_insensitive=True,
            owner_id=624076054969188363,  # The bot owner's ID
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
        seconds = int((time_right_now - self.last_login_time).total_seconds())
        time = f"{seconds}s"
        if seconds > 60:
            minutes = seconds - (seconds % 60)
            seconds = seconds - minutes
            minutes = int(minutes / 60)
            time = f"{minutes}min {seconds}s"
            if minutes > 60:
                hoursglad = minutes - (minutes % 60)
                hours = int(hoursglad / 60)
                minutes = minutes - (hours * 60)
                time = f"{hours}h {minutes}min {seconds}s"
        return time

    @property
    def get_why_emojies(self):
        """
        This function returns the emojis for the bot

        Returns:
            Dict : A dictionary of emojis
        """
        return {"why": "<:why:932912321544728576>"}

    @property
    def blacklisted_users(self):
        """
        This function returns all the blacklisted users

        Returns:
            List : List of blacklisted users
        """
        with open("database/blacklisted.json") as f:
            data = json.load(f)
        return data

    async def blacklist_user(self, user_id: int):
        """
        This function is used to blacklist a user so they cant use why bot anymore

        Parameters
            :param: user_id (int) : The id for the user. This will be appended to the List of blacklisted users
        """
        with open("database/blacklisted.json") as f:
            data = json.load(f)

        if user_id not in data:
            data.append(user_id)

        with open("database/blacklisted.json", "w") as f:
            json.dump(data, f, indent=4)

    async def whitelist_user(self, user_id: int):
        """
        This function is used to whitelist a user so they can use why bot

        Parameters
            :param: user_id (int) : The id for the user. This will be appended to the List of blacklisted users
        """
        with open("database/blacklisted.json") as f:
            data = json.load(f)

        if user_id in data:
            data.remove(user_id)

        with open("database/blacklisted.json", "w") as f:
            json.dump(data, f, indent=4)
