import random

import discord
import pyfiglet
import discord_colorize
from discord.commands import SlashCommandGroup
from discord.ext import commands

from core.helpers.checks import run_bot_checks

colors = discord_colorize.Colors()
fonts = pyfiglet.FigletFont.getFonts()
for idx, font in enumerate(fonts):
    fonts[idx] = font.replace("_", "")
fonts = dict(zip(fonts, pyfiglet.FigletFont.getFonts()))


class TextConvert(commands.Cog):
    def __init__(self, client):
        self.client = client

    textconvert = SlashCommandGroup("text", "Convert text to something else")

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

    @textconvert.command()
    @commands.check(run_bot_checks)
    async def ascii(
        self,
        ctx,
        message: str,
        color: discord.Option(
            str,
            default="nocolor",
            choices=["red", "yellow", "blue", "green", "gray", "pink", "cyan", "white"],
        ),
        font: discord.Option(str, "The font to do the ascii art with") = "big",
    ):
        if fonts.get(font) is None:
            return await ctx.respond(
                embed=discord.Embed(
                    title="Invalid Font!",
                    description=f'Available Fonts:\n{", ".join(fonts.keys())}',
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

        if color == "nocolor":
            message = f"```\n{pyfiglet.figlet_format(message, font=fonts[font])}\n```"
        else:
            message = f"```ansi\n{colors.colorize(pyfiglet.figlet_format(message, font=fonts[font]), fg=color)}\n```"

        if len(message) > 4000:
            return await ctx.respond("Text to long to send :(", ephemeral=True)
        await ctx.respond(
            embed=discord.Embed(title="Ascii Art Output:", description=message)
        )


def setup(client):
    client.add_cog(TextConvert(client))
