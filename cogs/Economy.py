import discord
import os
from discord.ext import commands
import json

class Economy(commands.Cog):
  def __init__(self, client):
    self.client = client
  
def setup(client):
    client.add_cog(Economy(client))