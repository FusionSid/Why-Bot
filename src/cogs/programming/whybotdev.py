import io
import inspect
import datetime

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from core.models import WhyBot
from core.helpers.checks import run_bot_checks
from core.helpers.http import get_request


class WhyBotDev(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    why_dev = SlashCommandGroup(
        "whydev", "Why bot development info and programming commands"
    )

    @why_dev.command(
        name="getcode", description="Get the code for a specific Why-Bot command"
    )
    async def getcode(self, ctx, name: str):
        """
        This command is used to get the code for a specific command
        It is useful if you want to quickly check the code for a command without opening the github
        It also provides a link to the github link with the code highlighted

        Help Info:
        ----------
        Category: Programming

        Usage: getcode <name: str>
        """
        commands_list = []
        for cmd in self.client.application_commands:
            if isinstance(cmd, discord.SlashCommandGroup):
                continue
            commands_list.append(cmd)

        for command in commands_list:
            if command.name.lower() == name.lower():
                func = command.callback
                filename = inspect.getsourcefile(func).split("/src")[1]
                function_code = inspect.getsource(func).replace("```", "'")
                first_line = func.__code__.co_firstlineno

                function_length = len(function_code.replace("\\n", "").split("\n")[:-1])

                last_line = function_length + first_line - 1

                if len(function_code) > 1750:
                    file = io.BytesIO(function_code.encode())

                    return await ctx.respond(
                        embed=discord.Embed(
                            title="Code to large to fit in a message",
                            description=f"<https://github.com/FusionSid/Why-Bot/blob/rewrite-the-rewrite/src{filename}#L{first_line}-L{last_line}>",
                            color=ctx.author.color,
                        ),
                        file=discord.File(file, "command.py"),
                    )

                return await ctx.respond(
                    f"""```py\n\t# Code for the: {func.__name__} function/command\n\n{function_code}\n```\n<https://github.com/FusionSid/Why-Bot/blob/rewrite/src{filename}#L{first_line}-L{last_line}>"""
                )
        await ctx.respond(
            embed=discord.Embed(
                title="Get Code",
                description="Command not found!",
                color=ctx.author.color,
            ),
            ephemeral=True,
        )

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
    async def ping(self, ctx):
        """
        This command is used to get the ping for the bot
        """

        await ctx.respond(f"Pong!\n{round(self.client.latency * 1000)}ms")

    @why_dev.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        """
        This command is used to make a suggestion for the bot
        """

        suggestion_channel = self.client.config["suggestion_channel"]

        error_embed = discord.Embed(
            title="Error getting suggestion channel",
            description="Most likely cause: Bot owner has disabled suggestions",
        )

        try:
            channel = await self.client.fetch_channel(suggestion_channel)
        except discord.errors.NotFound:
            return await ctx.respond(embed=error_embed)

        if suggestion_channel == 0 or suggestion_channel is None:
            return await ctx.respond(embed=error_embed)

        em = discord.Embed(
            title=f"Suggestion",
            description=suggestion,
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
        )

        em.add_field(name="Suggested By:", value=ctx.author.name, inline=False)

        message = await channel.send(content=ctx.author.id, embed=em)

        await message.add_reaction("✅")
        await message.add_reaction("❌")

        await ctx.respond("Thank you for the suggestion :)")

    @why_dev.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def bug(self, ctx, *, bug):
        em = discord.Embed(
            title="Bug Report",
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
            description=bug,
        )

        em.add_field(name="Report By:", value=ctx.author.name)

        bug_channel = self.client.config["bug_report_channel"]

        error_embed = discord.Embed(
            title="Error getting suggestion channel",
            description="Most likely cause: Bot owner has disabled bug reports",
        )

        try:
            channel = await self.client.fetch_channel(bug_channel)
        except discord.errors.NotFound:
            return await ctx.respond(embed=error_embed)

        if bug_channel == 0 or bug_channel is None:
            return await ctx.respond(embed=error_embed)

        await channel.send(content=ctx.author.id, embed=em)
        await ctx.respond("Thank you for the bug report :)")

    @why_dev.command(
        name="botinvite", description="Get a link to invite Why-Bot to the server"
    )
    async def botinvite(self, ctx: discord.commands.ApplicationContext):
        """
        This command is used to get the invite link for the bot
        """
        interaction = await ctx.respond(
            embed=discord.Embed(
                title="Invite **Why?** to your server:",
                description=(
                    "[Why Invite"
                    " Link](https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands)"
                ),
                color=ctx.author.color,
            )
        )
        message = await (await interaction.original_message())
        await message.add_reaction("🔗")
        react_check = (
            lambda reaction, user: user.id == ctx.author.id
            and reaction.emoji == "🔗"
            and reaction.message.id == message.id
        )
        await self.client.wait_for("reaction_add", check=react_check, timeout=30.0)
        await ctx.respond(
            "https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"
        )

    @why_dev.command()
    async def recent_commit(self, ctx):
        # URL = "https://api.github.com/repos/FusionSid/Why-Bot/commits/master"
        URL = (
            "https://api.github.com/repos/FusionSid/Why-Bot/commits/rewrite-the-rewrite"
        )
        response = await get_request(URL)
        if response is None:
            em = discord.Embed(
                title="An error occured while trying to get the commit",
                description=(
                    "API basically had a skill issue.\nIf this persists and you are able to, report this as a bug with </bug:0> :)"
                ),
                color=discord.Colour.red(),
            )
            return await ctx.respond(embed=em, ephemeral=True)

        em = discord.Embed(
            title="Why Bot - Most Recent Commit",
            description=f"Commit: [{response.get('sha')}]({response.get('html_url')})",
            color=discord.Color.random(),
        )
        if (commit_info := response.get("committer")) is not None:
            em.set_author(
                name=f"Author: {commit_info.get('login')}",
                icon_url=commit_info.get("avatar_url"),
            )
        if response.get("commit") is not None:
            em.add_field(name="Message:", value=response["commit"].get("message"))

        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(WhyBotDev(client))
