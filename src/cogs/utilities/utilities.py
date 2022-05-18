import datetime

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

import log.log
from utils import WhyBot, blacklisted
from utils.views import CalculatorView


class Utilities(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
    
    
    utilities = SlashCommandGroup("utilities", "Utility Commands")


    @utilities.command(name="calculate", description="Interactive button calculator")
    @commands.check(blacklisted)
    async def calculate(self, ctx):
        """
        This command is used to show an interactive button calculator

        Help Info:
        ----------
        Category: Utilities

        Usage: calculate
        """
        await ctx.defer()
        view = CalculatorView(ctx)
        message = await ctx.respond("```\n```", view=view)
        res = await view.wait()
        if res:
            for i in view.children:
                i.disabled = True
        return await message.edit(view=view)


    @utilities.command(name="invite", description="Create 10 day invite for the server")
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
        await ctx.respond(link)


    @utilities.command(name="botinvite", description="Get a link to invite Why-Bot to the server")
    @commands.check(blacklisted)
    async def botinvite(self, ctx):
        """
        This command is used to get the invite link for the bot

        Help Info:
        ----------
        Category: Utilities

        Usage: botinvite
        """
        interaction = await ctx.respond(
            embed=discord.Embed(
                title="Invite **Why?** to your server:",
                description="[Why Invite Link](https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands)",
                color=  ctx.author.color,
            )
        )
        message = await interaction.original_message()
        await message.add_reaction("🔗")
        react_check = lambda reaction, user: user.id == ctx.author.id and reaction.emoji == "🔗" and reaction.message.id == message.id
        await self.client.wait_for("reaction_add", check=react_check, timeout=30.0)
        await ctx.respond("https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands")


    @utilities.command(name="avatar", description="Get the avatar for a member")
    @commands.check(blacklisted)
    async def avatar(self, ctx, member: discord.Member = None):
        """
        This command is used to get the avatar for a member

        Help Info:
        ----------
        Category: Utilities

        Usage: avatar [member: discord.Member]
        """
        if member is None:
            member = ctx.author
        em = discord.Embed(title=f"{member.name}'s Avatar:", color=member.color)
        em.set_image(url=member.avatar.url)
        await ctx.respond(embed=em)
        

    @utilities.command(name="invites", description="Get the amount of people that a member has invited to the server")
    @commands.check(blacklisted)
    async def invites(self, ctx, member: discord.Member = None):
        """
        This command is used to get the amount of people that a member has invited to the server

        Help Info:
        ----------
        Category: Utilities

        Usage: invites [member: discord.Member]
        """
        if member is None:
            member = ctx.author

        total_invites = 0
        for invite in await ctx.guild.invites():
            if invite.inviter == member:
                total_invites += invite.uses

        em = discord.Embed(
            title="Invites",
            # This line has been stolen from simplex bot
            description=f"{member.mention} has invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!",
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
        )
        await ctx.respond(embed=em)


    @utilities.command(name="inviteslb", description="Get a leaderboard of the invites in the server")
    @commands.check(blacklisted)
    async def inviteslb(self, ctx):
        """
        This command is used to get a leaderboard of the invites in the server

        Help Info:
        ----------
        Category: Utilities

        Usage: inviteslb
        """
        
        em = discord.Embed(
            title="Leaderboard",
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
        )
        total_invites = {}
        for invite in await ctx.guild.invites():
            try:
                total_invites[invite.inviter.name] += invite.uses
            except KeyError:
                total_invites[invite.inviter.name] = invite.uses
        total_invites = dict(
            sorted(total_invites.items(), reverse=True, key=lambda item: item[1])
        )

        for key, value in total_invites.items():
            if value != 0:
                em.add_field(name=key, value=value, inline=False)

        await ctx.respond(embed=em)


def setup(client: WhyBot):
    client.add_cog(Utilities(client))
