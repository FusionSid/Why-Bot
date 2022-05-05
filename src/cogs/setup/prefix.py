import discord
import aiosqlite
from discord.ext import commands

import log.log
from utils import WhyBot, blacklisted

async def get_prefix(guild_id):
    async with aiosqlite.connect("database/main.db") as db:
        cur = await db.execute(
            "SELECT * FROM Prefix WHERE guild_id=?", (guild_id,)
        )
        prefix = await cur.fetchall()

        if len(prefix) == 0:
            prefix = "?"
            await db.execute(
                "INSERT INTO Prefix (guild_id, prefix) VALUES (?, ?)",
                (guild_id, prefix),
            )
            await db.commit()
        else:
            prefix = prefix[0][1]

    return prefix


class Prefix(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client


    @commands.slash_command(name="prefix", description="Shows the bots prefix")
    @commands.check(blacklisted)
    async def prefix(self, ctx:discord.ApplicationContext):
        """
        This command is used to show the prefix for the bot

        Help Info:
        ----------
        Category: Settings

        Usage: prefix
        """
        prefix = await get_prefix(ctx.guild.id)
        em = discord.Embed(title=f"Hi, my prefix is `{prefix}`", color=ctx.author.color)
        return await ctx.respond(embed=em)


    @commands.slash_command(name="setprefix", description="Sets the guild prefix for the bot")
    @commands.check(blacklisted)
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, prefix: str):
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

        await ctx.respond(
            embed=discord.Embed(
                title="Prefix Update",
                description=f"Prefix changed to `{prefix}`",
                color=ctx.author.color,
            )
        )


def setup(client: WhyBot):
    client.add_cog(Prefix(client))
