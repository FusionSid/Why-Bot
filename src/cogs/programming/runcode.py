import discord
import aiohttp
from discord.ext import commands


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
    async def ricklang(self, ctx):
        modal = CodeInput(title="Code Input")
        await ctx.send_modal(modal)
        await modal.wait()

        if modal.code is None:
            return await ctx.respond("Invalid Input", ephemeral=True)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.fusionsid.xyz/api/runcode",
                json={"code": modal.code, "language": "rickroll_lang"},
            ) as resp:
                response = await resp.json()
            if resp.status != 200:
                em = discord.Embed(
                    title="Rickroll-Lang",
                    description="Something went wrong!\n(API probably had a skill issue)",
                    color=discord.Color.blue(),
                )
                await ctx.respond(embed=em)

        em = discord.Embed(
            title="Output",
            color=discord.Color.blue(),
            description=f"""```\n{response['stdout']}\n```""",
        )

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(RunCode(client))
