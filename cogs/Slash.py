import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client


    @cog_ext.cog_slash(name="sus", description="When its too sus lol")
    async def _sus(self, ctx: SlashContext):
        embed = discord.Embed(title="Ayo!", description="Thats kinda sus ngl!")
        await ctx.send(embed=embed)


    @cog_ext.cog_slash(name="ping", description="Displays the bots ping")
    async def _ping(self, ctx: SlashContext):
        await ctx.send(embed=discord.Embed(title="***Ping***", description=f"{round(self.client.latency * 1000)}ms"))


    @cog_ext.cog_slash(name="invite", description="Creates an invite to your server")
    async def _invite(self, ctx: SlashContext):
        link = await ctx.channel.create_invite(max_age=10)
        await ctx.send(link)


    @cog_ext.cog_slash(name='botinvite', description="Invite Why to your server")
    async def _botinvite(self, ctx: SlashContext):
        await ctx.send(embed=discord.Embed(title="Invite **Why?** to your server:", description="https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"))

    @cog_ext.cog_slash(name='suggest', description="Suggest a feature for the bot",
                       options=[
                           create_option(
                               name="suggestion",
                               description="The suggestion",
                               option_type=3,
                               required=True
                           )
                       ])
    async def _suggest(self, ctx, *, suggestion):
        sid = await self.client.fetch_user(624076054969188363)
        await sid.send(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.send("Thank you for you suggestion!")


def setup(client):
    client.add_cog(Slash(client))
