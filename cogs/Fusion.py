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

def setup(client):
  client.add_cog(Fusion(client))
