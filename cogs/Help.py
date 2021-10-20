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
        embed = discord.Embed(
          title="Beat Commands",
          color=0x515596
        )

        embed.add_field(name="+join", value="Bot joins to your voice channel.", inline=False)
        embed.add_field(
          name="+play youtube-video-link (or search)",
          value="Bot joins to your voice channel and plays music from a video link.",
          inline=False
        )
        embed.add_field(name="?music", value="Bot joins to your channel and plays lofi.", inline=False)
        embed.add_field(name="?leave", value="Leave the voice channel.", inline=False)
        embed.add_field(name="?skip", value="Skips current track.", inline=False)
        embed.add_field(name="?pause", value="Pause music.", inline=False)
        embed.add_field(name="?resume", value="Resume music.", inline=False)
        embed.add_field(name="?queue", value="Shows current queue.", inline=False)
        embed.add_field(name="?loop", value="Loops current track.", inline=False)
        embed.add_field(name="+commands", value="Shows a list of commands.", inline=False)

        await ctx.send(embed=embed)
        
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
