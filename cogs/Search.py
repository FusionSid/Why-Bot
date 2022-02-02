import discord
from utils.checks import plugin_enabled
from discord.ext import commands
import random
from googleapiclient.discovery import build
from utils.other import log
import re
import urllib.request
import os
import praw
import dotenv
import requests

dotenv.load_dotenv()


isapi_key = "AIzaSyCj52wnSciil-4JPd6faOXXHfEb1pzrCuY"


def reddit_client():
    client = praw.Reddit(
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


class Search(commands.Cog):
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
        embed1 = discord.Embed(title=f"Search:({search.title()})")
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
                           description="Showing first 5 urls")
        videos = [ids[0], ids[1], ids[2], ids[3], ids[4]]
        for video in videos:
            em.add_field(name=f"{base_url}{video}", value="** **")
        await ctx.send(embed=em)

    @commands.command(aliases=['rimg'], help="This command looks through a reddit subreddit of your choice and finds an image from that subreddit", extras={"category":"Search"}, usage="redditimg [subreddit]", description="Find a image from a subreddit")
    @commands.check(plugin_enabled)
    async def redditimg(self, ctx, subreddit: str):
        rclient = reddit_client()
        urls = await get_img_url(client=rclient, sub_name=subreddit, limit=50)
        url = random.choice(urls)
        em = discord.Embed(title="Reddit Image Search:")
        em.set_image(url=url)
        await ctx.send(embed=em)

    @commands.command(aliases=['getmeme'], help="This command looks in r/memes to find a meme", extras={"category":"Search"}, usage="meme", description="Gets a meme")
    @commands.check(plugin_enabled)
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

    @commands.command(aliases=['redditsearch'], help="This command looks though a reddit subreddit of your choice and finds a random post.", extras={"category":"Search"}, usage="reddit [subreddit]", description="Find a random reddit post")
    @commands.check(plugin_enabled)
    async def reddit(self, ctx, subreddit: str):
        rclient = reddit_client()
        urls = await get_url(client=rclient, sub_name=subreddit, limit=50)
        url = random.choice(urls)
        em = discord.Embed(title="Reddit Search:", description=url)
        await ctx.send(embed=em)
    
    @commands.command(help="This command returns a random rock image", extra={"category":"Search"}, usage="rock", description="Rock Image")
    @commands.check(plugin_enabled)
    async def rock(self, ctx):
        url = "https://mrconos.pythonanywhere.com/rock/random"
        while True:
            response = requests.get(url, headers={}, data={}).json()
            if response['image'] == "none":
                pass
            else:
                break
        em = discord.Embed(title=response['name'], description=response['desc'])
        rating = response["rating"]
        em.add_field(name="Rating", value=f"{rating}/5")
        em.set_image(url=response["image"])
        await ctx.send(embed=em)

    # Some random API:

def setup(client):
    client.add_cog(Search(client))
