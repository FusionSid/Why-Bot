import discord
import aiohttp
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

        response = await post_request(
            "https://zprol.epicpix.ga/api/v1/run",
            body={"code": modal.code},
        )
        if response is None:
            em = discord.Embed(
                title="zProl",
                description="Something went wrong!\n(API probably had a skill issue)",
                color=discord.Color.blue(),
            )
            return await ctx.respond(embed=em)

        desc = "```\n"
        if response["compilation"]["stdout"] != "":
            desc += "stdout:\n" + response["compilation"]["stdout"]
        if response["compilation"]["stderr"] != "":
            desc += "\n\nstderr:\n" + response["compilation"]["stdout"]

        em = discord.Embed(
            title="Output",
            color=discord.Color.blue(),
            description=desc + "\n```",
        )
        if response["run"] is not None or response["run"] != "":
            em.add_field(name="Run:", value=response["run"])

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
