import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.models.client import WhyBot
from core.helpers.exception import UserAlreadyBlacklisted, UserAlreadyWhitelisted


class Blacklist(commands.Cog):
    def __init__(self, client):
        self.client: WhyBot = client

    blacklisted = SlashCommandGroup("blacklist", "Blacklist Commands")

    @blacklisted.command(name="blacklist", description="ban a user from using whybot")
    @commands.is_owner()
    async def blacklist(
        self, ctx, user_id: discord.Option(str, description="User id of user to ban")
    ):
        if not user_id.isnumeric():
            return await ctx.respond(
                embed=discord.Embed(
                    title="Invalid discord userid",
                    description="Please provide an INTEGER",
                    color=ctx.author.color,
                )
            )

        user_id = int(user_id)

        try:
            await self.client.blacklist_user(user_id)
        except UserAlreadyBlacklisted:
            return await ctx.respond(
                embed=discord.Embed(
                    title="User Already Blacklisted",
                    description="The user you tried to blacklist was already blacklisted.",
                    color=ctx.author.color,
                )
            )

        await ctx.respond(
            embed=discord.Embed(
                description="User blacklisted successfuly!", color=ctx.author.color
            )
        )

    @blacklisted.command(name="whitelist", description="unban a user from using whybot")
    @commands.is_owner()
    async def whitelist(
        self, ctx, user_id: discord.Option(str, description="User id of user to unban")
    ):
        if not user_id.isnumeric():
            return await ctx.respond(
                embed=discord.Embed(
                    title="Invalid discord userid",
                    description="Please provide an INTEGER",
                    color=ctx.author.color,
                )
            )

        user_id = int(user_id)

        try:
            await self.client.whitelist_user(user_id)
        except UserAlreadyWhitelisted:
            return await ctx.respond(
                embed=discord.Embed(
                    title="User Already Whitelisted",
                    description="The user you tried to whitelist was already whitelisted.",
                    color=ctx.author.color,
                )
            )

        await ctx.respond(
            embed=discord.Embed(
                description="User whitelisted successfuly!", color=ctx.author.color
            )
        )


def setup(client):
    client.add_cog(Blacklist(client))
