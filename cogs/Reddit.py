import discord
from discord.embeds import Embed
from discord.ext import commands
import requests

class Reddit(commands.Cog):
  def __init__(self, client):
    self.client = client


def setup(client):
    client.add_cog(Reddit(client))