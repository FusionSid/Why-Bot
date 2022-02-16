import discord
from discord.ext import commands
import asyncpraw
import os
from dotenv import load_dotenv
from utils import plugin_enabled
import datetime
import random

load_dotenv()

def reddit_client():
    client = asyncpraw.Reddit(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        user_agent="memes-fastapi"
    )
    return client


def is_image(post):
    try:
        return post.post_hint == "image"
    except AttributeError:
        return False


async def get_img_url(client: asyncpraw.Reddit, sub_name: str, limit: int):
    hot_memes = (await client.subreddit(sub_name)).hot(limit=limit)
    image_urls = []
    async for post in hot_memes:
        if is_image(post):
            image_urls.append(post.url)
    return image_urls


async def get_url(client: asyncpraw.Reddit, sub_name: str, limit: int):
    hot_memes = (await client.subreddit(sub_name)).hot(limit=limit)
    urls = []
    async for post in hot_memes:
        urls.append(post.url)
    return urls


class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['rimg'], help="This command looks through a reddit subreddit of your choice and finds an image from that subreddit", extras={"category":"Search"}, usage="redditimg [subreddit]", description="Find a image from a subreddit")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check(plugin_enabled)
    async def redditimg(self, ctx, subreddit: str):
        rclient = reddit_client()
        urls = await get_img_url(client=rclient, sub_name=subreddit, limit=50)
        url = random.choice(urls)
        em = discord.Embed(title="Reddit Image Search:", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.set_image(url=url)
        await ctx.send(embed=em)
        await rclient.close()


    @commands.command(aliases=['getmeme'], help="This command looks in r/memes to find a meme", extras={"category":"Search"}, usage="meme", description="Gets a meme")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check(plugin_enabled)
    async def meme(self, ctx):
        reddit = reddit_client()
        subreddit = await reddit.subreddit("memes")
        hot = subreddit.hot(limit=50)
        urls = []
        async for i in hot:
            urls.append(i)
        ran_sub = random.choice(urls)
        name = ran_sub.title
        url = ran_sub.url
        ups = ran_sub.ups
        downs = ran_sub.downs
        author = ran_sub.author
        em = discord.Embed(title=name, color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.set_image(url=url)
        em.set_footer(text=f"{author} | 👍 {ups}")
        await ctx.send(embed=em)
        await reddit.close()


    @commands.command(aliases=['redditsearch'], help="This command looks though a reddit subreddit of your choice and finds a random post.", extras={"category":"Search"}, usage="reddit [subreddit]", description="Find a random reddit post")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check(plugin_enabled)
    async def reddit(self, ctx, subreddit: str):
        rclient = reddit_client()
        urls = await get_url(client=rclient, sub_name=subreddit, limit=50)
        url = random.choice(urls)
        em = discord.Embed(title="Reddit Search:", description=url, color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)
        await rclient.close()
    

def setup(client):
    client.add_cog(Reddit(client))