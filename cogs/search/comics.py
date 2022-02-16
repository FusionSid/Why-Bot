import discord
from discord.ext import commands
from dotenv import load_dotenv


class Comics(commands.Cog):
    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(Comics(client))