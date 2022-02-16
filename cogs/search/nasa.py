import discord
import datetime
import urllib.request
from discord.ext import commands
from dotenv import load_dotenv
import os
from utils import get_url_json, get_url_image
import json

load_dotenv()

API_KEY = os.environ['NASA']

class Nasa(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def aopd(self, ctx, extra:str=None):
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
        data = await get_url_json(url)

        em = discord.Embed(
            title = "Astronomy Picture of the Day",
            color = ctx.author.color
        )
        if extra is not None:
            em.description = data["explanation"]
        em.set_image(url=data["hdurl"])
        em.timestamp = datetime.datetime.now()
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Nasa(client))