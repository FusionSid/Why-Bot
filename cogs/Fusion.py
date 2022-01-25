import discord
import os
import json
from discord.ext import commands
import dotenv
from utils import is_it_me
from utils.other import log

dotenv.load_dotenv()

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
    async def dmreply(self, ctx, *, msg):
        if ctx.message.reference is None:
          return
        else:
          id = ctx.message.reference.message_id
          id = await ctx.channel.fetch_message(id)
          id = int(id.content)
        person = await self.client.fetch_user(id)
        await person.send(msg)

    @commands.command()
    @commands.check(is_it_me)
    async def logs(self, ctx):
      file = discord.File("./other/log.txt")
      await ctx.send(file=file)

    @commands.command()
    @commands.check(is_it_me)
    async def backup(self, ctx):
      os.system("git add .")
      os.system("git commit -m 'backup' ")
      os.system("git push")

    @commands.command()
    @commands.check(is_it_me)
    async def useembed(self, ctx, code:str, channel:id=None):
        if channel is None:
            channel=ctx.channel
        else:
            channel = self.client.fetch_channel(channel)
        from ..tempstorage.code import run
        await run(channel)

    @commands.command()
    async def dmid(self, ctx, id:int, *, message):
      user = await self.client.fetch_user(id)
      await user.send(message)
      
def setup(client):
    client.add_cog(Fusion(client))
