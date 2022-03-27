from subprocess import run

import discord
from discord.ext import commands


class Git(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cwd = "/usr/bin/"

    @commands.group()
    @commands.is_owner()
    async def git(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        else:
            cmds = ["git pull", "git status", "git add", "git commit", "git push"]
            return await ctx.send(
                embed=discord.Embed(
                    title=f"Git Commands",
                    description=f"\n{ctx.prefix}".join(cmds),
                    color=ctx.author.color,
                )
            )

    @git.command()
    @commands.is_owner()
    async def pull(self, ctx):
        output = run([f"{self.cwd}git", "pull"], capture_output=True).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.is_owner()
    async def status(self, ctx):
        output = run([f"{self.cwd}git", "status"], capture_output=True).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.is_owner()
    async def add(self, ctx):
        output = run([f"{self.cwd}git", "add", "."], capture_output=True).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.is_owner()
    async def commit(self, ctx):
        output = run(
            [f"{self.cwd}git", "commit", "-m", "'Updated File'"], capture_output=True
        ).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.is_owner()
    async def push(self, ctx):
        output = run([f"{self.cwd}git", "push"], capture_output=True).stdout

        await ctx.send(output.decode())


def setup(client):
    client.add_cog(Git(client))
