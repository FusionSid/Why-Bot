import io
import os
import json
import string
import random

import discord
import aiofiles
from PIL import Image
import discord_colorize
from discord.ext import commands
from discord.commands import SlashCommandGroup

import __main__
from core.helpers.exception import ImageAPIFail
from core.helpers.checks import run_bot_checks
from core.helpers.http import get_request_bytes


class Random(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_check = run_bot_checks

    @staticmethod
    async def open_json_fun():
        path = os.path.join(
            os.path.dirname(__main__.__file__).replace("src", ""),
            "assets/json_files/fun_text.json",
        )
        async with aiofiles.open(path, mode="r") as f:
            contents = await f.read()
        data = json.loads(contents)

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
                description=(
                    f'**Truth:** {random.choice(data["truth"])}\n**Dare:**'
                    f' {random.choice(data["dares"])}\n\n**Computer Choice:**'
                    f' {random.choice(["truth", "dare"])}'
                ),
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

    @random.command()
    async def card(self, ctx):
        url = "https://api.fusionsid.xyz/api/image/random-card"
        img = await get_request_bytes(
            url,
            bytes_io=True,
        )

        if not isinstance(img, io.BytesIO):
            raise ImageAPIFail

        await ctx.respond(file=discord.File(img, "text.png"))

    @random.command()
    async def flipcoin(self, ctx):
        h_or_t = random.choice(["heads", "tails"])
        path = os.path.join(
            os.path.dirname(__main__.__file__).replace("src", ""),
            f"assets/images/{h_or_t}.png",
        )
        await ctx.respond(f"Its {h_or_t}!", file=discord.File(path))

    @random.command()
    async def color(self, ctx):
        color = tuple([random.randint(0, 255) for i in range(3)])
        img = Image.new("RGB", (500, 500), color)
        send = io.BytesIO()
        img.save(send, "PNG")
        send.seek(0)
        await ctx.respond(file=discord.File(send, "color.png"))

    @random.command()
    async def letter(self, ctx):
        return await ctx.respond(
            f"Your random letter is '{random.choice(string.ascii_lowercase)}'"
        )

    @random.command()
    async def diceroll(self, ctx):
        color = random.choice(
            ["red", "yellow", "blue", "green", "gray", "pink", "cyan", "white"]
        )

        colors = discord_colorize.Colors()
        dice = random.choice(self.dice)
        message = f"```ansi\n{colors.colorize(dice, fg=color)}\n```"
        await ctx.respond(
            embed=discord.Embed(
                title=f"Rolled a {self.dice.index(dice)+1}",
                description=message,
                color=discord.Color.random(),
            )
        )

    # credit to micfun123 for the dice ascii art
    dice = [
        """\
-----
|   |
| o |
|   |
-----
""",
        """\
-----
|o  |
|   |
|  o|
-----
""",
        """\
-----
|o  |
| o |
|  o|
-----
""",
        """\
-----
|o o|
|   |
|o o|
-----
""",
        """\
-----
|o o|
| o |
|o o|
-----
""",
        """\
-----
|o o|
|o o|
|o o|
-----
""",
    ]


def setup(client):
    client.add_cog(Random(client))
