import discord
from discord.ext import commands
import random
from googleapiclient.discovery import build
import re
import urllib.request
from googlesearch import search

isapi_key = "AIzaSyCj52wnSciil-4JPd6faOXXHfEb1pzrCuY"

class Google(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['is'])
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
  
  @commands.command(aliases=['yt'])
  async def youtube(self, ctx, *, search_):
    search_ = search_.replace(" ", "+")
    html = urllib.request.urlopen(f'http://www.youtube.com/results?search_query={search_}')
    ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    base_url = "https://www.youtube.com/watch?v="
    em=discord.Embed(title="Youtube Search", description = "Showing first 5 urls")
    videos = [ids[0], ids[1], ids[2], ids[3], ids[4]]
    for video in videos:
      em.add_field(name=f"{base_url}{video}", value="** **")
    await ctx.send(embed=em)

  @commands.command(aliases=['search'])
  async def google(self, ctx, *, search_):
    em = discord.Embed(title="Google Search", description = "Showing first 10 urls")
    for i in search(search_, tld="com", num=10, stop=10):
      em.add_field(name=i, value="** **")
    await ctx.send(embed=em)

def setup(client):
    client.add_cog(Google(client))
