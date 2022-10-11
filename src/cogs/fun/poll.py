import discord
from discord.ext import commands

from core.models import WhyBot
from core.helpers.checks import run_bot_checks


class Poll(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    @commands.slash_command(description="Makes a Yah or Nah poll")
    @commands.guild_only()
    async def yesorno(self, ctx, *, message):
        msg = await ctx.respond(
            embed=discord.Embed(
                title="Yah or Nah?", description=message, color=ctx.author.color
            )
        )
        msg = await msg.original_message()
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")


def setup(client):
    client.add_cog(Poll(client))
