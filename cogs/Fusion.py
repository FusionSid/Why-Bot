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

  @commands.command()
  @commands.check(is_it_me)
  async def addshopitem(self, ctx)
    with open("shop.json") as f:
      data = json.load(f)
    
    def wfcheck(m):
      return m.channel == ctx.channel and m.author == ctx.author

    await ctx.send("Enter Name")
    name = await client.wait_for("message", check=wfcheck)
    await ctx.send("Enter Price")
    price = await client.wait_for("message", check=wfcheck)
    await ctx.send("Enter Description")
    desc = await client.wait_for("message", check=wfcheck)
    await ctx.send("Purchaseable? true/false")
    buy = await client.wait_for("message", check=wfcheck)

    if buy.lower() == "true"
      content = {
        "name": name, 
        "price": int(price), 
        "description":desc, 
        "buy": True
        }
    else:
      content = {
        "name": name, 
        "price": int(price), 
        "description":desc, 
        "buy": False
        }
    
    data["mainshop"].append(content)

    with open('shop.json', 'w') as f:
      json.dump(data, f)

def setup(client):
  client.add_cog(Fusion(client))
