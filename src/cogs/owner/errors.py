import os
import datetime

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

import __main__
from core.models import WhyBot
from core.helpers.log import get_last_errors

LOGFILE_PATH = os.path.join(os.path.dirname(__main__.__file__), "logfiles/main.log")


class ErrorLog(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    error = SlashCommandGroup(
        "errors", "Commands for why bot error management. OWNER ONLY"
    )

    @error.command()
    @commands.is_owner()
    async def logs_file(self, ctx):
        file = discord.File(LOGFILE_PATH, "main.log")
        await ctx.respond(file=file, ephemeral=True)

    @error.command()
    @commands.is_owner()
    async def clear_logs_file(self, ctx):
        with open(LOGFILE_PATH, "r+") as f:
            f.truncate(0)
        await ctx.respond("Logfile Cleared", ephemeral=True)

    @error.command()
    @commands.is_owner()
    async def get_last_error(self, ctx, limit: int = 1):
        """
        This command is used to get the most recent errors/error that the bot logged to the log file
        """
        errors = await get_last_errors(count=limit)
        await ctx.defer()

        if errors is None:
            return await ctx.respond(
                "No recent error (you probably cleaned the file recently)",
                ephemeral=True,
            )

        em = discord.Embed(
            title="Last Error/s",
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow(),
        )
        for key, value in errors.items():
            em.add_field(name=key[:250], value=value[:1000], inline=False)

        await ctx.respond(embed=em, ephemeral=True)


def setup(client: WhyBot):
    client.add_cog(ErrorLog(client))
