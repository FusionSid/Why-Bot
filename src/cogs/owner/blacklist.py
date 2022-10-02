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
        """
        This command is used to ban a user from using Why Bot

        Help Info:
        ----------
        Category: Owner

        Usage: blacklist <user_id:int>
        """
        if not user_id.isnumeric():
            return await ctx.respond(
                embed=discord.Embed(
                    title="Invalid discord user id",
                    description="Please provide an integer",
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )

        user_id = int(user_id)

        try:
            await self.client.fetch_user(user_id)
        except discord.ApplicationCommandInvokeError:
            return await ctx.respond(
                embed=discord.Embed(
                    title="Invalid discord user id",
                    description="Please provide a real user",
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )

        try:
            await self.client.blacklist_user(user_id)
        except UserAlreadyBlacklisted:
            return await ctx.respond(
                embed=discord.Embed(
                    title="User Already Blacklisted",
                    description="The user you tried to blacklist was already blacklisted.",
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )

        await ctx.respond(
            embed=discord.Embed(
                description="User blacklisted successfuly!", color=ctx.author.color
            ),
            ephemeral=True,
        )

    @blacklisted.command(name="whitelist", description="unban a user from using whybot")
    @commands.is_owner()
    async def whitelist(
        self, ctx, user_id: discord.Option(str, description="User id of user to unban")
    ):
        """
        This command is used to unban a user from using Why Bot

        Help Info:
        ----------
        Category: Owner

        Usage: whitelist <user_id:int>
        """
        if not user_id.isnumeric():
            return await ctx.respond(
                embed=discord.Embed(
                    title="Invalid discord user id",
                    description="Please provide an integer",
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )

        user_id = int(user_id)

        try:
            await self.client.fetch_user(user_id)
        except discord.ApplicationCommandInvokeError:
            return await ctx.respond(
                embed=discord.Embed(
                    title="Invalid discord user id",
                    description="Please provide a real user",
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )

        try:
            await self.client.whitelist_user(user_id)
        except UserAlreadyWhitelisted:
            return await ctx.respond(
                embed=discord.Embed(
                    title="User Already Whitelisted",
                    description="The user you tried to whitelist was already whitelisted.",
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )

        await ctx.respond(
            embed=discord.Embed(
                description="User whitelisted successfuly!", color=ctx.author.color
            ),
            ephemeral=True,
        )


def setup(client):
    client.add_cog(Blacklist(client))
