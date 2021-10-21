import discord
from discord.ext import commands

class Other(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def invite(self, ctx):
    link = await ctx.channel.create_invite(max_age=10)
    await ctx.send(link)
  
  @commands.command()
  async def botinvite(self, ctx):
    await ctx.send(embed=discord.Embed(title="Invite **Why?** to your server:", description = "https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"))
  
def setup(client):
    client.add_cog(Other(client))