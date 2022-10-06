import os
import tempfile

import discord
from discord.ext import commands
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

import __main__
from core.helpers.checks import run_bot_checks


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def gen_crab(self, t1, t2):
        path = os.path.join(
            os.path.dirname(__main__.__file__).replace("src", ""),
            "assets/videos/crab.mp4",
        )
        clip = VideoFileClip(path)
        text = TextClip(t1, fontsize=48, color="white", font="Symbola")
        text2 = (
            TextClip("____________________", fontsize=48, color="white", font="Verdana")
            .set_position(("center", 210))
            .set_duration(15.4)
        )
        text = text.set_position(("center", 200)).set_duration(15.4)
        text3 = (
            TextClip(t2, fontsize=48, color="white", font="Verdana")
            .set_position(("center", 270))
            .set_duration(15.4)
        )

        video = CompositeVideoClip(
            [clip, text.crossfadein(1), text2.crossfadein(1), text3.crossfadein(1)]
        ).set_duration(15.4)
        file = tempfile.NamedTemporaryFile(suffix=".mp4")
        video.write_videofile(file.name, threads=4, preset="superfast", verbose=False)
        clip.close()
        video.close()
        file.seek(0)
        return file

    @commands.slash_command()
    @commands.check(run_bot_checks)
    async def crab(self, ctx, text1, text2):
        await ctx.defer()
        video = await self.gen_crab(text1, text2)
        await ctx.respond(file=discord.File(video.name, "crab.mp4"))
        video.close()


def setup(client):
    client.add_cog(Fun(client))
