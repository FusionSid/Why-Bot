import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.models import WhyBot
from core.models.tag import Tag
from core.helpers.checks import run_bot_checks


class Tags(commands.Cog):
    def __init__(self, client):
        self.client: WhyBot = client
        self.cog_check = run_bot_checks

    tags = SlashCommandGroup("tag", "Command related to the tags plugin")

    @tags.command()
    @commands.has_permissions(administrator=True)
    async def create(
        self,
        ctx,
        name: str,
        value: discord.Option(str, "The value of the tag", max_value=2000),
    ):
        pass

    @tags.command()
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx, name: str):
        pass


def setup(client):
    client.add_cog(Tags(client))
