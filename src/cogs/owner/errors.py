import datetime

import discord
from discord.ext import commands

from utils import WhyBot
from log import get_last_errors

class ErrorLog(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def logs_file(self, ctx):
        file = discord.File("./log/logs.txt")
        await ctx.author.send(file=file)


    @commands.command()
    async def clear_logs_file(self, ctx):
        with open("./log/logs.txt", 'r+') as f:
            f.truncate(0)


    @commands.command()
    async def get_last_error(self, ctx, limit : int = 1):
        errors = await get_last_errors(count=limit)

        if errors is None:
            return await ctx.send("No recent error (you probably cleaned the file recently)")

        em = discord.Embed(
            title="Last Error/s",
            color = ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )
        for key, value in errors.items():
            em.add_field(name=key, value=value, inline=False)

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(ErrorLog(client))