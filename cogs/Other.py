import discord
from discord.ext import commands

class Other(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def invite(self, ctx):
    link = await ctx.channel.create_invite(max_age=10)
    await ctx.send(link)
  
def setup(client):
    client.add_cog(Other(client))