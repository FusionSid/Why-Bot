import discord
from discord.ext import commands

from core.models.client import WhyBot
from core.models.counting import CountingData
from core.db.setup_guild import setup_counting


class Counting(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author.bot:
            return

        counting_data = await self.get_counting_data()
        if counting_data is None:
            await setup_counting(self.client.db, message.guild.id)

    async def get_counting_data(self, guild_id: int):
        data = await self.client.db.fetch(
            "SELECT * FROM counting WHERE guild_id=$1", guild_id
        )
        if not len(data):
            return None

        return CountingData(*data[0])


def setup(client):
    client.add_cog(Counting(client))
