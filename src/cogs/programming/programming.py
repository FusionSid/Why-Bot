import inspect
import datetime

import discord
import aiohttp
from bs4 import BeautifulSoup
from discord.ext import commands

import log.log
from utils import blacklisted, WhyBot

class Programming(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client


    @commands.slash_command(name="getcode", description="Get the code for a specific Why-Bot command")
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
        commands_list = list(self.client.application_commands) + list(self.client.commands)
        for command in commands_list:
            if command.name.lower() == name.lower():
                func = command.callback
                filename = inspect.getsourcefile(func).split("/src")[1]
                function_code = inspect.getsource(func).replace("```", "'")

                first_line = func.__code__.co_firstlineno

                function_length = len(function_code.replace("\\n", "").split("\n")[:-1])

                last_line = function_length + first_line - 1

                if len(function_code) > 1990:
                    return await ctx.send(embed=discord.Embed(title="Code to large lmao", description=f"Link to code:\n<https://github.com/FusionSid/Why-Bot/blob/rewrite/src{filename}#L{first_line}-L{last_line}>", color=ctx.author.color))

                return await ctx.respond(
                    f"""```py\n\t# Code for the: {func.__name__} function / {command.name} command\n\t# Code written by FusionSid#3645\n\n{function_code}\n```\n<https://github.com/FusionSid/Why-Bot/blob/rewrite/src{filename}#L{first_line}-L{last_line}>"""
                )
        await ctx.respond(embed=discord.Embed(title="Get Code", description="Command not found!", color=ctx.author.color), ephemeral=True)


    @commands.slash_command(name="get_command_doc", description="Get the doc string for a command")
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
        commands_list = list(self.client.application_commands) + list(self.client.commands)
        for command in commands_list:
            if command.name.lower() == name.lower():
                func = command.callback
                cmd = command
                break
        if func is None:
            return await ctx.respond(embed=discord.Embed(title="Get Command Doc", description="Command not found!", color=ctx.author.color), ephemeral=True)

        doc_string = func.__doc__.split("\n")
        doc_string = [i.strip() for i in doc_string]
        doc_string = "\n".join(doc_string)
        em = discord.Embed(
            title=f"Doc String for {cmd}",
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
            description=f'```py\n"""\n{doc_string}\n"""\n```',
        )

        await ctx.respond(embed=em)



    @commands.slash_command(name="pydoc", description="Search the python3 documentation")
    @commands.check(blacklisted)
    async def pydoc(self, ctx, *, query):
        """
        This command is used to search the python docs

        Help Info:
        ----------
        Category: Programming

        Usage: pydoc <query>
        """
        text = query.strip('`')

        url = "https://docs.python.org/3/genindex-all.html"

        em = discord.Embed(title="Python3 docs search", color=ctx.author.color)
        em.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/242px-Python-logo-notext.svg.png')

        async with aiohttp.ClientSession() as client_session:
            async with client_session.get(url) as response:
                if response.status != 200:
                    em.description = 'An error occurred (status code: {response.status}). Retry later.'
                    return await ctx.respond(embed=em)
    

                soup = BeautifulSoup(str(await response.text()), 'lxml')

                def soup_match(tag):
                    return all(string in tag.text for string in text.strip().split()) and tag.name == 'li'

                elements = soup.find_all(soup_match, limit=10)
                links = [tag.select_one("li > a") for tag in elements]
                links = [link for link in links if link is not None]
    

                if not links:
                    em.description = "No results found :("
                    return await ctx.respond(embed=em)

                content = [f"[`{a.string}`](https://docs.python.org/3/{a.get('href')})" for a in links]
                if len(content) > 10:
                    content = content[:3]
                content = '\n'.join(content)
                # content = '\n'.join([f"{index+1}: {item}" for index, item in enumerate(content)])
                em.description = f"Results for `{text}` :\n {content}"
                return await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Programming(client))