import discord
import os
import json
from discord.ext import commands
import dotenv
from utils import is_it_me, Log
from subprocess import run
import time
from os import listdir
from os.path import isfile, join

log = Log("./database/log.txt", timestamp=True)

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
            return await ctx.send(embed=discord.Embed(title=f"Git Commands", description="?git pull\n?git status\n?git add\n?git commit\n?git push"))

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


    @git.command()
    @commands.check(is_it_me)
    async def add(self, ctx):
        output = run(["git", "add", "."], capture_output=True).stdout

        await ctx.send(output.decode())


    @git.command()
    @commands.check(is_it_me)
    async def commit(self, ctx):
        output = run(["git", "commit", "-m", "'Updated File'"], capture_output=True).stdout

        await ctx.send(output.decode())


    @git.command()
    @commands.check(is_it_me)
    async def push(self, ctx):
        output = run(["git", "push"], capture_output=True).stdout

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
            with open("./database/db.json") as f:
                data = json.load(f)
            for i in data:
                if i["announcement_channel"] is None:
                    try:
                        await guild.system_channel.send(message)
                    except:
                        pass
                    for i in guild.text_channels:
                        try:
                            await i.send(message)
                            c +=1
                            break
                        except Exception as e:
                            await ctx.send(embed=discord.Embed(title=f"Failed to send to {i.name}\n{guild.name} ({guild.id})", description=e))
                            c -= 1
                else:
                    try:
                        channel = await self.client.fetch_channel(int(i["announcement_channel"]))
                        await channel.send(message)
                    except:
                        pass
           
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
    async def dmreply(self, ctx, *, msg=None):
        if ctx.message.reference is None:
          return
        else:
            await ctx.message.delete()
            id = ctx.message.reference.message_id
            id = await ctx.channel.fetch_message(id)
            await id.reply(msg)
            id = int(id.content)
        person = await self.client.fetch_user(id)

        if msg is None:
            pass
        else:
            await person.send(msg)

        if ctx.message.attachments is None:
            return
        else:
            for i in ctx.message.attachments:
                em = discord.Embed()
                em.set_image(url=i.url)
                await person.send(embed=em)
        

    @commands.command()
    @commands.check(is_it_me)
    async def logs(self, ctx):
      file = discord.File("./database/log.txt")
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


    @commands.command()
    @commands.check(is_it_me)
    async def needhelp(self, ctx):
        needhelp = []
        for i in self.client.commands:
            if i.help is None:
                if i.cog_name == "Fusion" or i.cog_name == "Economy" or i.cog_name == "Leveling":
                    pass
                else:
                    needhelp.append(f"{i.name} | {i.cog_name}")
        await ctx.send("\n".join(needhelp))

    @commands.command()
    @commands.check(is_it_me)
    async def cmdtojson(self, ctx):
        commandlist = []
        for i in self.client.commands:
            print(i)
            if i.usage is None:
                pass
            else:
                if len(i.aliases) == 0:
                    aliases = None
                else:
                    aliases = i.aliases
                data = {
                    "name" : i.name,
                    "aliases" : aliases,
                    "description" : i.description,
                    "help" : i.help,
                    "category" : i.extras['category'].lower(),
                    "usage" : i.usage
                }
                commandlist.append(data)
        with open("./commands.json", 'w') as f:
            json.dump(commandlist, f, indent=4)
    
def setup(client):
    client.add_cog(Fusion(client))
