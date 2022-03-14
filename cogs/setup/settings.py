import discord
from discord.ext import commands
from discord import slash_command

from main import get_prefix
from log import log_errors

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name="prefix", description="Shows the bots prefix")
    async def prefix(self, ctx):
        prefix = await get_prefix(self.client, ctx.message)
        em = discord.Embed(
            title=f"Hi, my prefix is `{prefix}`", 
            color=ctx.author.color
        )
        return await ctx.respond(embed=em)

def setup(client):
    client.add_cog(Settings(client))