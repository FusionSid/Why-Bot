import discord
import os
import sqlite3
from discord.ext import commands
from cryptography.fernet import Fernet

class Database(commands.Cog):
  def __init__(self, client):
    self.client = client

def setup(client):
    client.add_cog(Database(client))