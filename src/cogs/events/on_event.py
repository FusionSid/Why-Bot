import datetime

import discord
from discord.ext import commands

from core.models.client import WhyBot
from core.helpers.logger import log_normal
from core.helpers.exception import InvalidDatabaseUrl
from core.utils.client_functions import update_activity, create_connection_pool


class OnEvent(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        This is the event that is called when a message is sent in a channel
        It will check if the bot has been mentioned in the message and if so
            it will reply with a message containing the guild prefix
        """

        if message.author.bot:
            return

        if (
            self.client.user.mentioned_in(message)
            and message.mention_everyone == False
            and message.reference is None
        ):
            em = discord.Embed(
                title=f"Hi, my name is {self.client.user.display_name}. Use /help for help",
                color=message.author.color,
            )
            return await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Runs when the bot is ready
        Prints a message to console and updates the bot's activity
        """
        self.client.console.print("\n[bold green]Bot is ready")

        await update_activity(self.client)

        online_alert_channel = self.client.config["online_alert_channel"]

        if online_alert_channel == 0 or online_alert_channel == None:
            return

        try:
            channel = await self.client.fetch_channel(online_alert_channel)
        except discord.errors.NotFound:
            return

        em = discord.Embed(
            title="Bot is online",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now(),
        )
        await channel.send(embed=em)

        try:
            self.client.db = await create_connection_pool()
        except ValueError:
            raise InvalidDatabaseUrl

        if self.client.config["LOGGING"]:
            await log_normal("Bot is Online")


def setup(client: WhyBot):
    client.add_cog(OnEvent(client))
