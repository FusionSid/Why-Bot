import discord
from log import log_errors
import datetime
from utils import update_activity
from discord.ext import commands

class OnGuild(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        await update_activity(self.client)
        channel = self.client.get_channel(self.client.config['leave_alert_channel'])

        em = discord.Embed(title="Leave", description=f"Left: {guild.name}", color=discord.Color.red())
        em.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=em)
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.client.get_channel(self.client.config['join_alert_channel'])

        em = discord.Embed(title="Join", description=f"Joined: {guild.name}", color=discord.Color.green())
        em.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=em)
        await update_activity(self.client)

def setup(client):
    client.add_cog(OnGuild(client))