import discord
from discord.ext import commands

from main import WhyBot
from log import log_errors
from main import get_prefix
from utils import update_activity


class OnEvent(commands.Cog):
    def __init__(self, client : WhyBot):
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message):
        """
        This is the event that is called when a message is sent in a channel
        It will check if the bot has been mentioned in the message and if so 
            it will reply with a message containing the guild prefix
        """

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
        """
        Runs when the bot is ready
        Prints a message to console and updates the bot's activity
        """
        print("Bot is ready")
        await update_activity(self.client)
        


def setup(client : WhyBot):
    client.add_cog(OnEvent(client))