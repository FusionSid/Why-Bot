import inspect
import datetime

import discord
from discord.ext import commands

from utils import blacklisted

class Programming(commands.Cog):
    def __init__(self, client):
        self.client = client

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
                filename = inspect.getsourcefile(func).split("/src")[1]
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
    @commands.check(blacklisted)
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

def setup(client):
    client.add_cog(Programming(client))