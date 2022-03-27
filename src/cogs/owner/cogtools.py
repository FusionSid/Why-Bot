import datetime

import discord
from discord.ext import commands

from utils import WhyBot


class CogTools(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title="Reload",
            description=f"{extension} successfully reloaded",
            color=ctx.author.color,
        )
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title="Load",
            description=f"{extension} successfully loaded",
            color=ctx.author.color,
        )
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title="Unload",
            description=f"{extension} successfully unloaded",
            color=ctx.author.color,
        )
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def listcogs(self, ctx):
        return await ctx.send("\n".join(self.client.cogs_list))

    @commands.command(aliases=["rall"])
    async def reloadall(self, ctx):
        cogs = self.client.cogs_list

        exc_cogs = []
        for cog in exc_cogs:
            cogs.remove(f"cogs.{cog}")

        for cogs in cogs:
            try:
                self.client.reload_extension(cogs)
            except:
                continue
        await ctx.send("All Reloaded")


def setup(client: WhyBot):
    client.add_cog(CogTools(client))
