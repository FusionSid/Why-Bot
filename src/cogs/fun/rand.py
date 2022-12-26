import io
import os
import json
import string
import random

import discord
import aiofiles
from PIL import Image
import discord_colorize
from discord.commands import SlashCommandGroup

import __main__
from core import BaseCog
from core.helpers import ImageAPIFail
from core.helpers.http import get_request_bytes


class Random(BaseCog):
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

    @random.command(description="Show a random compliment")
    async def compliment(self, ctx: discord.ApplicationContext):
        data = await self.open_json_fun()
        await ctx.respond(random.choice(data["compliment"]))

    @random.command(description="Show a random dare")
    async def dare(self, ctx: discord.ApplicationContext):
        data = await self.open_json_fun()
        await ctx.respond(random.choice(data["dares"]))

    @random.command(description="Show a random fact")
    async def fact(self, ctx: discord.ApplicationContext):
        data = await self.open_json_fun()
        await ctx.respond(random.choice(data["facts"]))

    @random.command(description="Show a random roast")
    async def roast(self, ctx: discord.ApplicationContext):
        data = await self.open_json_fun()
        await ctx.respond(random.choice(data["roasts"]))

    @random.command(description="Show a random truth")
    async def truth(self, ctx: discord.ApplicationContext):
        data = await self.open_json_fun()
        await ctx.respond(random.choice(data["truth"]))

    @random.command(description="Show a random truth and dare")
    async def truth_or_dare(self, ctx: discord.ApplicationContext):
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

    @random.command(description="Pick a random number")
    async def number(self, ctx: discord.ApplicationContext, stop: int, start: int = 0):
        return await ctx.respond(random.randint(start, stop))

    @random.command(description="Pick a random choice out of the options you give")
    async def choice(
        self,
        ctx: discord.ApplicationContext,
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

    @random.command(description="Choose a random card")
    async def card(self, ctx: discord.ApplicationContext):
        url = "https://api.fusionsid.xyz/api/image/random-card"
        img = await get_request_bytes(
            url,
            bytes_io=True,
        )

        if not isinstance(img, io.BytesIO):
            raise ImageAPIFail

        await ctx.respond(file=discord.File(img, "text.png"))

    @random.command(description="Flip a coin")
    async def flipcoin(self, ctx: discord.ApplicationContext):
        h_or_t = random.choice(["heads", "tails"])
        path = os.path.join(
            os.path.dirname(__main__.__file__).replace("src", ""),
            f"assets/images/{h_or_t}.png",
        )
        await ctx.respond(f"Its {h_or_t}!", file=discord.File(path))

    @random.command(description="Pick a random color")
    async def color(self, ctx: discord.ApplicationContext):
        color = tuple(random.randint(0, 255) for _ in range(3))
        img = Image.new("RGB", (500, 500), color)
        send = io.BytesIO()
        img.save(send, "PNG")
        send.seek(0)
        await ctx.respond(file=discord.File(send, "color.png"))

    @random.command(description="Pick a random letter")
    async def letter(self, ctx: discord.ApplicationContext):
        return await ctx.respond(
            f"Your random letter is '{random.choice(string.ascii_lowercase)}'"
        )

    @random.command(description="Roll a dice")
    async def diceroll(self, ctx: discord.ApplicationContext):
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
