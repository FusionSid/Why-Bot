import discord
from discord.ext import commands

class Help(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def help(self, ctx, cat=None, cmd=None):

    if cat == None:
      pass

    else:
      
      if cat.lower() == 'database':
        pass

      if cat.lower() == 'economy':
        pass

      if cat.lower() == 'fun':
        pass

      if cat.lower() == 'google':
        pass

      if cat.lower() == 'minecraft':
        pass

      if cat.lower() == 'moderation':
        pass

      if cat.lower() == 'music':
        pass

      if cat.lower() == 'other':
        pass

      if cat.lower() == 'reddit':
        pass

      if cat.lower() == 'text':
        pass

      if cat.lower() == 'utilities':
        pass

      else:
        await ctx.send("```Invalid Category\nCategories List:\ndatabase, economy fun, google, minecraft, moderation, music, reddit, text, utilities, counting and other```")
  
def setup(client):
    client.add_cog(Help(client))
