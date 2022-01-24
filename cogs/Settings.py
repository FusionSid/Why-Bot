import discord
from discord.ext import commands
import json
from discord.ui import Button, View
from utils.other import log
from utils import Paginator
from utils.checks import plugin_enabled

async def enabled_cogs(ctx):
    with open("./database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == ctx.guild.id:
            plugins = i['settings']['plugins']
    em = discord.Embed(title="Plugins:",description="These are all the plugins that have been enabled on your server")
    for key, value in plugins.items():
        if value == True:
            emoji = "Enabled ✅"
        else:
            emoji = "Disabled ❌"
        em.add_field(name=key, value=emoji)
    em.set_footer(text=f"Use {ctx.prefix}plugins to toggle plugins")
    return em

async def get_channels(self, ctx):
    with open("./database/db.json") as f:
        data = json.load(f)
    em = discord.Embed(title="Channels")
    em.set_footer(text="Use /set to set these")
    for i in data:
        if i['guild_id'] == ctx.guild.id:
            if i['counting_channel'] == None:
                counting="Not Set"
            else:
                channel = await self.client.fetch_channel(i['counting_channel'])
                counting = channel
            if i['welcome_channel'] == None:
                welcome="Not Set"
            else:
                channel = await self.client.fetch_channel(i['welcome_channel'])
                welcome = channel
            if i['log_channel'] == None:
                log="Not Set"
            else:
                channel = await self.client.fetch_channel(i['log_channel'])
                log = channel
            em.add_field(name="Counting:", value=counting)
            em.add_field(name="Welcome:", value=welcome)
            em.add_field(name="Log:", value=log)
    return em
        
async def autorole(self, ctx):
    with open("./database/db.json") as f:
        data = json.load(f)
    em = discord.Embed(title="Autorole")
    em.set_footer(text="Use ?autorole [@role] [all/bot] to set the autorole")
    for i in data:
        if i['guild_id'] == ctx.guild.id:
            autorole = i['autorole']
    if autorole['all'] == None:
        em.add_field(name="All", value="Not set")
    else:
        role = await ctx.guild.get_role(autorole['all'])
        em.add_field(name="All", value=role.mention)
    if autorole['bot'] == None:
        em.add_field(name="Bot", value="Not set")
    else:
        role = await ctx.guild.fetch_role(autorole['bot'])
        em.add_field(name="Bot", value=role.mention)
    return em

async def welcome_text(ctx):
    with open("./database/db.json") as f:
        data = json.load(f)
    em = discord.Embed(title="Welcome Text")
    em.set_footer(text="Use ?setwelcometext [text] to set the text")
    for i in data:
        if i['guild_id'] == ctx.guild.id:
            wt = i['settings']['welcometext']
    em.add_field(name="Text:", value=wt)
    return em

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def settings(self,ctx):
        plugins = await enabled_cogs(ctx)

        em = discord.Embed(title="Settings", description="Use the arrows to look throught the settings")
        
        prefix = discord.Embed(title = "Prefix", description=f"The prefix is `{ctx.prefix}`")
        prefix.set_footer(text=f"You can use {ctx.prefix}setprefix [prefix] to set the prefix")

        channels = await get_channels(self, ctx)
        autoroles = await autorole(self, ctx)
        welcometext = await welcome_text(ctx)

        ems = [em, plugins, prefix, channels, autoroles, welcometext]
        view = Paginator(ctx=ctx, ems=ems)

        message = await ctx.send(embed=em, view=view)
        res = await view.wait()
        if res:
            for i in view.children:
                i.disabled = True
        return await message.edit(view=view)
    
    @commands.group()
    async def plugins(self, ctx):
        if ctx.invoked_subcommand is None:
          em = discord.Embed(title="Plugins", description=f"Use `{ctx.prefix}plugins [enable/disable] [plugin name]`")
          em.add_field(name="Plugin List:", value="Counting\nModeration\nEconomy\nTextConvert\nSearch\nWelcome\nLeveling\nMusic\nOnping\nTicket\nMinecraft\nUtilities")
          em.set_footer(text="This command is case sensitive so please use capital letters")
          await ctx.send(embed=em)
    
    @plugins.group()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx, plugin:str):
        plist = ["Counting","Moderation","Economy","TextConvert","Search","Welcome","Leveling","Music","Onping","Ticket","Minecraft","Utilities", "Fun"]
        if plugin not in plist:
            return await ctx.send(f"Plugin not found, use `{ctx.prefix}plugins` for a list of them")
        with open('./database/db.json') as f:
            data = json.load(f)
        for i in data:
            if i['guild_id'] == ctx.guild.id:
                i['settings']['plugins'][plugin] = True

        with open("./database/db.json", 'w') as f:
            json.dump(data, f, indent=4)
        
        await ctx.send(f"{plugin} has been enabled")


    @plugins.group()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, plugin:str):
        plist = ["Counting","Moderation","Economy","TextConvert","Search","Welcome","Leveling","Music","Onping","Ticket","Minecraft","Utilities"]
        if plugin not in plist:
            return await ctx.send(f"Plugin not found, use `{ctx.prefix}plugins` for a list of them")
        with open('./database/db.json') as f:
            data = json.load(f)
        for i in data:
            if i['guild_id'] == ctx.guild.id:
                i['settings']['plugins'][plugin] = False

        with open("./database/db.json", 'w') as f:
            json.dump(data, f, indent=4)
        
        await ctx.send(f"{plugin} has been disabled")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcometext(self, ctx, *, text):
        if len(text) > 55:
            return await ctx.send("Text is to big")
        with open("./database/db.json") as f:
            data = json.load(f)
        for i in data:
            if i['guild_id'] == ctx.guild.id:
                i['settings']['welcometext'] = text
        with open("./database/db.json", 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"{text}\nHas been set as the welcome text")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(ctx, pref: str):
        with open(f'./database/db.json') as f:
            data = json.load(f)
        for i in data:
            if i["guild_id"] == ctx.guild.id:
                i["prefix"] = pref
        with open(f'./database/db.json', 'w') as f:
            json.dump(data, f)
        await ctx.send(embed=discord.Embed(title=f"Prefix has been set to `{pref}`"))

def setup(client):
    client.add_cog(Settings(client))