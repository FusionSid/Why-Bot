import discord
from discord.ext import commands

class Dictionary(commands.Cog):
    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(Dictionary(client))