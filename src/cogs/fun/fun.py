import os
import random
import tempfile

import discord
from discord.ext import commands
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

import __main__
from core.helpers.checks import run_bot_checks
from core.helpers.views import RickRollView


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_check = run_bot_checks

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
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def crab(self, ctx, text1, text2):
        await ctx.defer()
        video = await self.gen_crab(text1, text2)
        await ctx.respond(file=discord.File(video.name, "crab.mp4"))
        video.close()

    @commands.slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def claim(self, ctx):
        em = discord.Embed(title="Claim 100k Why Coins", color=discord.Color.blue())
        await ctx.respond(embed=em, view=RickRollView(self.client.db))

    @commands.slash_command()
    async def spongebob(self, ctx, time: int, unit: str):
        path = os.path.join(
            os.path.dirname(__main__.__file__), "assets/images/spongebob"
        )
        images = {}
        for image in os.listdir(path):
            key = image[:-4]
            images[key] = image

    @commands.slash_command(name="8ball")
    async def _8ball(self, ctx, question: str):
        responses = [
            "As I see it, yes",
            "It is certain",
            "It is decidedly so",
            "Most likely",
            "Outlook good",
            "Signs point to yes",
            "Without a doubt",
            "Yes",
            "Yes - definitely",
            "You may rely on it",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
        ]
        em = discord.Embed(
            title="8 Ball 🎱",
            description=f"**Question:** {question}\n**Answer:** {random.choice(responses)}",
            color=ctx.author.color,
        )
        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Fun(client))
