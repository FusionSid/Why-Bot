import discord
from discord.ext import commands
from utils import is_it_me

class Blacklisted(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bl'])
    @commands.check(is_it_me)
    async def blacklist(self, ctx, user_id: int):
        user = await self.client.fetch_user(user_id)
        await self.client.blacklist_user(user_id)

        await ctx.send(f"User ({user.name}) has been blacklisted")


    @commands.command(aliases=['wl'])
    @commands.check(is_it_me)
    async def whitelist(self, ctx, user_id: int):
        user = await self.client.fetch_user(user_id)
        await self.client.whitelist_user(user_id)

        await ctx.send(f"User ({user.name}) has been whitelisted")


    @commands.command(aliases=['blacklisted'])
    @commands.check(is_it_me)
    async def listblack(self, ctx):
        blacklisted = await self.client.blacklisted_users
        blacklisted_users = []
        for user in blacklisted:
            try:
                await self.client.fetch_user(user)
                blacklisted_users.append(user.name)
            except:
                blacklisted_users.append(user)
                continue
        await ctx.send(embed=discord.Embed(
            title="Blacklisted Users:",
            description=", ".join(blacklisted_users)
        ))

def setup(client):
    client.add_cog(Blacklisted(client))