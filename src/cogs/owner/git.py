from subprocess import run

import discord
from discord.ext import commands

from core.models import WhyBot


class Git(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.bin_path = "/usr/bin/"

    @commands.group()
    @commands.is_owner()
    async def git(self, ctx):
        """
        This is a group of git commands
        """
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
        output = run([f"{self.bin_path}git", "pull"], capture_output=True).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.is_owner()
    async def status(self, ctx):
        output = run([f"{self.bin_path}git", "status"], capture_output=True).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.is_owner()
    async def add(self, ctx):
        output = run([f"{self.bin_path}git", "add", "."], capture_output=True).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.is_owner()
    async def commit(self, ctx):
        output = run(
            [f"{self.bin_path}git", "commit", "-m", "'Updated File/s'"],
            capture_output=True,
        ).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.is_owner()
    async def push(self, ctx):
        output = run([f"{self.bin_path}git", "push"], capture_output=True).stdout

        await ctx.send(output.decode())


def setup(client):
    client.add_cog(Git(client))
