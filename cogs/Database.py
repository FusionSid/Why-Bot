import discord
import os
import sqlite3
from discord.ext import commands
from cryptography.fernet import Fernet

def gen_key():
    key = Fernet.generate_key()
    return key


def encrypt(key, message):
    f = Fernet(key)
    encrypted = f.encrypt(message)
    return encrypted


def decrypt(key, encrypted):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted).decode()
    return decrypted


class Database(commands.Cog):
  def __init__(self, client):
    self.client = client

  db_path = "/home/runner/Why-Bot/Databases/"
  cd = "/home/runner/Why-Bot/cogs/"

  @commands.command()
  async def store(self, ctx):
    conn = sqlite3.connect(f"{ctx.guild.id}.db")
    c = conn.cursor()

    def wfcheck(m):
      return m.channel == ctx.channel and m.author == ctx.author

    await ctx.send("```|Database|\nBefore you start you will need a key.\nIf you dont have one exit and run ?gen_key to get a key\nIt is advised to use this command in dms```")
    
    await ctx.send("```Please enter key:```")
    key_ = await self.client.wait_for("message", check=wfcheck)
    try:
      await ctx.channel.purge(limit=1)
    except:
      pass

    await ctx.send("```Please enter what you would like to name your stored content:```")
    name = await self.client.wait_for("message", check=wfcheck)

    await ctx.send("```Lastly enter the text you want to store:```")
    value = await self.client.wait_for("message", check=wfcheck)
    try:
      await ctx.channel.purge(limit=1)
    except:
      pass

    value = str(value)
    value = value.encode()
    evalue = encrypt(key_, value)
    c.execute(f"CREATE TABLE IF NOT EXISTS {ctx.author.id} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT)")
    with conn:
        c.execute("INSERT INTO :table (name, password) VALUES (:name, :password)", {'table':ctx.author.name,'name':name, 'password':evalue})
    await ctx.send("Done")


  @commands.command()
  async def get(self, ctx):
    def wfcheck(m):
      return m.channel == ctx.channel and m.author == ctx.author
    conn = sqlite3.connect(f"{ctx.guild.id}.db")
    c = conn.cursor()
    def find(search_type="all", search=None):
      if search_type == 'name':
          with conn:
              c.execute("SELECT * FROM {} WHERE name = :name", {'name': search})
          return c.fetchall()

      if search_type == 'id':
          with conn:
              c.execute("SELECT * FROM {} WHERE id = :id", {'id': int(search)})
          return c.fetchall()

      if search_type == 'all':
          with conn:
              c.execute("SELECT * FROM {}")
          return c.fetchall()

      else:
          print("ERROR")

    await ctx.send("```Enter search type (name/id/all):```")
    stype = await self.client.wait_for("message", check=wfcheck)
    stype = stype.lower()

    await ctx.send("```Enter search (if your search type was all type: all):```")
    search = await self.client.wait_for("message", check=wfcheck)
    result = find(stype, search)

    await ctx.send(f"Result:\n{result}")
    await ctx.send("```If you would like it decrypted enter the id of the one you want to decrypt if not type: no```")
    id_ = await self.client.wait_for("message", check=wfcheck)
    try:
      id_ = int(id_)
    except:
      return
    await ctx.send("```Please enter key:```")
    key_ = await self.client.wait_for("message", check=wfcheck)
    try:
      await ctx.channel.purge(limit=1)
    except:
      pass
    value = find("id", id_)
    decrypt = value[0][2]
    decrypted = decrypt(key_, decrypt)
    value[0][2] = decrypted
    await ctx.send("Decrypted sent to dms")
    await ctx.author.send(value)

    





def setup(client):
    client.add_cog(Database(client))
