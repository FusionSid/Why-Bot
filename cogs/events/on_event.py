import discord
from discord.ext import commands

from log import log_errors
from main import get_prefix
from utils import update_activity

class OnEvent(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if self.client.user.mentioned_in(message) and message.mention_everyone == False and message.reference is None:
            prefix = await get_prefix(self.client, message)
            em = discord.Embed(
                title=f"Hi, my prefix is `{prefix}`", 
                color=message.author.color
            )
            return await message.channel.send(embed=em)


    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready")
        await update_activity(self.client)


def setup(client):
    client.add_cog(OnEvent(client))