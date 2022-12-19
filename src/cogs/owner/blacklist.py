import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.models.client import WhyBot
from core.utils.client_functions import GUILD_IDS
from core.helpers.exception import UserAlreadyBlacklisted, UserAlreadyWhitelisted


class Blacklist(commands.Cog):
    def __init__(self, client):
        self.client: WhyBot = client

    blacklisted = SlashCommandGroup(
        "blacklist", "Commands for why bot blacklist management. OWNER ONLY"
    )

    @blacklisted.command(
        name="blacklist",
        description="ban a user from using whybot",
        guild_ids=GUILD_IDS,
    )
    @commands.is_owner()
    async def blacklist(
        self,
        ctx: discord.ApplicationContext,
        user_id: discord.Option(str, description="User id of user to ban"),
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
        except (
            discord.NotFound,
            discord.HTTPException,
            discord.ApplicationCommandInvokeError,
        ):
            return await ctx.respond(
                embed=discord.Embed(
                    title="Something went wrong fetching the user",
                    description=(
                        "Most likely an invalid discord user id.\nPlease provide a real"
                        " user"
                    ),
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
                    description=(
                        "The user you tried to blacklist was already blacklisted."
                    ),
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

    @blacklisted.command(
        name="whitelist",
        description="unban a user from using whybot",
        guild_ids=GUILD_IDS,
    )
    @commands.is_owner()
    async def whitelist(
        self,
        ctx: discord.ApplicationContext,
        user_id: discord.Option(str, description="User id of user to unban"),
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
        except (
            discord.NotFound,
            discord.HTTPException,
            discord.ApplicationCommandInvokeError,
        ):
            return await ctx.respond(
                embed=discord.Embed(
                    title="Something went wrong fetching the user",
                    description=(
                        "Most likely an invalid discord user id.\nPlease provide a real"
                        " user"
                    ),
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
                    description=(
                        "The user you tried to whitelist was already whitelisted."
                    ),
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

    @blacklisted.command(guild_ids=GUILD_IDS)
    @commands.is_owner()
    async def isblacklisted(
        self,
        ctx: discord.ApplicationContext,
        user_id: discord.Option(str, description="User id of user to check") = None,
    ):
        users = await self.client.get_blacklisted_users(reasons=True)
        if user_id is not None:
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
            for userid, reason in users:
                if userid == user_id:
                    try:
                        user = await self.client.fetch_user(user_id)
                    except (
                        discord.NotFound,
                        discord.HTTPException,
                        discord.ApplicationCommandInvokeError,
                    ):
                        return await ctx.respond(
                            embed=discord.Embed(
                                title="Something went wrong fetching the user",
                                description=(
                                    "Most likely an invalid discord user id.\nPlease"
                                    " provide a real user"
                                ),
                                color=ctx.author.color,
                            ),
                            ephemeral=True,
                        )

                    return await ctx.respond(
                        embed=discord.Embed(
                            title=(
                                f"User: {user.name}#{user.discriminator} ({user.id}) is"
                                " blacklisted"
                            ),
                            description=f"Reason Provided: {reason}",
                            color=ctx.author.color,
                        )
                    )
            embed = discord.Embed(
                title=f"User with id {user_id} is NOT blacklisted",
                color=ctx.author.color,
            )
            return await ctx.respond(embed=embed)

        await ctx.respond(
            embed=discord.Embed(
                title="Blacklisted User IDs",
                description="\n".join(str(i[0]) for i in users),
            )
        )


def setup(client):
    client.add_cog(Blacklist(client))
