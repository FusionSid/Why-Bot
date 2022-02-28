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

    @commands.command(usage = "apod", description = "Astronomy Picture of the day", help = "This command shows the  NASA astronomy picture of the day", extras={"category": ""})
    @commands.check(plugin_enabled)
    async def apod(self, ctx):
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&thumbs=True"
        data = await get_url_json(url)

        em = discord.Embed(
            title = data['title'],
            color = ctx.author.color
        )
        em.description = data["explanation"]
        if data["media_type"] == "image":
            em.set_image(url=data["hdurl"])
        elif data["media_type"] == "video":
            em.set_image(url=data['thumbnail'])
        em.timestamp = datetime.datetime.now()
        em.set_footer(text=data['copyright'])
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Nasa(client))
