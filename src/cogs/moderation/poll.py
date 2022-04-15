import discord
from discord.ext import commands

from utils import blacklisted

class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Makes a Yah or Nah poll")
    @commands.check(blacklisted)
    async def yesorno(self, ctx, *, message):
        msg = await ctx.send(embed=discord.Embed(title="Yah or Nah?", description=message, color=ctx.author.color))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

def setup(client):
    client.add_cog(Poll(client))