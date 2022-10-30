from enum import Enum

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.helpers.http import get_request


def animal_embed(response: dict | None, title: str):
    if response is None:
        return discord.Embed(
            title="An error occured while trying to get the image",
            description=(
                "API basically had a skill issue.\nIf this persists and you are able to, report this as a bug with </bug:0> :)"
            ),
            color=discord.Colour.red(),
        )

    em = discord.Embed(
        title=title, description=response["fact"], color=discord.Color.random()
    )
    em.set_image(url=response["image"])
    return em


class AnimalURLS(Enum):
    dog = "https://some-random-api.ml/animal/dog"
    cat = "https://some-random-api.ml/animal/cat"
    fox = "https://some-random-api.ml/animal/fox"
    panda = "https://some-random-api.ml/animal/panda"
    bird = "https://some-random-api.ml/animal/bird"
    kangaroo = "https://some-random-api.ml/animal/kangaroo"
    koala = "https://some-random-api.ml/animal/koala"
    raccoon = "https://some-random-api.ml/animal/raccoon"
    red_panda = "https://some-random-api.ml/animal/red_panda"
    capybara = [
        "https://api.capybara-api.xyz/v1/image/random",
        "https://api.capybara-api.xyz/v1/facts/random",
    ]


class Animals(commands.Cog):
    def __init__(self, client):
        self.client = client

    animal = SlashCommandGroup("animal", "Get images and facts about animals")

    @animal.command()
    async def dog(self, ctx):
        url = AnimalURLS.dog.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed(response, "Dog!"))

    @animal.command()
    async def cat(self, ctx):
        url = AnimalURLS.cat.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed(response, "Cat!"))

    @animal.command()
    async def fox(self, ctx):
        url = AnimalURLS.fox.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed(response, "Fox!"))

    @animal.command()
    async def panda(self, ctx):
        url = AnimalURLS.panda.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed(response, "Panda!"))

    @animal.command()
    async def bird(self, ctx):
        url = AnimalURLS.bird.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed(response, "Bird!"))

    @animal.command()
    async def kangaroo(self, ctx):
        url = AnimalURLS.kangaroo.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed(response, "Kangaroo!"))

    @animal.command()
    async def koala(self, ctx):
        url = AnimalURLS.koala.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed(response, "Koala!"))

    @animal.command()
    async def raccon(self, ctx):
        url = AnimalURLS.raccoon.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed(response, "Racoon!"))

    @animal.command()
    async def redpanda(self, ctx):
        url = AnimalURLS.red_panda.value
        response = await get_request(url)

        await ctx.respond(embed=animal_embed(response, "Red Panda!"))

    @animal.command()
    async def capybara(self, ctx):
        image_url = AnimalURLS.capybara.value[0]
        image = await get_request(image_url)

        fact_url = AnimalURLS.capybara.value[1]
        fact = await get_request(fact_url)

        if image is None or fact is None:
            return await ctx.respond(embed=animal_embed(None, "Ok I pull up!"))

        response = {"fact": fact["fact"], "image": image["storage_url"]}
        await ctx.respond(embed=animal_embed(response, "Ok I pull up!"))


def setup(client):
    client.add_cog(Animals(client))
