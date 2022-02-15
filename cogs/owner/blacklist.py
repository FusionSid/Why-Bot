import discord
from discord.ext import commands
from utils import is_it_me
import json

class Blacklisted(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bl'])
    @commands.check(is_it_me)
    async def blacklist(self, ctx, userid: int):
        with open('./database/blacklisted.json') as f:
            blacklisted = json.load(f)

        if userid in blacklisted:
            await ctx.send("User is already blacklisted")
        else:
            blacklisted.append(userid)
            await ctx.send("User has been blacklisted")

        with open('./database/blacklisted.json', 'w') as f:
            json.dump(blacklisted, f, indent=4)


    @commands.command(aliases=['wl'])
    @commands.check(is_it_me)
    async def whitelist(self, ctx, userid: int):
        with open('./database/blacklisted.json') as f:
            blacklisted = json.load(f)

        if userid in blacklisted:
            blacklisted.remove(userid)
            await ctx.send("User is no longer blacklisted")
        else:
            await ctx.send("User isnt blacklisted")

        with open('./database/blacklisted.json', 'w') as f:
            json.dump(blacklisted, f, indent=4)


    @commands.command(aliases=['blacklisted'])
    @commands.check(is_it_me)
    async def listblack(self, ctx):
        with open('./database/blacklisted.json') as f:
            blacklisted = json.load(f)

        await ctx.send(blacklisted)

def setup(client):
    client.add_cog(Blacklisted(client))