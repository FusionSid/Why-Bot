import discord
from discord.ext import commands
import json
from discord.ui import Button, View
from utils import Paginator

async def enabled_cogs(guild_id):
    with open("./database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == guild_id:
            plugins = i['settings']['plugins']
    for plugin in plugins.items()

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def settings(self,ctx):
        pass

def setup(client):
    client.add_cog(Settings(client))