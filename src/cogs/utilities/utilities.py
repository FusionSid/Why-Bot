import inspect
import datetime

import discord
from discord.ext import commands
from discord.commands import slash_command

import log.log
from utils import WhyBot, blacklisted
from utils.views import CalculatorView


class Utilities(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.command(name="calculate", description="Interactive button calculator")
    @commands.check(blacklisted)
    async def calculate(self, ctx):
        """
        This command is used to show an interactive button calculator

        Help Info:
        ----------
        Category: Utilities

        Usage: calculate
        """
        view = CalculatorView(ctx)
        message = await ctx.send("```\n```", view=view)
        res = await view.wait()
        if res:
            for i in view.children:
                i.disabled = True
        return await message.edit(view=view)


    @commands.command()
    @commands.check(blacklisted)
    async def invite(self, ctx):
        """
        This command is used to make a 10 day invite for the server

        Help Info:
        ----------
        Category: Utilities

        Usage: invite
        """
        link = await ctx.channel.create_invite(max_age=10)
        await ctx.send(link)

    @commands.command()
    @commands.check(blacklisted)
    async def botinvite(self, ctx):
        """
        This command is used to get the invite link for the bot

        Help Info:
        ----------
        Category: Utilities

        Usage: botinvite
        """
        await ctx.send(
            embed=discord.Embed(
                title="Invite **Why?** to your server:",
                description="[Why Invite Link](https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands)",
                color=ctx.author.color,
            )
        )

    @commands.command()
    @commands.check(blacklisted)
    async def avatar(self, ctx, member: discord.Member = None):
        """
        This command is used to get the avatar for a member

        Help Info:
        ----------
        Category: Utilities

        Usage: avatar [member: discord.Member (default=You)]
        """
        if member is None:
            member = ctx.author
        em = discord.Embed(title=f"{member.name}'s Avatar:", color=member.color)
        em.set_image(url=member.avatar.url)
        await ctx.send(embed=em)


def setup(client: WhyBot):
    client.add_cog(Utilities(client))
