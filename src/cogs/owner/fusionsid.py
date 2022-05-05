import discord
import json
from discord.ext import commands

from utils import Config, WhyBot

class FusionSid(commands.Cog):
    def __init__(self, client:WhyBot):
        self.client = client


    @commands.slash_command()
    @commands.is_owner()
    async def reload_config(self, ctx):
        with open("./config.json") as f:
            config = Config(json.load(f))
        
        self.client.config = config
        await ctx.respond(embed=discord.Embed(title="Reloaded Config", color=ctx.author.color))


    @commands.slash_command()
    @commands.is_owner()
    async def get_config(self, ctx):
        with open("./config.json") as f:
            config = json.load(f)

        em = discord.Embed(title="Why Bot Config", description="Channel config for why bot", color=ctx.author.color)

        for key, value in config.items():
            if value is None:
                val = "None / Not Set"
            elif value is not None:
                try:
                    channel = await self.client.fetch_channel(value)
                    val = channel.mention
                except discord.errors.NotFound:
                    val = "None / Not Set"

            em.add_field(name=key, value=val)

        await ctx.respond(embed=em)

def setup(client):
    client.add_cog(FusionSid(client))
        