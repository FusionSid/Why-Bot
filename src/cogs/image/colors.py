import io

import discord
import aiohttp
from PIL import Image
from discord.ext import commands


class Colors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def get_colors(
        self, ctx: discord.ApplicationContext, file: discord.Attachment
    ):
        await ctx.defer()
        file = await file.read()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.fusionsid.xyz/api/image/get_colors/?show_hex=true",
                data={"image": file},
            ) as resp:
                response = await resp.json()
                if resp.ok is False:
                    return await ctx.respond(
                        embed=discord.Embed(
                            title="An error occured while trying to get the image",
                            description=(
                                "This could be because you didnt upload an image\n"
                                "If not the API basically had a skill issue.\n"
                                "If this persists and you are able to, report this as a bug with </bug:0> :)"
                            ),
                            color=discord.Colour.red(),
                        ),
                        ephemeral=True,
                    )

        palette_joined = "\n".join(response["palette"])
        em = discord.Embed(
            title="Image Colors",
            description=f"**Dominant Color:** {response['dominant_color']}\n**Palette:**\n{palette_joined}",
            color=discord.Color.random(),
        )

        dcolor_img = Image.new("RGB", (150, 150), response["dominant_color"])
        dcolor_file = io.BytesIO()
        dcolor_img.save(dcolor_file, "PNG")
        dcolor_file.seek(0)

        palette_img = Image.new("RGB", (300, 200))
        x, y = 0, 0
        for i in response["palette"]:
            try:
                palette_img.paste(Image.new("RGB", (100, 100), i), (x, y))
            except ValueError:
                pass
            x += 100
            if x == 400:
                x = 0
                y += 100

        palette_file = io.BytesIO()
        palette_img.save(palette_file, "PNG")
        palette_file.seek(0)

        await ctx.respond(
            embed=em,
            files=[
                discord.File(dcolor_file, "dominant_color.png"),
                discord.File(palette_file, "palette.png"),
            ],
        )


def setup(client):
    client.add_cog(Colors(client))
