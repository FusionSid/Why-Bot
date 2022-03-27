import datetime

import discord
from discord.ext import commands

from log import log_errors
from utils import update_activity, WhyBot


class OnGuild(commands.Cog):
    def __init__(self, client : WhyBot):
        self.client = client
    

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        """
        Called when the bot is removed from a guild
        It will update the bots activity
        It will also send a message to the the leave_alert_channel which is set in the config
        """
        await update_activity(self.client)
        try:
            channel = self.client.get_channel(self.client.config.leave_alert_channel)
        except Exception as err:
            return

        em = discord.Embed(title="Leave", description=f"Left: {guild.name}", color=discord.Color.red())
        em.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=em)
    
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        Called when the bot joins a guild
        It will update the bots activity
        It will also send a message to the the join_alert_channel which is set in the config
        """
        channel = self.client.get_channel(self.client.config.join_alert_channel)

        em = discord.Embed(title="Join", description=f"Joined: {guild.name}", color=discord.Color.green())
        em.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=em)
        await update_activity(self.client)


def setup(client : WhyBot):
    client.add_cog(OnGuild(client))