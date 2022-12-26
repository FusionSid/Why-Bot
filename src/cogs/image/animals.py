from enum import Enum

import discord
from discord.commands import SlashCommandGroup

from core import BaseCog
from core.helpers import get_request, ImageAPIFail


def animal_embed(response: dict = None):
    if response is None:
        raise ImageAPIFail

    em = discord.Embed(
        title=response["title"],
        description=response["desc"],
        color=discord.Color.random(),
    )

    em.set_image(url=response["image"])

    return em


def animal_embed_randomapi(response: dict | None, title: str):
    if response is None:
        raise ImageAPIFail

    em = discord.Embed(
        title=title, description=response["fact"], color=discord.Color.random()
    )

    em.set_image(url=response["image"])

    return em


class AnimalURLS(Enum):
    # some random api
    dog = "https://some-random-api.ml/animal/dog"
    cat = "https://some-random-api.ml/animal/cat"
    fox = "https://some-random-api.ml/animal/fox"
    panda = "https://some-random-api.ml/animal/panda"
    bird = "https://some-random-api.ml/animal/bird"
    kangaroo = "https://some-random-api.ml/animal/kangaroo"
    koala = "https://some-random-api.ml/animal/koala"
    raccoon = "https://some-random-api.ml/animal/raccoon"
    red_panda = "https://some-random-api.ml/animal/red_panda"

    # other
    capybara = "https://api.capy.lol/v1/capybara?json=true"
    shibe = "https://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true"
    duck = "https://random-d.uk/api/v2/quack"
    whale = "https://some-random-api.ml/img/whale"


class Animals(BaseCog):

    animal = SlashCommandGroup("animal", "Get images and facts about animals")

    @animal.command(description="Show a picture of a dog")
    async def dog(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.dog.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed_randomapi(response, "Dog!"))

    @animal.command(description="Show a picture of a cat")
    async def cat(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.cat.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed_randomapi(response, "Cat!"))

    @animal.command(description="Show a picture of a fox")
    async def fox(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.fox.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed_randomapi(response, "Fox!"))

    @animal.command(description="Show a picture of a panda")
    async def panda(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.panda.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed_randomapi(response, "Panda!"))

    @animal.command(description="Show a picture of a bird")
    async def bird(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.bird.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed_randomapi(response, "Bird!"))

    @animal.command(description="Show a picture of a kangaroo")
    async def kangaroo(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.kangaroo.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed_randomapi(response, "Kangaroo!"))

    @animal.command(description="Show a picture of a koala")
    async def koala(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.koala.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed_randomapi(response, "Koala!"))

    @animal.command(description="Show a picture of a racoon")
    async def raccon(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.raccoon.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed_randomapi(response, "Racoon!"))

    @animal.command(description="Show a picture of a red panda")
    async def redpanda(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.red_panda.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed_randomapi(response, "Red Panda!"))

    @animal.command(description="Show a picture of a capybara")
    async def capybara(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.capybara.value
        image = await get_request(url)

        if (
            image is None
            or image.get("data") is None
            or image["data"].get("url") is None
        ):
            await ctx.respond(embed=animal_embed(None))

        response = {
            "desc": "Ok I Pull Up!",
            "image": image["data"]["url"],
            "title": "Capybara!",
        }
        await ctx.respond(embed=animal_embed(response))

    @animal.command(description="Show a picture of a duck")
    async def duck(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.duck.value
        image = await get_request(url)

        if image is None or image.get("url") is None:
            await ctx.respond(embed=animal_embed(None))

        response = {
            "desc": "Quack!",
            "image": image["url"],
            "title": "Duck!",
        }
        await ctx.respond(embed=animal_embed(response))

    @animal.command(description="Show a picture of a shiba inu")
    async def shibe(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.shibe.value
        image = await get_request(url)

        if image is None or not image:
            await ctx.respond(embed=animal_embed(None))

        response = {
            "desc": "Certified good boi!",
            "image": image[0],
            "title": "Shiba Inu!",
        }
        await ctx.respond(embed=animal_embed(response))

    @animal.command(description="Show a picture of a whale")
    async def whale(self, ctx: discord.ApplicationContext):
        url = AnimalURLS.whale.value
        image = await get_request(url)

        if image is None or not image:
            await ctx.respond(embed=animal_embed(None))

        response = {
            "desc": "Big boi!",
            "image": image["link"],
            "title": "Whale!",
        }
        await ctx.respond(embed=animal_embed(response))


def setup(client):
    client.add_cog(Animals(client))
