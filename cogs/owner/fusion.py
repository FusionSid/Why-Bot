import discord
import os
import json
from discord.ext import commands
import datetime
import dotenv
from utils import is_it_me, Log
from subprocess import run
import time

log = Log()

dotenv.load_dotenv()

class Fusion(commands.Cog):
    def __init__(self, client):
        self.client = client


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
        em = discord.Embed(title=guild.name, color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.add_field(name="ID:", value=guild.id)
        em.add_field(name="Owner name", value=guild.owner.name)
        em.add_field(name="Member Count", value=guild.member_count)
        await ctx.author.send(embed=em)
        
    
    @commands.command()
    @commands.check(is_it_me)
    async def message_servers(self, ctx, *, kwargs):
        colors = {
            "none" : None,
            "blue": discord.Color.blue(),
            "blurple": discord.Color.blurple(),
            "brand_green": discord.Color.brand_green(),
            "brand_red": discord.Color.brand_red(),
            "dark_blue": discord.Color.dark_blue(),
            "dark_gold": discord.Color.dark_gold(),
            "dark_gray": discord.Color.dark_gray(),
            "dark_green": discord.Color.dark_green(),
            "dark_grey": discord.Color.dark_grey(),
            "dark_magenta": discord.Color.dark_magenta(),
            "dark_orange": discord.Color.dark_orange(),
            "dark_purple": discord.Color.dark_purple(),
            "dark_red": discord.Color.dark_red(),
            "dark_teal": discord.Color.dark_teal(),
            "dark_theme": discord.Color.dark_theme(),
            "darker_gray": discord.Color.darker_gray(),
            "darker_grey": discord.Color.darker_grey(),
            "fuchsia": discord.Color.fuchsia(),
            "gold": discord.Color.gold(),
            "green": discord.Color.green(),
            "greyple": discord.Color.greyple(),
            "light_gray": discord.Color.light_gray(),
            "light_grey": discord.Color.light_grey(),
            "lighter_gray": discord.Color.lighter_gray(),
            "lighter_grey": discord.Color.lighter_grey(),
            "magenta": discord.Color.magenta(),
            "nitro_pink": discord.Color.nitro_pink(),
            "og_blurple": discord.Color.og_blurple(),
            "orange": discord.Color.orange(),
            "purple": discord.Color.purple(),
            "random": discord.Color.random(),
            "red": discord.Color.red(),
            "teal": discord.Color.teal(),
        }

        colorlist = []
        for c in colors:
            colorlist.append(c)
            
        def wait_for_check(m):
            return m.author == ctx.author and m.channel == ctx.message.channel

        em = discord.Embed()
        em.timestamp = datetime.datetime.utcnow()

        kwargs = shlex.split(kwargs)
        args = {}

        for index in range(len(kwargs)):
            if index % 2 == 0:
                args[kwargs[index].lstrip("--")] = kwargs[index+1]
            index += 0

        for key, value in args.items():
            print(len(args))
            if key.lower() == "title":
                em.title = value
            elif key.lower() == "description" or key.lower() == "desc":
                em.description = value
            elif key.lower() == "img" or key.lower() == "image":
                em.set_image(url=value)
            elif key.lower() == "color" or key.lower() == "colour":
                if value.lower() == "list" or value.lower() == "help":
                    return await ctx.send(", ".join(colorlist))
                if value.lower() not in colorlist:
                    await ctx.send("Color not found", delete_after=2)
                    em.color = ctx.author.color
                else:
                    em.color = colors[value.lower()]
            elif key.lower() == "fields":
                vint = False
                try:
                    int(value) 
                    vint= True
                except:
                    vint = False
                
                if vint is True:
                    for i in range(int(value)):
                        entername = await ctx.send("Enter Name:")
                        name = await self.client.wait_for("message", check=wait_for_check, timeout=300)
                        await name.delete()

                        entervalue = await ctx.send("Enter Value:")
                        value = await self.client.wait_for("message", check=wait_for_check, timeout=300)
                        await entername.delete()
                        await entervalue.delete()
                        await value.delete()

                        em.add_field(name=name.content, value=value.content)
            elif key.lower() in ["timestamp", "time"] and value.lower() in ["true", "yes"]:
                em.timestamp = datetime.datetime.now()
            else:
                pass

        data = await self.client.get_db()
        for guild in self.client.guilds:
            if data[str(guild.id)]["announcement_channel"] is None:
                try:
                    await guild.system_channel.send(embed=em)
                except Exception:
                    continue
            else:
                try:
                    channel = await self.client.fetch_channel(int(data[str(guild.id)]["announcement_channel"]))
                    await channel.send(embed=em)
                except Exception:
                    continue
    

    @commands.command()
    @commands.check(is_it_me)
    async def msgserver(self, ctx, id:int, *, message):
        for guild in self.client.guilds:
            if guild.id == id:
                return await guild.text_channels[0].send(message)
        await ctx.send("guild not found")


    @commands.command()
    @commands.check(is_it_me)
    async def logs(self, ctx):
      file = discord.File("./database/log.txt")
      await ctx.author.send(file=file)


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
    async def needhelp(self, ctx):
        needhelp = []
        for i in self.client.commands:
            if i.help is None:
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
