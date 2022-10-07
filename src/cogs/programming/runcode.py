import aiohttp
import discord
from discord.ext import commands

from core.helpers.http import post_request


class CodeInput(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = None

        self.add_item(
            discord.ui.InputText(
                label="Please enter the code", style=discord.InputTextStyle.long
            )
        )

    async def callback(self, interaction: discord.Interaction):
        self.code = self.children[0].value
        return await interaction.response.send_message(
            "Running code now...", ephemeral=True
        )


class RunCode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def zprol(self, ctx):
        modal = CodeInput(title="Code Input")
        await ctx.send_modal(modal)
        await modal.wait()

        if modal.code is None:
            return await ctx.respond("Invalid Input", ephemeral=True)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://zprol.epicpix.ga/api/v1/run",
                json={"code": modal.code},
            ) as resp:
                try:
                    response = await resp.json()
                except aiohttp.ContentTypeError:
                    response = None

        if response is None or response.get("compilation") is None:
            em = discord.Embed(
                title="zProl",
                description="Something went wrong!\n(API probably had a skill issue)",
                color=discord.Color.blue(),
            )
            return await ctx.respond(embed=em)

        em = discord.Embed(
            title="zProl Code Output",
            color=discord.Color.blue(),
        )

        if response["compilation"]["stderr"] != "":
            em.description = (
                f"**Compilation result:**```{response['compilation']['stderr']}```"
            )
            em.color = discord.Color.red()
        elif response["compilation"]["stdout"] != "":
            em.description = (
                f"**Compilation result:**```{response['compilation']['stdout']}```"
            )

        # If the program produced output
        if response.get("run") is not None and response.get("run") != "":
            em.add_field(name="Program Output:", value=f"```\n{response['run']}\n```")

        await ctx.respond(embed=em)

    @commands.slash_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ricklang(self, ctx):
        modal = CodeInput(title="Code Input")
        await ctx.send_modal(modal)
        await modal.wait()

        if modal.code is None:
            return await ctx.respond("Invalid Input", ephemeral=True)

        response = await post_request(
            "https://api.fusionsid.xyz/api/runcode",
            body={"code": modal.code, "language": "rickroll_lang"},
        )
        if response is None:
            em = discord.Embed(
                title="Rickroll-Lang",
                description="Something went wrong!\n(API probably had a skill issue)",
                color=discord.Color.blue(),
            )
            return await ctx.respond(embed=em)

        em = discord.Embed(
            title="Output",
            color=discord.Color.blue(),
            description=f"""```\n{response['stdout']}\n```""",
        )

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(RunCode(client))
