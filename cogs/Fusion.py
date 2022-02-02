import discord
import os
import json
from discord.ext import commands
import dotenv
from utils import is_it_me
from utils.other import log
from subprocess import run
import time
from os import listdir
from os.path import isfile, join

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

    @commands.command(aliases=['blacklisted'])
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
  
    @commands.group()
    @commands.check(is_it_me)
    async def git(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        else:
            return await ctx.send(embed=discord.Embed(f"Git Commands", description="git pull\ngit status"))

    @git.command()
    @commands.check(is_it_me)
    async def pull(self, ctx):
        output = run(["git", "pull"], capture_output=True).stdout

        await ctx.send(output.decode())


    @git.command()
    @commands.check(is_it_me)
    async def status(self, ctx):
        output = run(["git", "status"], capture_output=True).stdout

        await ctx.send(output.decode())

    @commands.command()
    @commands.check(is_it_me)
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Load', description=f'{extension} successfully loaded', color=0xff00c8)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.check(is_it_me)
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Unload', description=f'{extension} successfully unloaded', color=0xff00c8)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(is_it_me)
    async def serverlist(self, ctx):
        servers = list(self.client.guilds)
        await ctx.send(f"Connected on {str(len(servers))} servers:")
        await ctx.send('\n'.join(guild.name for guild in servers))

    @commands.command()
    @commands.check(is_it_me)
    async def svrls(self, ctx):
      await ctx.message.delete()
      for guild in self.client.guilds:
        em = discord.Embed(title=guild.name)
        em.add_field(name="ID:", value=guild.id)
        em.add_field(name="Owner name", value=guild.owner.name)
        em.add_field(name="Member Count", value=guild.member_count)
        await ctx.author.send(embed=em)
        
        
    
    @commands.command()
    @commands.check(is_it_me)
    async def message_servers(self, ctx, *, message):
        c = 0
        for guild in self.client.guilds:
            for i in guild.text_channels:
              try:
                await i.send(message)
                c +=1
                break
              except Exception as e:
                await ctx.send(embed=discord.Embed(title=f"Failed to send to {i.name}\n{guild.name} ({guild.id})", description=e))
                c -= 1
        await ctx.send(f"Message sent to {c}/{len(self.client.guilds)} servers")

    @commands.command()
    @commands.check(is_it_me)
    async def msgserver(self, ctx, id:int, *, message):
        for guild in self.client.guilds:
            if guild.id == id:
                return await guild.text_channels[0].send(message)
        await ctx.send("guild not found")

    @commands.command(aliases=['dmr'])
    @commands.check(is_it_me)
    async def dmreply(self, ctx, *, msg):
        if ctx.message.reference is None:
          return
        else:
            await ctx.message.delete()
            id = ctx.message.reference.message_id
            id = await ctx.channel.fetch_message(id)
            await id.reply(msg)
            id = int(id.content)
        person = await self.client.fetch_user(id)
        await person.send(msg)
        

    @commands.command()
    @commands.check(is_it_me)
    async def logs(self, ctx):
      file = discord.File("./other/log.txt")
      await ctx.author.send(file=file)
      
    @commands.command()
    async def embedcreatorpy(self,ctx):
      await ctx.send(embed=discord.Embed(description="[Embed Creator Python](https://why-discord-bot.fusionsid.repl.co/embed)"))

    @commands.command()
    @commands.check(is_it_me)
    async def ssinfo(self, ctx, g:int):
        guild = self.client.get_guild(g)
        print(guild)
        em = discord.Embed(title="Server Info:", description=f"For: {guild.name}", color=ctx.author.color)
        em.set_thumbnail(url=guild.icon.url)
        em.set_author(name=f"Guild Owner: {guild.owner.name}", icon_url=guild.owner.avatar.url)
        em.add_field(name="Member Count:", value=guild.member_count) 
        em.add_field(name="Created: ", value=f"<t:{int(time.mktime(guild.created_at.timetuple()))}>")
        em.add_field(name="ID:", value=guild.id)
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(is_it_me)
    async def reloadall(self, ctx):
        lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
        no_py = [s.replace('.py', '') for s in lst]
        startup_extensions = ["cogs." + no_py for no_py in no_py]
        startup_extensions.remove("cogs.Leveling")

        try:
            for cogs in startup_extensions:
                self.client.reload_extension(cogs)

            await ctx.send("All Reloaded")

        except Exception as e:
            print(e)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel):
        
            cha = await self.client.fetch_channel(926232260166975508)
            em = discord.Embed(title="New DM", description=f"From {message.author.name}")

            if message.content != "":
                em.add_field(name="Content", value=f"{message.content}")
            await cha.send(content=f"{message.author.id}", embed=em)

            if message.attachments is not None:
                for attachment in message.attachments:
                    em = discord.Embed(title="** **")
                    em.set_image(url=attachment.url)
                    await cha.send(embed=em)


def setup(client):
    client.add_cog(Fusion(client))
