import discord
import os
import sqlite3
from discord.ext import commands
from cryptography.fernet import Fernet

class Database(commands.Cog):
  def __init__(self, client):
    self.client = client

  def decrypt(key, encrypted):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted).decode()
    return decrypted

  def encrypt(key, message):
    f = Fernet(key)
    encrypted = f.encrypt(message)
    return encrypted

  @commands.command()
  async def store(self, ctx):
    cd = os.getcwd()
    os.chdir(f"{cd}/Databases")
    conn = sqlite3.connect(f"{ctx.guild.id}.db")
    c = conn.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS {ctx.author.id} (id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT, value TEXT")

    def wfcheck(m):
      return m.channel == ctx.channel and m.author == ctx.author

    await ctx.send("Enter Key:")
    key = await client.wait_for("message", check=wfcheck)

    await ctx.send("Enter Value:")
    value = await client.wait_for("message", check=wfcheck)

    await ctx.send("Enter Encryption Key (if you dont have a key type `None` and then use `genkey` to create a key)")
    ekey = await client.wait_for("message", check=wfcheck)
    
    if value.lower() == "none":
      return
    
    ev = encrypt(ekey, value)

    with conn:
      c.execute(f"INSERT INTO {ctx.author.name} (key, value) VALUES (:key, :value)", {'key':key, 'value':ev})

  
  @commands.command()
  async def get(self, ctx):
    cd = os.getcwd()
    os.chdir(f"{cd}/Databases")
    conn = sqlite3.connect(f"{ctx.guild.id}.db")
    c = conn.cursor()

    def wfcheck(m):
      return m.channel == ctx.channel and m.author == ctx.author

    await ctx.send("Enter Key:")
    key = await client.wait_for("message", check=wfcheck)

    await ctx.send("Enter Encryption Key")
    ekey = await client.wait_for("message", check=wfcheck)

    c.execute(f"SELECT * FROM {ctx.author.name} WHERE key = :key", {'key', key})

    dv = decrypt(ekey, value)

    await ctx.send(dv)

  
def setup(client):
    client.add_cog(Database(client))