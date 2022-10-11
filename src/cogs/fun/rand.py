import os
import json
import random

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

import __main__
from core.helpers.checks import run_bot_checks


class Random(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_check = run_bot_checks

    async def open_json_fun(self):
        path = os.path.join(
            os.path.dirname(__main__.__file__).replace("src", ""),
            "assets/json_files/fun_text.json",
        )
        with open(path) as f:
            data = json.load(f)

        return data

    random = SlashCommandGroup("random", "Random commands")

    @random.command()
    async def compliment(self, ctx):
        data = await self.open_json_fun()
        await ctx.respond(random.choice(data["compliment"]))

    @random.command()
    async def dare(self, ctx):
        data = await self.open_json_fun()
        await ctx.respond(random.choice(data["dares"]))

    @random.command()
    async def fact(self, ctx):
        data = await self.open_json_fun()
        await ctx.respond(random.choice(data["facts"]))

    @random.command()
    async def roast(self, ctx):
        data = await self.open_json_fun()
        await ctx.respond(random.choice(data["roasts"]))

    @random.command()
    async def truth(self, ctx):
        data = await self.open_json_fun()
        await ctx.respond(random.choice(data["truth"]))

    @random.command()
    async def truth_or_dare(self, ctx):
        data = await self.open_json_fun()
        await ctx.respond(
            embed=discord.Embed(
                title="Truth Or Dare",
                description=f'**Truth:** {random.choice(data["truth"])}\n**Dare:** {random.choice(data["dares"])}\n\n**Computer Choice:** {random.choice(["truth", "dare"])}',
                color=ctx.author.color,
            )
        )

    @random.command()
    async def number(self, ctx, stop: int, start: int = 0):
        return await ctx.respond(random.randint(start, stop))

    @random.command()
    async def choice(
        self,
        ctx,
        choice1: str,
        choice2: str,
        choice3: str = None,
        choice4: str = None,
        choice5: str = None,
        choice6: str = None,
        choice7: str = None,
        choice8: str = None,
        choice9: str = None,
        choice10: str = None,
    ):
        await ctx.defer()
        choice = random.choice(
            [
                i
                for i in (
                    choice1,
                    choice2,
                    choice3,
                    choice4,
                    choice5,
                    choice6,
                    choice7,
                    choice8,
                    choice9,
                    choice10,
                )
                if i is not None
            ]
        )
        return await ctx.respond(
            embed=discord.Embed(
                title="Random Choice",
                description=f"**Computer Choice:** {choice}",
                color=ctx.author.color,
            )
        )


def setup(client):
    client.add_cog(Random(client))
