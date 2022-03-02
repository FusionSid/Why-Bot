import discord
from discord.ext import commands
from utils import is_it_me
import datetime

async def get_cog(client, ext):
    for cog in client.cogs_list:
        if ext.lower() in cog:
            return cog

class CogTools(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.check(is_it_me)
    async def reload(self, ctx, extension):
        # self.client.reload_extension(await get_cog(self.client, extension))
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=ctx.author.color)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        

    @commands.command()
    @commands.check(is_it_me)
    async def load(self, ctx, extension):
        # self.client.load_extension(await get_cog(self.client, extension))
        self.client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(title='Load', description=f'{extension} successfully loaded', color=ctx.author.color)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    
    @commands.command()
    @commands.check(is_it_me)
    async def unload(self, ctx, extension):
        # self.client.unload_extension(await get_cog(self.client, extension))
        self.client.unload_extension(f"cogs.{extension}")
        embed = discord.Embed(title='Unload', description=f'{extension} successfully unloaded', color=ctx.author.color)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(is_it_me)
    async def listcogs(self, ctx):
        return await ctx.send("\n".join(self.client.cogs_list))


    @commands.command(aliases=['rall'])
    @commands.check(is_it_me)
    async def reloadall(self, ctx):
        cogs = self.client.cogs_list

        cogs.remove("cogs.leveling.leveling")
        try:
            for cogs in cogs:
                try:
                    self.client.reload_extension(cogs)
                except:
                    continue
            await ctx.send("All Reloaded")

        except Exception as e:
            print(e)


def setup(client):
    client.add_cog(CogTools(client))