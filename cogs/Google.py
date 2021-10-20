import discord
from discord.ext import commands
import random
from googleapiclient.discovery import build
import requests
import re
import urllib.request
from googlesearch import search

isapi_key = "AIzaSyCj52wnSciil-4JPd6faOXXHfEb1pzrCuY"

class Google(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def imagesearch(self, ctx, *, search):
      ran = random.randint(0, 9)
      resource = build("customsearch", "v1", developerKey=isapi_key).cse()
      result = resource.list(
          q=f"{search}", cx="54c1117c3e104029b", searchType="image"
      ).execute()
      url = result["items"][ran]["link"]
      embed1 = discord.Embed(title=f"Search:({search.title()})")
      embed1.set_image(url=url)
      await ctx.send(embed=embed1)
  

  @commands.command()
  async def youtube(self, ctx, *, search):
    html - urllib.request.urlopen(f'http://www.youtube.com/results?search_query={search}')
    ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    base_url = "https://www.youtube.com/watch?v="
    em=discord.Embed(title="Youtube Search", description = "Showing first 5 urls")
    videos = [ids[0], ids[1], ids[2], ids[3], ids[4]]
    for video in videos:
      em.add_field(name=video, value="** **")
    await ctx.send(embed=em)


  @commands.command()
  async def google(self, ctx, *, search):
    em = discord.Embed(title="Google Search", description = "Showing first 5 urls")
    for i in search(query, tid="com", num=10, stop=10, pause=2):
      em.addfield(name=i, value="** **")
    await ctx.send(embed=em)

def setup(client):
    client.add_cog(Google(client))