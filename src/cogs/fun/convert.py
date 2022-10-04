import random

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from core.helpers.checks import run_bot_checks


class TextConvert(commands.Cog):
    def __init__(self, client):
        self.client = client

    textconvert = SlashCommandGroup("textconvert", "Convert text to something else")

    @textconvert.command()
    @commands.check(run_bot_checks)
    async def stickycaps(
        self, ctx, *, text: discord.Option(str, "The text to convert")
    ):
        functions = [str.upper, str.lower]
        result = "".join(random.choice(functions)(char) for char in text)
        if len(result) <= 1999:
            return await ctx.respond(result)
        await ctx.respond("Too long to send :(")

    @textconvert.command()
    @commands.check(run_bot_checks)
    async def expand(
        self, ctx, space: int, *, text: discord.Option(str, "The text to convert")
    ):
        spacing = " " * space
        result = spacing.join(text)
        if len(result) <= 1999:
            return await ctx.respond(result)
        await ctx.respond("Too long to send :(")

    @textconvert.command()
    @commands.check(run_bot_checks)
    async def reverse(self, ctx, *, text: discord.Option(str, "The text to convert")):
        result = text[::-1]
        if len(result) <= 1999:
            return await ctx.respond(result)
        await ctx.respond("Too long to send :(")

    @textconvert.command()
    @commands.check(run_bot_checks)
    async def texttohex(self, ctx, *, text: discord.Option(str, "The text to convert")):
        try:
            hex_output = " ".join("{:02x}".format(ord(char)) for char in text)
        except Exception as e:
            return await ctx.respond(
                f"Error: `{e}`. This probably means the text is malformed"
            )
        if len(hex_output) <= 1999:
            return await ctx.respond(f"```fix\n{hex_output}```")
        await ctx.respond("Too long to send :(")

    @textconvert.command()
    @commands.check(run_bot_checks)
    async def hextotext(self, ctx, *, text: discord.Option(str, "The text to convert")):
        try:
            text_output = bytearray.fromhex(text).decode()
        except Exception as e:
            return await ctx.respond(
                f"**Error: `{e}`. This probably means the text is malformed**"
            )
        if len(text_output) <= 1999:
            return await ctx.respond(f"```fix\n{text_output}```")
        await ctx.respond("Too long to send :(")

    @textconvert.command()
    @commands.check(run_bot_checks)
    async def texttobinary(
        self, ctx, *, text: discord.Option(str, "The text to convert")
    ):
        try:
            binary_output = " ".join(format(ord(char), "b") for char in text)
        except Exception as e:
            return await ctx.respond(
                f"**Error: `{e}`. This probably means the text is malformed."
            )
        if len(binary_output) <= 1999:
            return await ctx.respond(f"```fix\n{binary_output}```")
        await ctx.respond("Too long to send :(")

    @textconvert.command()
    @commands.check(run_bot_checks)
    async def binarytotext(
        self, ctx, *, text: discord.Option(str, "The text to convert")
    ):
        try:
            text_output = "".join([chr(int(char, 2)) for char in text.split()])
        except Exception as e:
            await ctx.respond(
                f"**Error: `{e}`. This probably means the text is malformed"
            )
        if len(text_output) <= 1999:
            return await ctx.respond(f"```fix\n{text_output}```")
        await ctx.respond("Too long to send :(")

    @textconvert.command()
    @commands.check(run_bot_checks)
    async def emojify(self, ctx, *, text: discord.Option(str, "The text to convert")):
        emojis = []

        extra = {
            "?": ":question:",
            "!": ":exclamation:",
        }
        numbers = {
            0: ":zero:",
            1: ":one:",
            2: ":two:",
            3: ":three:",
            4: ":four:",
            5: ":five:",
            6: ":six:",
            7: ":seven:",
            8: ":eight:",
            9: ":nine:",
        }

        for char in text.lower():
            if char.isdecimal():
                emojis.append(numbers.get(char, ""))
            elif char.isalpha():
                emojis.append(f":regional_indicator_{char}:")
            elif char in extra:
                emojis.append(extra.get(char, ""))
            else:
                emojis.append(char)

        await ctx.respond(" ".join(emojis))


def setup(client):
    client.add_cog(TextConvert(client))
