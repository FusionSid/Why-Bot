import discord
from utils.checks import plugin_enabled
from discord.ext import commands
import random
import aiohttp
import aiofiles
from googleapiclient.discovery import build
import re
import datetime
import urllib.request
import os
import praw
import asyncio
import wikipedia
import dotenv

async def get_wiki(query):
    page = wikipedia.page(query, auto_suggest=True, preload=True)
    summary = page.summary

    embed = discord.Embed(title="Wikipedia:", description=summary, color=0x00ff00)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_author(name=f"Searching for {query}")
    embed.set_thumbnail(url=random.choice(page.images))
    embed.add_field(name="Link", value=f"[Wikipedia Link]({page.url})")

    return embed


class Search(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.animal_urls = {
            "dog" : "https://some-random-api.ml/animal/dog",
            "cat" : "https://some-random-api.ml/animal/cat",
            "fox" : "https://some-random-api.ml/animal/fox",
            "panda" : "https://some-random-api.ml/animal/panda",
            "bird" : "https://some-random-api.ml/animal/bird",
        }

 
    @commands.command(help="This command returns a random rock image", extras={"category":"Search"}, usage="rock", description="Rock Image")
    @commands.check(plugin_enabled)
    async def rock(self, ctx):
        url = "https://mrconos.pythonanywhere.com/rock/random"
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    response = await resp.json()
                    if response['image'] == "none":
                        pass
                    else:
                        break
        em = discord.Embed(title=response['name'], description=response['desc'], color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        rating = response["rating"]
        em.add_field(name="Rating", value=f"{rating}/5")
        em.set_image(url=response["image"])
        await ctx.send(embed=em)


    # Animals:
    @commands.command(help="This command show a picture of a dog", extras={"category":"Search"}, usage="dog", description="Dog Image")
    @commands.check(plugin_enabled)
    async def dog(self, ctx):
        url = self.animal_urls["dog"]
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    r = await resp.json()
        em = discord.Embed(title="Dog!", description=r['fact'], color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.set_image(url=r['image'])

        await ctx.send(embed=em)
    
    @commands.command(help="This command show a picture of a cat", extras={"category":"Search"}, usage="cat", description="Cat Image")
    @commands.check(plugin_enabled)
    async def cat(self, ctx):
        url = self.animal_urls["cat"]
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    r = await resp.json()
        em = discord.Embed(title="Cat!", description=r['fact'], color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.set_image(url=r['image'])

        await ctx.send(embed=em)

    @commands.command(help="This command show a picture of a panda", extras={"category":"Search"}, usage="panda", description="Panda Image")
    @commands.check(plugin_enabled)
    async def panda(self, ctx):
        url = self.animal_urls["panda"]
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    r = await resp.json()
        em = discord.Embed(title="Panda!", description=r['fact'], color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.set_image(url=r['image'])

        await ctx.send(embed=em)

    @commands.command(help="This command show a picture of a fox", extras={"category":"Search"}, usage="fox", description="Fox Image")
    @commands.check(plugin_enabled)
    async def fox(self, ctx):
        url = self.animal_urls["fox"]
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    r = await resp.json()
        em = discord.Embed(title="Fox!", description=r['fact'], color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.set_image(url=r['image'])

        await ctx.send(embed=em)

    @commands.command(help="This command show a picture of a bird", extras={"category":"Search"}, usage="bird", description="Bird Image")
    @commands.check(plugin_enabled)
    async def bird(self, ctx):
        url = self.animal_urls["bird"]
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    r = await resp.json()
        em = discord.Embed(title="Bird!", description=r['fact'], color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.set_image(url=r['image'])

        await ctx.send(embed=em)

    
    @commands.command(help="This command shows a fake tweet image with the user you wants name on it and the message you want", extras={"category":"Search"}, usage="tweet [@person] [message]", description="Fake tweet image")
    @commands.check(plugin_enabled)
    async def tweet(self, ctx, member: discord.Member, *, message):
        data = {
            "username" : member.name,
            "displayname" : member.display_name,
            "avatar" : member.avatar.url,
            "comment" : message
        }

        url = "https://some-random-api.ml/canvas/tweet/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/tweet{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/tweet{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/tweet{ctx.author.id}.png")

    @commands.command(aliases=['ytc'], help="This command shows a fake youtube comment image with the user you wants name on it and the message you want", extras={"category":"Search"}, usage="ytcomment [@person] [message]", description="Fake youtube comment image")
    @commands.check(plugin_enabled)
    async def ytcomment(self, ctx, member: discord.Member, *, message):
        data = {
            "username" : member.name,
            "avatar" : member.avatar.url,
            "comment" : message
        }

        url = "https://some-random-api.ml/canvas/youtube-comment/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/yt{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/yt{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/yt{ctx.author.id}.png")

    @commands.command(help="This command shows a memeber profile pic on a simp card", extras={"category":"Search"}, usage="simp [@member]", description="Simp card")
    @commands.check(plugin_enabled)
    async def simp(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        data = {
            "avatar" : member.avatar.url,
        }

        url = "https://some-random-api.ml/canvas/simpcard/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/simp{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/simp{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/simp{ctx.author.id}.png")

    @commands.command(help="This command shows your licence to be horny card", extras={"category":"Search"}, usage="horny [@member]", description="Horny licence")
    @commands.check(plugin_enabled)
    async def horny(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        data = {
            "avatar" : member.avatar.url,
        }

        url = "https://some-random-api.ml/canvas/horny/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/horny{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/horny{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/horny{ctx.author.id}.png")

    @commands.command(help="This command is actually a bunch of commands. You type the command and then specify an overlay type, these are the options:\ngay, glass, wasted, passed, jail, comrade, triggered\nAfter you pick one the bot will put that as an overlay on top of the member you picked profile pictire", extras={"category":"Search"}, usage="overlay [type] [@member]", description="Image overlays for you discord profile pic")
    @commands.check(plugin_enabled)
    async def overlay(self, ctx, type:str=None, member: discord.Member=None):
        overlays = ["gay","glass","wasted","passed","jail","comrade","triggered"]
        if type is None or type.lower() not in overlays:
            return await ctx.send(embed=discord.Embed(title="Overlays:", description="\n".join(overlays), color=ctx.author.color))

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/{type}/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")
    
    @commands.command(help="This command tells a (not funny) joke", extras={"category":"Search"}, usage="joke", description="Joke")
    @commands.check(plugin_enabled)
    async def joke(self, ctx):
        url = "https://some-random-api.ml/joke"
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    r = await resp.json()
        em=discord.Embed(title=r['joke'], color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=em)

    @commands.command(help="This command shows lyrics for a song. You input the title and the bot tries to find the lyrics for that song", extras={"category":"Search"}, usage="lyrics [song name]", description="Song lyrics command")
    @commands.check(plugin_enabled)
    async def lyrics(self, ctx, *, song):
        url = "https://some-random-api.ml/lyrics"
        song = song.replace(" ", "+")
        data = {
            "title" : song
        }

        async with aiohttp.ClientSession() as session:
                async with session.get(url, data=data) as resp:
                    r = await resp.json()
        if 'error' in r:
            return await ctx.send(r['error'])
        
        em = discord.Embed(
            title=r['title'],
            description=f"{r['lyrics']}\n\n[Link on genius]({r['links']['genius']})", color=ctx.author.color
        )
        em.set_author(name=r['author'])
        em.set_thumbnail(url=r['thumbnail']['genius'])
        em.color = ctx.author.color
        em.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=em)
    
    @commands.command(aliases=['wkp', 'wikipedia'], help="This command looks through wikipedia and finds you a page based on your search query", usage='wiki [search]', description="Wikipedia Search", extras={"category":"Search"})
    @commands.check(plugin_enabled)
    async def wiki(self, ctx, *, query):
        embed = await get_wiki(query)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Search(client))
