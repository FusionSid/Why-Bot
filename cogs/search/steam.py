import discord
from discord.ext import commands

class Steam(commands.Cog):
    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(Steam(client))