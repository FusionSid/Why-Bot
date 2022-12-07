from enum import Enum

import discord
from discord.ext import commands

from core.models import WhyBot
from core.helpers.checks import run_bot_checks
from core.helpers.http import get_request_bytes
from core.helpers.exception import ImageAPIFail


class ImageURLS(Enum):
    ## Some Random API Endpoints
    # overlays
    comrade = "https://some-random-api.ml/canvas/overlay/comrade"
    gay = "https://some-random-api.ml/canvas/overlay/gay"
    wasted = "https://some-random-api.ml/canvas/overlay/wasted"
    jail = "https://some-random-api.ml/canvas/overlay/jail"
    triggered = "https://some-random-api.ml/canvas/overlay/triggered"
    glass = "https://some-random-api.ml/canvas/overlay/glass"
    passed = "https://some-random-api.ml/canvas/overlay/passed"

    # filters
    blue = "https://some-random-api.ml/canvas/filter/blue"
    red = "https://some-random-api.ml/canvas/filter/red"
    blurple = "https://some-random-api.ml/canvas/filter/blurple"
    green = "https://some-random-api.ml/canvas/filter/green"
    invertgreyscale = "https://some-random-api.ml/canvas/filter/invertgreyscale"
    sepia = "https://some-random-api.ml/canvas/filter/sepia"
    color = "https://some-random-api.ml/canvas/filter/color"
    greyscale = "https://some-random-api.ml/canvas/filter/greyscale"
    brightness = "https://some-random-api.ml/canvas/filter/brightness"

    # misc
    youtube = "https://some-random-api.ml/canvas/misc/youtube-comment"
    blur = "https://some-random-api.ml/canvas/misc/blur"
    spin = "https://some-random-api.ml/canvas/misc/spin"
    circle = "https://some-random-api.ml/canvas/misc/circle"
    pixelate = "https://some-random-api.ml/canvas/misc/pixelate"
    lolice = "https://some-random-api.ml/canvas/misc/lolice"
    oogway = "https://some-random-api.ml/canvas/misc/oogway"
    heart = "https://some-random-api.ml/canvas/misc/heart"
    tweet = "https://some-random-api.ml/canvas/misc/tweet"
    horny = "https://some-random-api.ml/canvas/misc/horny"
    lied = "https://some-random-api.ml/canvas/misc/lied"
    nobitches = "https://some-random-api.ml/canvas/misc/nobitches"
    simpcard = "https://some-random-api.ml/canvas/misc/simpcard"
    stupid = "https://some-random-api.ml/canvas/misc/its-so-stupid"

    ## Other
    unsplash = "https://source.unsplash.com/random"


class OtherImage(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    @commands.slash_command()
    async def unsplash(self, ctx: discord.ApplicationContext, search_terms: str = None):
        url = ImageURLS.unsplash.value
        if search_terms is not None:
            url += f"?{search_terms}"

        response = await get_request_bytes(url, bytes_io=True)
        if response is None:
            raise ImageAPIFail

        await ctx.respond(file=discord.File(response, "image.png"))


def setup(client):
    client.add_cog(OtherImage(client))
