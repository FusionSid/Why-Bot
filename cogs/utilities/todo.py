import discord
from discord.ext import commands
import aiosqlite

async def get_data(user):
    pass


class Todo(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def todo(self, ctx):
        pass



def setup(client):
    client.add_cog(Todo(client))