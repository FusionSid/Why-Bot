import discord
import random
import os
import json
import requests
from discord.ext import commands
import sqlite3

def is_it_me(ctx):
  return ctx.author.id == 624076054969188363

class Fusion(commands.Cog):

  def __init__(self, client):
    self.client = client
  
  @commands.command()
  @commands.check(is_it_me)
  async def blacklist(self, ctx, userid:int):
    with open('blacklisted.json') as f:
      blacklisted = json.load(f)

    if userid in blacklisted:
      await ctx.send("User is already blacklisted")
    else:
      blacklisted.append(userid)
      await ctx.send("User has been blacklisted")

    with open('blacklisted.json', 'w') as f:
      json.dump(blacklisted, f)

  @commands.command()
  @commands.check(is_it_me)
  async def whitelist(self, ctx, userid:int):
    with open('blacklisted.json') as f:
      blacklisted = json.load(f)

    if userid in blacklisted:
      blacklisted.remove(userid)
      await ctx.send("User is no longer blacklisted")
    else:
      await ctx.send("User isnt blacklisted")

    with open('blacklisted.json', 'w') as f:
      json.dump(blacklisted, f)
  
  @commands.command()
  @commands.check(is_it_me)
  async def listblack(self, ctx, userid:int):
    with open('blacklisted.json') as f:
      blacklisted = json.load(f)
    
    await ctx.send(blacklisted)
  
  @commands.command(hidden=True)
  @commands.check(is_it_me)
  async def load(self, *, module : str):
      """Loads a module."""
      try:
          self.client.load_extension(module)
      except Exception as e:
          await self.client.say('\N{PISTOL}')
          await self.client.say('{}: {}'.format(type(e).__name__, e))
      else:
          await self.client.say('\N{OK HAND SIGN}')

  @commands.command(hidden=True)
  @commands.check(is_it_me)
  async def unload(self, *, module : str):
      """Unloads a module."""
      try:
          self.client.unload_extension(module)
      except Exception as e:
          await self.client.say('\N{PISTOL}')
          await self.client.say('{}: {}'.format(type(e).__name__, e))
      else:
          await self.client.say('\N{OK HAND SIGN}')

  @commands.command(name='reload', hidden=True)
  @commands.check(is_it_me)
  async def _reload(self, *, module : str):
      """Reloads a module."""
      try:
          self.client.unload_extension(module)
          self.client.load_extension(module)
      except Exception as e:
          await self.client.say('\N{PISTOL}')
          await self.client.say('{}: {}'.format(type(e).__name__, e))
      else:
          await self.client.say('\N{OK HAND SIGN}')

def setup(client):
  client.add_cog(Fusion(client))
