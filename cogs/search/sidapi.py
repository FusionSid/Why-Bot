import discord
from utils import return_url_image
from discord.ext import commands
from io import BytesIO

class SidAPI(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = "https://memegenapi.herokuapp.com/api/"


    @commands.command(help = "This function generates a meme", description="Aborted meme", extras={"category", "Search"}, usage="aborted [@member]")
    async def aborted(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        url = f"{self.url}aborted?image_url={member.avatar.url}"
        image = await return_url_image(url=url)
        file = BytesIO(image)
        file.seek(0)
        await ctx.send(file=discord.File(file, "aborted.png"))

    @commands.command(help = "This function generates a meme", description="Armor meme", extras={"category", "Search"}, usage="armor [text]")
    async def armor(self, ctx, *, text):
        url = f"{self.url}armor?text={text.replace(' ', '+')}"
        image = await return_url_image(url=url)
        file = BytesIO(image)
        file.seek(0)
        await ctx.send(file=discord.File(file, "aborted.png"))

    @commands.command(help = "This function generates a meme", description="Affect meme", extras={"category", "Search"}, usage="affect [@member]")
    async def affect(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        url = f"{self.url}affect?image_url={member.avatar.url}"
        image = await return_url_image(url=url)
        file = BytesIO(image)
        file.seek(0)
        await ctx.send(file=discord.File(file, "affect.png"))

    @commands.command(help = "This function generates a meme", description="Wanted image", extras={"category", "Search"}, usage="wanted [@member]")
    async def affect(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        url = f"{self.url}wanted?image_url={member.avatar.url}"
        image = await return_url_image(url=url)
        file = BytesIO(image)
        file.seek(0)
        await ctx.send(file=discord.File(file, "wanted.png"))

    @commands.command(help = "This function generates a meme", description="Abandon meme", extras={"category", "Search"}, usage="abandon [text]")
    async def abandon(self, ctx, *, text):
        url = f"{self.url}abandon?text={text.replace(' ', '+')}"
        image = await return_url_image(url=url)
        file = BytesIO(image)
        file.seek(0)
        await ctx.send(file=discord.File(file, "abandon.png"))


def setup(client):
    client.add_cog(SidAPI(client))