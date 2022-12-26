import datetime

import discord
from discord.ext import commands

from core.models import NewTicketView, WhyBot
from core.helpers import (
    InvalidDatabaseUrl,
    log_normal,
    update_activity,
    create_connection_pool,
    create_redis_connection,
)


class OnEvent(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        This is the event that is called when a message is sent in a channel
        It will check if the bot has been mentioned in the message and if so
            it will reply with a message containing the guild prefix
        """

        if message.author.bot:
            return

        if (
            self.client.user.mentioned_in(message)
            and message.mention_everyone is False
            and message.reference is None
        ):
            em = discord.Embed(
                title=f"Hi, my name is {self.client.user.display_name}. Use </help:0> for help",
                color=message.author.color,
            )
            return await message.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Runs when the bot is ready
        Prints a message to console and updates the bot's activity
        """
        # update the bots activity
        await update_activity(self.client)

        # (try to) connect to the postgresql database
        try:
            self.client.db = await create_connection_pool()
        except ValueError:
            raise InvalidDatabaseUrl

        # connect to redis db and reset the cache
        self.client.redis = await create_redis_connection()
        await self.client.redis.flushall()  # reset cache

        # Send online alert
        online_alert_channel = self.client.config.get("online_alert_channel")
        if online_alert_channel in (0, None):
            return

        try:
            channel = await self.client.fetch_channel(online_alert_channel)
        except discord.errors.NotFound:
            return

        await self.__setup_ticket_buttons()

        await channel.send(
            embed=discord.Embed(
                title="Bot is online",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now(),
            )
        )

        if self.client.config.get("LOGGING"):
            await log_normal("Bot is Online")

        # print to console that its ready
        self.client.console.print("\n[bold green]Bot is ready")

    async def __setup_ticket_buttons(self):
        guilds = await self.client.db.fetch(
            "SELECT guild_id FROM ticket_guild WHERE create_button=true"
        )
        for guild_id in map(lambda x: x[0], guilds):
            self.client.add_view(NewTicketView(guild_id, self.client))


def setup(client: WhyBot):
    client.add_cog(OnEvent(client))
