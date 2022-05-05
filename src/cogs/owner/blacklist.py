from typing import Union

import discord
from discord.ext import commands

import log.log
from utils import WhyBot


class Blacklisted(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.slash_command(aliases=["bl"])
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        """
        This command is for blacklisting users from using the bot

        Help Info:
        ----------
        Category: Owner

        Usage: blacklist <user: discord.Member | int>
        """
        if isinstance(user, discord.Member):
            user = user

        elif isinstance(user, int):
            user = await self.client.fetch_user(user)

        await self.client.blacklist_user(user.id)

        await ctx.respond(f"User ({user.name}) has been blacklisted")

    @commands.slash_command(aliases=["wl"])
    @commands.is_owner()
    async def whitelist(self, ctx, user: discord.Member):
        """
        This command is for whitelisting users who were blacklisted from using the bot

        Help Info:
        ----------
        Category: Owner

        Usage: whitelist <user: discord.Member | int>
        """
        if isinstance(user, discord.Member):
            pass

        elif isinstance(user, int):
            user = await self.client.fetch_user(user)

        await self.client.whitelist_user(user.id)

        await ctx.respond(f"User ({user.name}) has been whitelisted")

    @commands.slash_command(aliases=["blacklisted"])
    @commands.is_owner()
    async def listblack(self, ctx):
        """
        This command is for listing users who have been blacklisted

        Help Info:
        ----------
        Category: Owner

        Usage: listblack
        """
        blacklisted = self.client.blacklisted_users
        blacklisted_users = []
        for user in blacklisted:
            try:
                await self.client.fetch_user(user)
                blacklisted_users.append(f"{user.name} ({user.id})")
            except:
                blacklisted_users.append(user)
                continue
        await ctx.respond(
            embed=discord.Embed(
                title="Blacklisted Users:", description=", ".join(blacklisted_users)
            )
        )


def setup(client: WhyBot):
    client.add_cog(Blacklisted(client))
