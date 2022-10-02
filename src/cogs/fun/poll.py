import asyncio
import datetime
import time as py_time

import discord
from discord.utils import get
from discord.ext import commands


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Makes a Yah or Nah poll")
    async def yesorno(self, ctx, *, message):
        msg = await ctx.respond(
            embed=discord.Embed(
                title="Yah or Nah?", description=message, color=ctx.author.color
            )
        )
        msg = await msg.original_message()
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")


def setup(client):
    client.add_cog(Poll(client))
