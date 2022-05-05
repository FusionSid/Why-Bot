import datetime

import discord
from discord.ext import commands

from utils import WhyBot
from log import get_last_errors


class ErrorLog(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.slash_command()
    @commands.is_owner()
    async def logs_file(self, ctx):
        file = discord.File("./log/logs.txt")
        await ctx.author.send(file=file)

    @commands.slash_command()
    @commands.is_owner()
    async def clear_logs_file(self, ctx):
        with open("./log/logs.txt", "r+") as f:
            f.truncate(0)

    @commands.slash_command()
    @commands.is_owner()
    async def get_last_error(self, ctx, limit: int = 1):
        """
        This command is used to get the most recent errors/error that the bot logged to the log file

        Help Info:
        ----------
        Category: Owner

        Usage: get_last_error [limit: int (default = 1)]
        """
        errors = await get_last_errors(count=limit)

        if errors is None:
            return await ctx.respond(
                "No recent error (you probably cleaned the file recently)"
            )

        em = discord.Embed(
            title="Last Error/s",
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow(),
        )
        for key, value in errors.items():
            em.add_field(name=key, value=value, inline=False)

        await ctx.respond(embed=em)


def setup(client: WhyBot):
    client.add_cog(ErrorLog(client))
