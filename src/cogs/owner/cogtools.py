import datetime

import discord
from discord.ext import commands

import log.log
from utils import WhyBot


class CogTools(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.slash_command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        """
        This command is used to reload a cog

        Help Info:
        ----------
        Category: Owner

        Usage: reload <extension: str>
        """
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title="Reload",
            description=f"{extension} successfully reloaded",
            color=ctx.author.color,
        )
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.respond(embed=embed)

    @commands.slash_command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        """
        This command is used to load a cog

        Help Info:
        ----------
        Category: Owner

        Usage: load <extension: str>
        """
        self.client.load_extension(f"cogs.{extension}")
        self.client.cogs_list.append(extension)
        embed = discord.Embed(
            title="Load",
            description=f"{extension} successfully loaded",
            color=ctx.author.color,
        )
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.respond(embed=embed)

    @commands.slash_command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """
        This command is used to unload a cog

        Help Info:
        ----------
        Category: Owner

        Usage: unload <extension: str>
        """

        self.client.unload_extension(f"cogs.{extension}")
        self.client.cogs_list.remove(extension)
        embed = discord.Embed(
            title="Unload",
            description=f"{extension} successfully unloaded",
            color=ctx.author.color,
        )
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.respond(embed=embed)

    @commands.slash_command()
    @commands.is_owner()
    async def listcogs(self, ctx):
        """
        This command lists the cogs that the bot has

        Help Info:
        ----------
        Category: Owner

        Usage: listcogs
        """
        return await ctx.respond("\n".join(self.client.cogs_list))

    @commands.slash_command(aliases=["rall"])
    async def reloadall(self, ctx):
        """
        This command is used to reload all the cogs

        Help Info:
        ----------
        Category: Owner

        Usage: reloadall
        """
        cogs = self.client.cogs_list

        exc_cogs = []
        for cog in exc_cogs:
            cogs.remove(f"cogs.{cog}")

        for cogs in cogs:
            try:
                self.client.reload_extension(cogs)
            except:
                continue
        await ctx.respond("All Reloaded")


def setup(client: WhyBot):
    client.add_cog(CogTools(client))
