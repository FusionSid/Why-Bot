import os
import datetime

import discord
import aiofiles
from discord.commands import SlashCommandGroup
from discord.ext import commands

import __main__
from core.models import WhyBot
from core.helpers.views import ErrorView
from core.helpers.log import get_last_errors
from core.utils.client_functions import GUILD_IDS

LOGFILE_PATH = os.path.join(os.path.dirname(__main__.__file__), "logfiles/main.log")


class ErrorLog(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    error = SlashCommandGroup(
        "errors", "Commands for why bot error management. OWNER ONLY"
    )

    @error.command(guild_ids=GUILD_IDS, description="Send the whole logs file")
    @commands.is_owner()
    async def logs_file(self, ctx: discord.ApplicationContext):
        file = discord.File(LOGFILE_PATH, "main.log")
        await ctx.respond(file=file, ephemeral=True)

    @error.command(guild_ids=GUILD_IDS, description="Clear the logs file")
    @commands.is_owner()
    async def clear_logs_file(self, ctx: discord.ApplicationContext):
        async with aiofiles.open(LOGFILE_PATH, "r+") as f:
            await f.truncate(0)
        await ctx.respond("Logfile Cleared", ephemeral=True)

    @error.command(
        guild_ids=GUILD_IDS, description="Get the last error from the log file"
    )
    @commands.is_owner()
    async def get_last_error(self, ctx: discord.ApplicationContext, limit: int = 1):
        """This command is used to get the most recent errors/error that the bot logged to the log file"""

        await ctx.defer()
        if limit >= 24:
            return await ctx.respond(
                "To big of a number",
                ephemeral=True,
            )

        errors = await get_last_errors(count=limit)

        if errors is None:
            return await ctx.respond(
                "No recent error (you probably cleaned the file recently)",
                ephemeral=True,
            )

        em = discord.Embed(
            title=f"Last {str(limit)+' Errors' if limit > 1 else 'Error'}",
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow(),
        )
        if limit == 1:
            title = list(errors.keys())[0]
            err = list(errors.values())[0]
            em.description = f"**{title[:220]}**```py\n{err[:1900]}```"

            view = ErrorView(self.client.owner_id, f"{title}{err}")
            return await ctx.respond(embed=em, ephemeral=True, view=view)

        for key, value in errors.items():
            em.add_field(
                name=f"{key[:220]} **(read logfile for full)**"
                if len(key) >= 220
                else key,
                value=f"```py\n{value[:980]}```\n**(read logfile for full)**"
                if len(value) >= 980
                else f"```py\n{value}```",
                inline=False,
            )

        await ctx.respond(embed=em, ephemeral=True)


def setup(client: WhyBot):
    client.add_cog(ErrorLog(client))
