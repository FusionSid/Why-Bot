import random

import discord
from discord.ext import commands
from discord.ext.commands import clean_content

from utils import blacklisted


class TextConvert(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    @commands.check(blacklisted)
    async def drunkify(self, ctx, *, text: clean_content):
        functions = [str.upper, str.lower]
        drunkified_text = "".join(random.choice(functions)(char) for char in text)
        if len(drunkified_text) <= 1999:
            return await ctx.respond(drunkified_text)
        await ctx.respond("Too long to send :(")

    @commands.slash_command()
    @commands.check(blacklisted)
    async def expand(self, ctx, space: int, *, text: clean_content):
        spacing = " " * space
        result = spacing.join(text)
        if len(result) <= 1999:
            return await ctx.respond(result)
        await ctx.respond("Too long to send :(")

    @commands.slash_command()
    @commands.check(blacklisted)
    async def reverse(self, ctx, *, text: clean_content):
        result = text[::-1]
        if len(result) <= 1999:
            return await ctx.respond(result)
        await ctx.respond("Too long to send :(")

    @commands.slash_command()
    @commands.check(blacklisted)
    async def texttohex(self, ctx, *, text):
        try:
            hex_output = " ".join("{:02x}".format(ord(char)) for char in text)
        except Exception as e:
            return await ctx.respond(
                f"Error: `{e}`. This probably means the text is malformed"
            )
        if len(hex_output) <= 1999:
            return await ctx.respond(f"```fix\n{hex_output}```")
        await ctx.respond("Too long to send :(")

    @commands.slash_command()
    @commands.check(blacklisted)
    async def hextotext(self, ctx, *, text: clean_content):
        try:
            text_output = bytearray.fromhex(text).decode()
        except Exception as e:
            return await ctx.respond(
                f"**Error: `{e}`. This probably means the text is malformed**"
            )
        if len(text_output) <= 1999:
            return await ctx.respond(f"```fix\n{text_output}```")
        await ctx.respond("Too long to send :(")

    @commands.slash_command()
    @commands.check(blacklisted)
    async def texttobinary(self, ctx, *, text):
        try:
            binary_output = " ".join(format(ord(char), "b") for char in text)
        except Exception as e:
            return await ctx.respond(
                f"**Error: `{e}`. This probably means the text is malformed."
            )
        if len(binary_output) <= 1999:
            return await ctx.respond(f"```fix\n{binary_output}```")
        await ctx.respond("Too long to send :(")

    @commands.slash_command()
    @commands.check(blacklisted)
    async def binarytotext(self, ctx, *, text):
        try:
            text_output = "".join([chr(int(char, 2)) for char in text.split()])
        except Exception as e:
            await ctx.respond(f"**Error: `{e}`. This probably means the text is malformed")
        if len(text_output) <= 1999:
            return await ctx.respond(f"```fix\n{text_output}```")
        await ctx.respond("Too long to send :(")

    @commands.slash_command()
    @commands.check(blacklisted)
    async def emojify(self, ctx, *, text):
        emojis = []
        for s in text.lower():
            if s.isdecimal():
                num2emo = {
                    0: "zero",
                    1: "one",
                    2: "two",
                    3: "three",
                    4: "four",
                    5: "five",
                    6: "six",
                    7: "seven",
                    8: "eight",
                    9: "nine",
                }
                emojis.append(f":{num2emo.get(s)}:")
            elif s.isalpha():
                emojis.append(f":regional_indicator_{s}:")
            else:
                emojis.append(s)
        await ctx.respond(" ".join(emojis))


def setup(client):
    client.add_cog(TextConvert(client))
