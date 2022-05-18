import datetime

import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.Cog.listener()
    # async def on_message_edit(self, before, after):
    #     if after.author.id == self.client.user.id:
    #         return

    #     em = discord.Embed(
    #         title="Message Edit", 
    #         description=f"{before.author} edited their message", 
    #         color=discord.Color.blue(), 
    #         timestamp = after.edited_at
    #     )

    #     em.add_field(name="Before", value=before.content)
    #     em.add_field(name="After", value=after.content)


    


def setup(client):
    client.add_cog(Logging(client))