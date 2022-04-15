from datetime import datetime

import discord
from discord.ext import commands

import log.log
from utils import WhyBot, blacklisted

class Why(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(blacklisted)
    async def suggest(self, ctx, *, suggestion):
        """
        This command is used to make a suggestion for the bot

        Help Info:
        ----------
        Category: Utilities

        Usage: suggest <suggestion: str>
        """
        if self.client.config.suggestion_channel == 0 or self.client.config.suggestion_channel == None: return await ctx.send("Bot owner has disabled suggestions")

        try:
            channel = await self.client.fetch_channel(self.client.config.suggestion_channel)
        except discord.errors.NotFound:
            return await ctx.send("Bot owner has disabled suggestions")

        em = discord.Embed(
            title=f"Suggestion",
            description=suggestion,
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow(),
        )
        em.add_field(name=f"by: {ctx.author.name}", value=f"{ctx.author.id}")
        message = await channel.send(embed=em)
        await message.add_reaction("✅")
        await message.add_reaction("❌")


    @commands.command(description = "Report a bug")
    @commands.check(blacklisted)
    async def bug(self, ctx, *, bug):
        em = discord.Embed(title="REPORT", color=ctx.author.color)
        em.timestamp = datetime.utcnow()
        em.description = "Bug Report"
        em.add_field(name="Bug", value=bug)
        em.add_field(name="Report By:", value=ctx.author.name)

        try:
            channel = await self.client.fetch_channel(self.client.config.bug_report_channel)
        except discord.errors.NotFound:
            return await ctx.send("Bot owner has bug reports")

        await channel.send(content=ctx.author.id, embed=em)

def setup(client):
    client.add_cog(Why(client))