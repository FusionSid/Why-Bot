import discord
from discord.ext import commands
import json
from discord.ui import Button, View
from utils import Paginator

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
    em.set_footer(text=f"Use {ctx.prefix} to toggle plugins")
    return em
        

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def settings(self,ctx):
        plugins = await enabled_cogs(ctx)

        em = discord.Embed(title="Settings", description="Use the arrows to look throught the settings")
        ems = [plugins, em]
        view = Paginator(ctx=ctx, ems=ems)

        message = await ctx.send(embed=em, view=view)
        res = await view.wait()
        if res:
            for i in view.children:
                i.disabled = True
        return await message.edit(view=view)

def setup(client):
    client.add_cog(Settings(client))