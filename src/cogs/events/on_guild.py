import datetime

import discord
from discord.ext import commands

from core.models import WhyBot
from core.helpers.log import log_normal
from core.utils.client_functions import update_activity


class OnGuild(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """
        Called when the bot is removed from a guild
        It will update the bots activity
        It will also send a message to the the leave_alert_channel which is set in the config
        """
        await update_activity(self.client)
        leave_alert_channel = self.client.config["leave_alert_channel"]
        if leave_alert_channel == 0 or leave_alert_channel == None:
            return

        try:
            channel = self.client.get_channel(leave_alert_channel)
        except discord.errors.NotFound:
            return

        em = discord.Embed(
            title="Leave", description=f"Left: {guild.name}", color=discord.Color.red()
        )
        em.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=em)

        if self.client.config["LOGGING"]:
            await log_normal(f"Left Guild: '{guild.name}'")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        Called when the bot joins a guild
        It will update the bots activity
        It will also send a message to the the join_alert_channel which is set in the config
        """
        await update_activity(self.client)

        join_alert_channel = self.client.config["join_alert_channel"]
        if join_alert_channel == 0 or join_alert_channel == None:
            return

        try:
            channel = self.client.get_channel(join_alert_channel)
        except discord.errors.NotFound:
            return

        em = discord.Embed(
            title="Join",
            description=f"Joined: {guild.name}",
            color=discord.Color.green(),
        )
        em.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=em)

        if self.client.config["LOGGING"]:
            await log_normal(f"Joined Guild: '{guild.name}'")


def setup(client: WhyBot):
    client.add_cog(OnGuild(client))
