import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.models.client import WhyBot


class CogTools(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    cogtools = SlashCommandGroup(
        "cogtools", "Commands for why bot cogs management. OWNER ONLY"
    )

    @cogtools.command(guild_ids=[763348615233667082, 938913935774605442])
    @commands.is_owner()
    async def reload(self, ctx: discord.ApplicationContext, extension):
        """This command is used to reload a cog"""

        if extension not in self.client.cogs_list.keys():
            return await ctx.respond(
                embed=discord.Embed(
                    title="Cog doesn't exist or was not loaded",
                    description=f"Use listcogs command to check cogs",
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )

        self.client.reload_extension(self.client.cogs_list[extension])
        embed = discord.Embed(
            title="Reload",
            description=f"{extension} successfully reloaded",
            color=ctx.author.color,
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @cogtools.command(guild_ids=[763348615233667082, 938913935774605442])
    @commands.is_owner()
    async def load(self, ctx: discord.ApplicationContext, extension, name):
        """This command is used to load a cog"""

        try:
            self.client.load_extension(extension)
        except discord.ApplicationCommandInvokeError:
            await ctx.respond(
                embed=discord.Embed(
                    title="Cog doesn't exist",
                    description=f"Please provied path properly",
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )
        self.client.cogs_list[name] = extension

        embed = discord.Embed(
            title="Load",
            description=f"{extension} successfully loaded",
            color=ctx.author.color,
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @cogtools.command(guild_ids=[763348615233667082, 938913935774605442])
    @commands.is_owner()
    async def unload(self, ctx: discord.ApplicationContext, extension):
        """This command is used to unload a cog"""

        if extension not in self.client.cogs_list.keys():
            await ctx.respond(
                embed=discord.Embed(
                    title="Cog doesn't exist or was not loaded",
                    description=f"Use listcogs command to check cogs",
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )

        self.client.unload_extension(self.client.cogs_list[extension])
        self.client.cogs_list.pop(extension)

        embed = discord.Embed(
            title="Unload",
            description=f"{extension} successfully unloaded",
            color=ctx.author.color,
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @cogtools.command(guild_ids=[763348615233667082, 938913935774605442])
    @commands.is_owner()
    async def listcogs(self, ctx: discord.ApplicationContext):
        """This command lists the cogs that the bot has"""
        return await ctx.respond(
            embed=discord.Embed(
                title="Why Bot Cogs List",
                description="\n".join(self.client.cogs_list.keys()),
                color=ctx.author.color,
            ),
            ephemeral=True,
        )

    @cogtools.command(guild_ids=[763348615233667082, 938913935774605442])
    @commands.is_owner()
    async def reloadall(self, ctx: discord.ApplicationContext):
        """This command is used to reload all the cogs"""

        cogs = self.client.cogs_list.values()

        for cog in cogs:
            self.client.reload_extension(cog)

        await ctx.respond(
            embed=discord.Embed(title="All Cogs Reloaded", color=ctx.author.color),
            ephemeral=True,
        )


def setup(client: WhyBot):
    client.add_cog(CogTools(client))
