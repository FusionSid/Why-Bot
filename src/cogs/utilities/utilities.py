import inspect
import datetime

import discord
from discord.ext import commands
from discord.commands import slash_command

from utils import WhyBot, blacklisted
from utils.views import CalculatorView


class Utilities(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.command(name="calculate", description="Interactive button calculator")
    @commands.check(blacklisted)
    async def calculate(self, ctx):
        """
        This is an interactive calculator which uses buttons. It is simple to use and can calculate expressions

        HELP_INFO
        ---------
            Category: Utilities
            Usage: /calculate
        """
        view = CalculatorView(ctx)
        message = await ctx.send("```\n```", view=view)
        res = await view.wait()
        if res:
            for i in view.children:
                i.disabled = True
        return await message.edit(view=view)

    @commands.command()
    @commands.check(blacklisted)
    async def suggest(self, ctx, *, suggestion):
        """Makes a suggestion"""
        channel = await self.client.fetch_channel(self.client.config.suggestion_channel)
        em = discord.Embed(
            title=f"Suggestion",
            description=suggestion,
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow(),
        )
        em.add_field(name=f"by: {ctx.author.name}", value=f"{ctx.author.id}")
        message = await channel.send(embed=em)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

    @commands.command()
    @commands.check(blacklisted)
    async def getcode(self, ctx, name: str):
        """Gets the code for a function"""
        for command in self.client.commands:
            if command.name.lower() == name.lower():
                func = command.callback
                filename = inspect.getsourcefile(func).split("/Why-Bot/src")[1]
                function_code = inspect.getsource(func).replace("```", "'")

                first_line = func.__code__.co_firstlineno

                function_length = len(function_code.replace("\\n", "").split("\n")[:-1])

                last_line = function_length + first_line - 1

                await ctx.send(
                    f"""```py\n\t# Code for the: {func.__name__} function / {command.name} command\n\t# Code written by FusionSid#3645\n\n{function_code}\n```\n<https://github.com/FusionSid/Why-Bot/blob/rewrite/src{filename}#L{first_line}-L{last_line}>"""
                )


def setup(client: WhyBot):
    client.add_cog(Utilities(client))
