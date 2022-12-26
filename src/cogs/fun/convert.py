import io
import random

import discord
import pyfiglet
import discord_colorize
from discord.commands import SlashCommandGroup

from core import BaseCog
from core.helpers import get_request_bytes

colors = discord_colorize.Colors()
fonts = pyfiglet.FigletFont.getFonts()
for idx, font in enumerate(fonts):
    fonts[idx] = font.replace("_", "")
fonts = dict(zip(fonts, pyfiglet.FigletFont.getFonts()))


class TextConvert(BaseCog):

    textconvert = SlashCommandGroup("text", "Convert text to something else")

    @textconvert.command(description="Convert text to stickycaps")
    async def stickycaps(
        self,
        ctx: discord.ApplicationContext,
        text: discord.Option(str, "The text to convert"),
    ):
        functions = [str.upper, str.lower]
        result = "".join(random.choice(functions)(char) for char in text)
        if len(result) <= 1999:
            return await ctx.respond(result)
        await ctx.respond("Too long to send :(")

    @textconvert.command(description="Expand some text")
    async def expand(
        self,
        ctx: discord.ApplicationContext,
        space: int,
        text: discord.Option(str, "The text to convert"),
    ):
        spacing = " " * space
        result = spacing.join(text)
        if len(result) <= 1999:
            return await ctx.respond(result)
        await ctx.respond("Too long to send :(")

    @textconvert.command(description="Reverse some text")
    async def reverse(
        self,
        ctx: discord.ApplicationContext,
        text: discord.Option(str, "The text to convert"),
    ):
        result = text[::-1]
        if len(result) <= 1999:
            return await ctx.respond(result)
        await ctx.respond("Too long to send :(")

    @textconvert.command(description="Convert text to hex")
    async def texttohex(
        self,
        ctx: discord.ApplicationContext,
        text: discord.Option(str, "The text to convert"),
    ):
        try:
            hex_output = " ".join(f"{ord(char):02x}" for char in text)
        except Exception as e:
            return await ctx.respond(
                f"Error: `{e}`. This probably means the text is malformed"
            )
        if len(hex_output) <= 1999:
            return await ctx.respond(f"```fix\n{hex_output}```")
        await ctx.respond("Too long to send :(")

    @textconvert.command(description="Convert hex to text")
    async def hextotext(
        self,
        ctx: discord.ApplicationContext,
        text: discord.Option(str, "The text to convert"),
    ):
        try:
            text_output = bytearray.fromhex(text).decode()
        except Exception as e:
            return await ctx.respond(
                f"**Error: `{e}`. This probably means the text is malformed**"
            )
        if len(text_output) <= 1999:
            return await ctx.respond(f"```fix\n{text_output}```")
        await ctx.respond("Too long to send :(")

    @textconvert.command(description="Convert text to binary")
    async def texttobinary(
        self,
        ctx: discord.ApplicationContext,
        text: discord.Option(str, "The text to convert"),
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

    @textconvert.command(description="Convert binary to text")
    async def binarytotext(
        self,
        ctx: discord.ApplicationContext,
        text: discord.Option(str, "The text to convert"),
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

    @textconvert.command(description="Emojify some text")
    async def emojify(
        self,
        ctx: discord.ApplicationContext,
        text: discord.Option(str, "The text to convert"),
    ):
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

    @textconvert.command(description="Create ascii art from the given text")
    async def ascii(
        self,
        ctx: discord.ApplicationContext,
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

    @textconvert.command(description="Convert text to a font and show it as an image")
    async def fontconvert(
        self,
        ctx: discord.ApplicationContext,
        message: str,
        font: str = None,
        color: str = "black",
    ):
        if font is None:
            return await ctx.respond(
                embed=discord.Embed(
                    title="You must specify a font",
                    description=(
                        "[Click this to get a list of fonts you can"
                        " use](https://api.fusionsid.xyz/api/font/list)"
                    ),
                    color=discord.Colour.red(),
                ),
                ephemeral=True,
            )
        URL = "https://api.fusionsid.xyz/api/font/convert"

        text_image = await get_request_bytes(
            URL,
            data={"font": font, "text": message, "text_color": color},
            bytes_io=True,
        )

        if not isinstance(text_image, io.BytesIO):
            return await ctx.respond(
                embed=discord.Embed(
                    title="An error occured while trying to get the image",
                    description=(
                        "This is most likely because you used an invalid font\n        "
                        "                [Click this to get a list of fonts you can"
                        " use](https://api.fusionsid.xyz/api/font/list)"
                    ),
                    color=discord.Colour.red(),
                ),
                ephemeral=True,
            )

        await ctx.respond(file=discord.File(text_image, "text.png"))


def setup(client):
    client.add_cog(TextConvert(client))
