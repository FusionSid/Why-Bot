import discord
from discord.ext import commands
import random
from googleapiclient.discovery import build

class Google(commands.Cog):
  def __init__(self, client):
    self.client = client

  @client.command()
  async def imagesearch(ctx, *, search):
      ran = random.randint(0, 9)
      resource = build("customsearch", "v1", developerKey=isapi_key).cse()
      result = resource.list(
          q=f"{search}", cx="54c1117c3e104029b", searchType="image"
      ).execute()
      url = result["items"][ran]["link"]
      embed1 = discord.Embed(title=f"Search:({search.title()})")
      embed1.set_image(url=url)
      await ctx.send(embed=embed1)
  
def setup(client):
    client.add_cog(Google(client))