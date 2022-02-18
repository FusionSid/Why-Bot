import discord
import datetime
import urllib.request
from discord.ext import commands
from dotenv import load_dotenv
import os
from utils import get_url_json, get_url_image, plugin_enabled
import json

load_dotenv()

API_KEY = os.environ['NASA']

class Nasa(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(plugin_enabled)
    async def apod(self, ctx):
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
        data = await get_url_json(url)

        em = discord.Embed(
            title = data['title'],
            color = ctx.author.color
        )
        em.description = data["explanation"]
        if data["media_type"] == "image":
            em.set_image(url=data["hdurl"])
        elif data["media_type"] == "video":
            em.add_field(name="Video:", value=f"[Video Link]({data['url']})")
            video_id = data['url']
            video_id = video_id.lstrip("https://www.youtube.com/embed/")
            video_id = video_id.rstrip("?rel=0")
            thum_url = f"https://img.youtube.com/vi/{video_id}/3.jpg"
            em.set_image(url=thum_url)
        em.timestamp = datetime.datetime.now()
        em.set_footer(text=data['copyright'])
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Nasa(client))