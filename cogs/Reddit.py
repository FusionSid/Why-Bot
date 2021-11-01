import discord
from discord.ext import commands
import os
import random
import praw
import requests


# Create reddit client
def reddit_client():
    client = praw.Reddit(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        user_agent=os.environ['USER_AGENT']
    )
    return client


# Check if its an image
def is_image(post):
    try:
        return post.post_hint == "image"
    except AttributeError:
        return False


# Get top 50 image urls (memes)
async def get_img_url(client: praw.Reddit, sub_name: str, limit: int):
    hot_memes = client.subreddit(sub_name).hot(limit=limit)
    image_urls = []
    for post in hot_memes:
        if is_image(post):
            image_urls.append(post.url)
    return image_urls


async def get_url(client: praw.Reddit, sub_name: str, limit: int):
    hot_memes = client.subreddit(sub_name).hot(limit=limit)
    urls = []
    for post in hot_memes:
        urls.append(post.url)
    return urls


class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rimg'])
    async def redditimg(self, ctx, subreddit: str):
        rclient = reddit_client()
        urls = await get_img_url(client=rclient, sub_name=subreddit, limit=50)
        url = random.choice(urls)
        em = discord.Embed(title="Reddit Image Search:")
        em.set_image(url=url)
        await ctx.send(embed=em)

    @commands.command(aliases=['getmeme'])
    async def meme(self, ctx):
        reddit = reddit_client()
        subreddit = reddit.subreddit("memes")
        hot = subreddit.hot(limit=50)
        urls = []
        for i in hot:
            urls.append(i)
        ran_sub = random.choice(urls)
        name = ran_sub.title
        url = ran_sub.url
        ups = ran_sub.ups
        downs = ran_sub.downs
        author = ran_sub.author
        em = discord.Embed(title=name)
        em.set_image(url=url)
        em.set_footer(text=f"{author} | 👍 : {ups}")
        await ctx.send(embed=em)

    @commands.command(aliases=['redditsearch'])
    async def reddit(self, ctx, subreddit: str):
        rclient = reddit_client()
        urls = await get_url(client=rclient, sub_name=subreddit, limit=50)
        url = random.choice(urls)
        em = discord.Embed(title="Reddit Search:", description=url)
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Reddit(client))
