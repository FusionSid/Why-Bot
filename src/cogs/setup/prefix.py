import discord
import aiosqlite
from discord.ext import commands

import log.log
from utils import get_prefix, WhyBot, blacklisted


class Prefix(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client


    @commands.command(name="prefix", description="Shows the bots prefix")
    @commands.check(blacklisted)
    async def prefix(self, ctx: commands.Context):
        """
        This command is used to show the prefix for the bot

        Help Info:
        ----------
        Category: Settings

        Usage: prefix
        """
        prefix = await get_prefix(self.client, ctx.message)
        em = discord.Embed(title=f"Hi, my prefix is `{prefix}`", color=ctx.author.color)
        return await ctx.send(embed=em)


    @commands.command(name="setprefix", description="Sets the guild prefix for the bot")
    @commands.check(blacklisted)
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx: commands.Context, prefix: str):
        """
        This command is used to set the guild prefix for the bot

        Help Info:
        ----------
        Category: Owner

        Usage: setprefix <prefix: str>
        """
        async with aiosqlite.connect("database/main.db") as db:
            await db.execute(
                """UPDATE Prefix SET prefix=? WHERE guild_id=?""",
                (prefix, ctx.guild.id),
            )

            await db.commit()

        await ctx.send(
            embed=discord.Embed(
                title="Prefix Update",
                description=f"Prefix changed to `{prefix}`",
                color=ctx.author.color,
            )
        )


def setup(client: WhyBot):
    client.add_cog(Prefix(client))
