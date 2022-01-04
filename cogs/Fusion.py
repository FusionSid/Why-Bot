import discord
import json
from discord.ext import commands
import dotenv

dotenv.load_dotenv()

def is_it_me(ctx):
    return ctx.author.id == 624076054969188363


class Fusion(commands.Cog):

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

    @commands.command(aliases=['blacklisted', 'lb'])
    @commands.check(is_it_me)
    async def listblack(self, ctx):
        with open('./database/blacklisted.json') as f:
            blacklisted = json.load(f)

        await ctx.send(blacklisted)

    @commands.command()
    @commands.check(is_it_me)
    async def reload(self, ctx, extension):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.send(embed=embed)
  

    @commands.command()
    @commands.check(is_it_me)
    async def serverlist(self, ctx):
        servers = list(self.client.guilds)
        await ctx.send(f"Connected on {str(len(servers))} servers:")
        await ctx.send('\n'.join(guild.name for guild in servers))

    @commands.command()
    @commands.check(is_it_me)
    async def message_servers(self, ctx, *, message):
        for guild in self.client.guilds:
            await guild.text_channels[0].send(message)

    @commands.command()
    @commands.check(is_it_me)
    async def msgserver(self, ctx, id:int, *, message):
        for guild in self.client.guilds:
            if guild.id == id:
                return await guild.text_channels[0].send(message)
        await ctx.send("guild not found")

    @commands.command()
    @commands.check(is_it_me)
    async def dmreply(self, ctx, id:int, *, msg):
        person = await self.client.fetch_user(id)
        await person.send(msg)

def setup(client):
    client.add_cog(Fusion(client))
