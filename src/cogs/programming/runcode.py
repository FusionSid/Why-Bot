import io
from contextlib import redirect_stdout

import aiohttp
import discord
from aioconsole import aexec
from discord.ext import commands

from core import BaseCog
from core.helpers import GUILD_IDS, post_request, InputModalView


class RunCode(BaseCog):
    @commands.slash_command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def zprol(self, ctx: discord.ApplicationContext):
        modal = InputModalView(label="Please enter the code:", title="Code Input")
        await ctx.send_modal(modal)
        await modal.wait()

        if modal.value is None:
            return await ctx.respond("Invalid Input", ephemeral=True)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://zprol.epicpix.ga/api/v1/run",
                json={"code": modal.value},
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

    @commands.slash_command(description="Run code in the rickroll programming language")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def ricklang(self, ctx: discord.ApplicationContext):
        modal = InputModalView(label="Please enter the code:", title="Code Input")
        await ctx.send_modal(modal)
        await modal.wait()

        if modal.value is None:
            return await ctx.respond("Invalid Input", ephemeral=True)

        response = await post_request(
            "https://api.fusionsid.xyz/api/runcode",
            body={"code": modal.value, "language": "rickroll_lang"},
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

    @commands.slash_command(
        guild_ids=GUILD_IDS, description="Run code in the rickroll programming language"
    )
    @commands.is_owner()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def exec_code(self, ctx: discord.ApplicationContext):
        # this command dangerous af so second check just to make sure:
        if ctx.author.id != self.client.owner_id:
            raise commands.NotOwner

        modal = InputModalView(label="Please enter the code:", title="Code Input")
        await ctx.send_modal(modal)
        await modal.wait()

        if modal.value is None:
            return await ctx.respond("Invalid Input", ephemeral=True)

        locals = {
            "ctx": ctx,
            "client": self.client,
        }

        # Run the code
        stdout = io.StringIO()
        stderr = None
        with redirect_stdout(stdout):
            try:
                await aexec(modal.value, locals)
            except Exception as err:
                stderr = err
        output = stdout.getvalue()

        em = discord.Embed(
            title="Code Output:",
            description=f"```bash\n{output if output else 'No Stdout'}\n```",
            color=discord.Color.random(),
        )
        if stderr is not None:
            em.add_field(
                name="Stderr:",
                value="```bash\n{}: {}\n```".format(type(stderr).__name__, stderr),
            )

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(RunCode(client))
