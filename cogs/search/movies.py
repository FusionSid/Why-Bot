import discord
from utils import plugin_enabled
from discord.ext import commands
from imdb import Cinemagoer

ia = Cinemagoer()

class Movies(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(plugin_enabled)
    async def top_movies(self, ctx):
        top = ia.get_popular100_movies()

        await ctx.send(top[0])

    
    @commands.command()
    @commands.check(plugin_enabled)
    async def imdb_find_person(self, ctx, *, query):
        people = ia.search_person(query)
        person = people[0]

        em = discord.Embed(
            title = person["name"],
            description = f"First result for search: `{query}`",
            color = ctx.author.color
        )
        em.add_field(name="Summary:", value=person["biography"])
        em.set_thumbnail(url=person['headshot'])
        await ctx.send(embed=em)


    @commands.command()
    @commands.check(plugin_enabled)
    async def imdb_find_movie(self, ctx, *, movie):
        movies = ia.search_movie(movie)
        movie = movies[0]



def setup(client):
    client.add_cog(Movies(client))