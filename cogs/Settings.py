import discord
from discord.ext import commands
import json
from discord.ui import Button, View
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
        

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def settings(self,ctx):
        plugins = await enabled_cogs(ctx)

        em = discord.Embed(title="Settings", description="Use the arrows to look throught the settings")
        ems = [em, plugins]
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
        plist = ["Counting","Moderation","Economy","TextConvert","Search","Welcome","Leveling","Music","Onping","Ticket","Minecraft","Utilities"]
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


def setup(client):
    client.add_cog(Settings(client))