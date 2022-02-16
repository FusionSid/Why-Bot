import discord
from discord.ext import commands

class Ebay(commands.Cog):
    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(Ebay(client))