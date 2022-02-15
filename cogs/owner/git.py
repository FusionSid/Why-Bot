import discord
from discord.ext import commands
from utils import is_it_me
from subprocess import run
    
class Git(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cwd = "/usr/bin/"

    @commands.group()
    @commands.check(is_it_me)
    async def git(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        else:
            return await ctx.send(embed=discord.Embed(title=f"Git Commands", description="?git pull\n?git status\n?git add\n?git commit\n?git push", color=ctx.author.color))

    @git.command()
    @commands.check(is_it_me)
    async def pull(self, ctx):
        output = run([f"{self.cwd}git", "pull"], capture_output=True).stdout

        await ctx.send(output.decode())


    @git.command()
    @commands.check(is_it_me)
    async def status(self, ctx):
        output = run([f"{self.cwd}git", "status"], capture_output=True).stdout

        await ctx.send(output.decode())


    @git.command()
    @commands.check(is_it_me)
    async def add(self, ctx):
        output = run([f"{self.cwd}git", "add", "."], capture_output=True).stdout

        await ctx.send(output.decode())


    @git.command()
    @commands.check(is_it_me)
    async def commit(self, ctx):
        output = run([f"{self.cwd}git", "commit", "-m", "'Updated File'"], capture_output=True).stdout

        await ctx.send(output.decode())


    @git.command()
    @commands.check(is_it_me)
    async def push(self, ctx):
        output = run([f"{self.cwd}git", "push"], capture_output=True).stdout

        await ctx.send(output.decode())

def setup(client):
    client.add_cog(Git(client))