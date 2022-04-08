import inspect
import datetime

import discord
from discord.ext import commands
from discord.commands import slash_command

import log.log
from utils import WhyBot, blacklisted
from utils.views import CalculatorView


class Utilities(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.command(name="calculate", description="Interactive button calculator")
    @commands.check(blacklisted)
    async def calculate(self, ctx):
        """
        This command is used to show an interactive button calculator

        Help Info:
        ----------
        Category: Utilities

        Usage: calculate
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
        """
        This command is used to make a suggestion for the bot

        Help Info:
        ----------
        Category: Utilities

        Usage: suggest <suggestion: str>
        """
        if self.client.config.suggestion_channel == 0 or self.client.config.suggestion_channel == None: return await ctx.send("Bot owner has disabled suggestions")

        try:
            channel = await self.client.fetch_channel(self.client.config.suggestion_channel)
        except discord.errors.NotFound:
            return await ctx.send("Bot owner has disabled suggestions")

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
        """
        This command is used to get the code for a specific command
        It is useful if you want to quickly check the code for a command without opening the github
        It also provides a link to the github link with the code highlighted

        Help Info:
        ----------
        Category: Programming

        Usage: getcode <name: str>
        """
        for command in self.client.commands:
            if command.name.lower() == name.lower():
                func = command.callback
                filename = inspect.getsourcefile(func).split("/Why-Bot/src")[1]
                function_code = inspect.getsource(func).replace("```", "'")

                first_line = func.__code__.co_firstlineno

                function_length = len(function_code.replace("\\n", "").split("\n")[:-1])

                last_line = function_length + first_line - 1

                if len(function_code) > 1990:
                    return await ctx.send(embed=discord.Embed(title="Code to large lmao", description=f"Link to code:\n<https://github.com/FusionSid/Why-Bot/blob/rewrite/src{filename}#L{first_line}-L{last_line}>", color=ctx.author.color))

                return await ctx.send(
                    f"""```py\n\t# Code for the: {func.__name__} function / {command.name} command\n\t# Code written by FusionSid#3645\n\n{function_code}\n```\n<https://github.com/FusionSid/Why-Bot/blob/rewrite/src{filename}#L{first_line}-L{last_line}>"""
                )


    @commands.command()
    async def get_command_doc(self, ctx, name: str):
        """
        This command is used to get the doc string for a function
        Its kinda like a raw help command

        Help Info:
        ----------
        Category: Programming

        Usage: get_command_doc <name: str>
        """
        func, cmd = None, None
        for command in self.client.commands:
            if command.name.lower() == name.lower():
                func = command.callback
                cmd = command
                break

        if func is None:
            return await ctx.send("Command not found")

        doc_string = func.__doc__.split("\n")
        doc_string = [i.strip() for i in doc_string]
        doc_string = "\n".join(doc_string)
        em = discord.Embed(
            title=f"Doc String for {cmd}",
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
            description=f'```py\n"""\n{doc_string}\n"""\n```',
        )

        await ctx.send(embed=em)

    @commands.command()
    async def invite(self, ctx):
        """
        This command is used to make a 10 day invite for the server

        Help Info:
        ----------
        Category: Utilities

        Usage: invite
        """
        link = await ctx.channel.create_invite(max_age=10)
        await ctx.send(link)

    @commands.command()
    async def botinvite(self, ctx):
        """
        This command is used to get the invite link for the bot

        Help Info:
        ----------
        Category: Utilities

        Usage: botinvite
        """
        await ctx.send(
            embed=discord.Embed(
                title="Invite **Why?** to your server:",
                description="[Why Invite Link](https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands)",
                color=ctx.author.color,
            )
        )

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """
        This command is used to get the avatar for a member

        Help Info:
        ----------
        Category: Utilities

        Usage: avatar [member: discord.Member (default=You)]
        """
        if member is None:
            member = ctx.author
        em = discord.Embed(title=f"{member.name}'s Avatar:", color=member.color)
        em.set_image(url=member.avatar.url)
        await ctx.send(embed=em)


def setup(client: WhyBot):
    client.add_cog(Utilities(client))
