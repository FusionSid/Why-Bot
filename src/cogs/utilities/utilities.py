from io import BytesIO

import qrcode
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.helpers.views import CalculatorView
from core.utils.calc import slow_safe_calculate
from core.helpers.checks import run_bot_checks


class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_check = run_bot_checks

    utilities = SlashCommandGroup("utilities", "Utility Commands")

    @utilities.command(name="calculator", description="Interactive button calculator")
    async def calculator(self, ctx: discord.ApplicationContext):
        """This command is used to show an interactive button calculator"""

        await ctx.defer()

        view = CalculatorView(ctx)
        await ctx.respond("```\n```", view=view)

    @utilities.command()
    async def calculate(self, ctx: discord.ApplicationContext, expression: str):
        em = discord.Embed(
            title="Calculation Result",
            description=f"**Expression:**\n{expression}",
            color=discord.Color.random(),
        )

        result = await slow_safe_calculate(expression)
        em.add_field(name="Result", value=result)

        await ctx.respond(embed=em)

    @utilities.command(name="invite", description="Create an invite for the server")
    @commands.has_permissions(create_instant_invite=True)
    @commands.bot_has_permissions(create_instant_invite=True)
    async def invite(
        self,
        ctx: discord.ApplicationContext,
        expire_in: str = None,
        max_uses: str = None,
    ):
        """This command is used to make an invite for the server"""

        expire_in = 0 if expire_in is not None else expire_in
        max_uses = 0 if max_uses is not None else max_uses

        link = await ctx.channel.create_invite(max_age=expire_in, max_uses=max_uses)
        await ctx.respond(link)

    @utilities.command()
    async def qrcode(
        self,
        ctx: discord.ApplicationContext,
        url: str,
        color: str = "black",
        background_color: str = "white",
    ):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(url))
        qr.make(fit=True)
        try:
            img = qr.make_image(fill_color=color, back_color=background_color).convert(
                "RGB"
            )
        except ValueError:
            img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        image = BytesIO()
        img.save(image, "PNG")
        image.seek(0)
        await ctx.respond(file=discord.File(image, "qrcode.png"))


def setup(client):
    client.add_cog(Utilities(client))
