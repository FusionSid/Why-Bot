import io
import inspect

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from core.models import WhyBot
from core.helpers.checks import run_bot_checks


class WhyBotDev(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    why_dev = SlashCommandGroup(
        "whydev", "Why bot development info and programming commands"
    )

    # @why_dev.command(name="getcode", description="Get the code for a specific Why-Bot command")
    # @commands.check(run_bot_checks)
    # async def getcode(self, ctx, name: str):
    #     """
    #     This command is used to get the code for a specific command
    #     It is useful if you want to quickly check the code for a command without opening the github
    #     It also provides a link to the github link with the code highlighted

    #     Help Info:
    #     ----------
    #     Category: Programming

    #     Usage: getcode <name: str>
    #     """
    #     commands_list = []
    #     for cmd in self.client.application_commands:
    #         if isinstance(cmd, discord.SlashCommandGroup):
    #             continue
    #         commands_list.append(cmd)

    #     for command in commands_list:
    #         if command.name.lower() == name.lower():
    #             func = command.callback
    #             filename = inspect.getsourcefile(func).split("/src")[1]
    #             function_code = inspect.getsource(func).replace("```", "'")

    #             first_line = func.__code__.co_firstlineno

    #             function_length = len(function_code.replace("\\n", "").split("\n")[:-1])

    #             last_line = function_length + first_line - 1

    #             if len(function_code) > 1500:
    #                 return await ctx.send(embed=discord.Embed(title="Code to large lmao", description=f"Link to code:\n<https://github.com/FusionSid/Why-Bot/blob/rewrite-the-rewrite/src{filename}#L{first_line}-L{last_line}>", color=ctx.author.color))

    #             return await ctx.respond(
    #                 f"""```py\n\t# Code for the: {func.__name__} function/command\n\t# Written by FusionSid#3645 :)\n\n{function_code}\n```\n<https://github.com/FusionSid/Why-Bot/blob/rewrite/src{filename}#L{first_line}-L{last_line}>"""
    #             )
    #     await ctx.respond(embed=discord.Embed(title="Get Code", description="Command not found!", color=ctx.author.color), ephemeral=True)

    # @why_dev.command()
    # async def get_all_commands(self, ctx):
    #     file = io.BytesIO("\n".join(i.name for i in self.client.application_commands).encode())
    #     await ctx.respond(file=discord.File(file, "commands.txt"))

    @why_dev.command()
    async def uptime(self, ctx):
        """
        This command is used to get the uptime for the bot
        """

        em = discord.Embed(
            title="Why bot uptime",
            description=f"I has been online for: {await self.client.uptime}",
            color=ctx.author.color,
        )
        await ctx.respond(embed=em)

    @why_dev.command(name="ping", description="Shows the bot's ping")
    @commands.check(run_bot_checks)
    async def ping(self, ctx):
        """
        This command is used to get the ping for the bot
        """

        await ctx.respond(f"Pong!\n{round(self.client.latency * 1000)}ms")


def setup(client):
    client.add_cog(WhyBotDev(client))
