import discord
from discord.ui import Button, View
import json
from discord.ext import commands
import datetime
import dotenv
from utils import is_it_me, Log, kwarg_to_embed
import time

log = Log()

dotenv.load_dotenv()

class BotInfoView(View):
    def __init__(self):
        super().__init__(timeout=None)

        button1 = Button(style=discord.ButtonStyle.grey, label="Vote:",url="https://discordbotlist.com/bots/why")
        button2 = Button(style=discord.ButtonStyle.grey, label="Source:",url="https://github.com/FusionSid/Why-Bot")
        button3 = Button(style=discord.ButtonStyle.grey,label="Discord:", url="https://discord.gg/ryEmgnpKND")
        button4 = Button(style=discord.ButtonStyle.grey,label="Website:", url="https://fusionsid.xyz/whybot")

        self.add_item(button1)
        self.add_item(button2)
        self.add_item(button3)
        self.add_item(button4)


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
        data = await kwarg_to_embed(self.client, ctx, kwargs)
        em = data[0]

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
    async def finduser(self, ctx, id:int):
        user = await self.client.fetch_user(id)
        em = discord.Embed(title="User Info:", description=f"For: {user.name}", color=user.color)
        em.add_field(name="ID:", value=user.id, inline=False)
        em.set_thumbnail(url=user.avatar.url)
        em.add_field(name="Created Account:",value=f"<t:{int(time.mktime(user.created_at.timetuple()))}>", inline=False)
        shared_guilds = []
        for guild in self.client.guilds:
            if user in guild.members:
                shared_guilds.append(guild.name)
        em.add_field(name=f"Shared Guilds: ({len(shared_guilds)})", value=", ".join(shared_guilds))

        with open('./database/userdb.json') as f:
            data = json.load(f)
        cuse = data[str(user.id)]["command_count"]

        em.add_field(name="Command Use:", value=f"User has used Why Bot: {cuse} times")
        
        em.timestamp = datetime.datetime.now()
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
    

    @commands.command()
    async def show_bot_info_message(self, ctx):
        em = discord.Embed(
            title = "🔗 Why Bot - Info and Links",
            description = "Why bot is an open source multi-purpose discord bot",
            color = discord.Color.red(),
            timestamp = datetime.datetime.now()
        )
        em.add_field(
            inline=False,
            name = "**Help Command**", 
            value = "```diff\n- If you need help with Why Bot you can use the command: ?help```"
        )
        em.add_field(
            inline=False,
            name = "**Bugs:**", 
            value = "```diff\n- If you find a bug and want to report it, Use the command: ?bug <bug>```"
        )
        em.add_field(
            inline=False,
            name = "**Suggestions:**", 
            value = "```diff\n- If you have a suggestion for Why bot, Use the command ?suggest <suggestion> or the slash command: /suggest to make a suggestion.```"
        )
        em.add_field(
            inline=False,
            name = "**Dev:**", 
            value = "```diff\n- Why bot is open-source so if you would like to contribute to Why Bot - Checkout the github. You can also contact FusionSid: (@FusionSid#3645)```"
        )
        em.add_field(
            inline=False,
            name = "**DM The Bot**", 
            value = "```diff\n- If you want you can always DM the bot. You can do this if you need help, want to report something, want to suggest something or if you just want to talk. ```"
        )
        em.add_field(
            inline=False,
            name = "Mostly made by: FusionSid",
            value = "`Twitter (Which I don't really use):` [@Fusion_Sid](https://twitter.com/Fusion_Sid)\n`My Github profile:` [FusionSid](https://github.com/FusionSid)"
        )
        
        em.set_thumbnail(url=self.client.user.avatar.url)
        em.set_footer(text="To invite Why, Click the bot and hit add to server or user ?botinvite")

        await ctx.send(embed=em, view=BotInfoView())

        

def setup(client):
    client.add_cog(Fusion(client))
