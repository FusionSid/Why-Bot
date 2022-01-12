import discord
from discord.ext import commands
import json
from discord.ui import Button, View
from ..utils.buttons import Paginator

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Settings(client))