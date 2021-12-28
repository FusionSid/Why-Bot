# Slash commands
import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ui import Button, View
from discord import Option

class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(guild_ids=[763348615233667082], name="hi", description="Test")
    async def hello(self, ctx, user : Option(discord.Member, "The user", required=False) = None):
        if user is None:
            await ctx.respond("Hello")
        else:
            await ctx.respond(f"Hello {user.mention}")

def setup(client):
    client.add_cog(Slash(client))