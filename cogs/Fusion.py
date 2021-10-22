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
  
  @commands.command(aliases=['bl'])
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

  @commands.command(aliases=['wl'])
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
  
  @commands.command(aliases=['blacklisted', 'lb'])
  @commands.check(is_it_me)
  async def listblack(self, ctx):
    with open('blacklisted.json') as f:
      blacklisted = json.load(f)
    
    await ctx.send(blacklisted)
  

  @commands.command()
  @commands.check(is_it_me)
  async def reload(self, ctx, extension):
    self.client.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
    await ctx.send(embed=embed)


def setup(client):
  client.add_cog(Fusion(client))
