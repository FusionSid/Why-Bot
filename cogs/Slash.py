from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Slash(client))
