import discord
from utils.checks import plugin_enabled
from discord.ext import commands
import random
from googleapiclient.discovery import build
import re
import datetime
import urllib.request
import os
import dotenv

dotenv.load_dotenv()
isapi_key = os.environ['ISAPI']

class Google(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['is'], help="This command is used to search for images on google.", extras={"category":"Search"}, usage="imagesearch [search query]", description="Find an image from google")
    @commands.check(plugin_enabled)
    async def imagesearch(self, ctx, *, search):
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey=isapi_key).cse()
        result = resource.list(
            q=f"{search}", cx="54c1117c3e104029b", searchType="image"
        ).execute()
        url = result["items"][ran]["link"]
        embed1 = discord.Embed(title=f"Search:({search.title()})", color=ctx.author.color)
        embed1.timestamp = datetime.datetime.utcnow()
        embed1.set_image(url=url)
        await ctx.send(embed=embed1)

    @commands.command(aliases=['yt'], help="This command gets searches through youtube to find a video.", extras={"category":"Search"}, usage="youtube [search query]", description="Searches through youtube for videos")
    @commands.check(plugin_enabled)
    async def youtube(self, ctx, *, search_):
        search_ = search_.replace(" ", "+")
        html = urllib.request.urlopen(
            f'http://www.youtube.com/results?search_query={search_}')
        ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        base_url = "https://www.youtube.com/watch?v="
        em = discord.Embed(title="Youtube Search",
                           description="Showing first 5 urls", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        videos = [ids[0], ids[1], ids[2], ids[3], ids[4]]
        for video in videos:
            em.add_field(name=f"{base_url}{video}", value="** **")
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Google(client))