import discord
from discord.ext import commands

class Help(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def help(self, ctx, cat=None):

    if cat == None:
      pass

    else:
      if cat.lower() == 'database':
        embed = discord.Embed(
          title="Database Commands",
          color=0x515596
        )
        embed.add_field(name="?genkey",value="Generates a key for encrypting and decrypting")
        embed.add_field(name="?store",value="Encrypts text and stores it in a database. Can only be encrypted/decrypted with a key")
        embed.add_field(name="?get",value="Gets items")

        return await ctx.send(embed=embed)

      if cat.lower() == 'economy':
        embed = discord.Embed(
          title="Economy Commands",
          color=0x515596
        )

      if cat.lower() == 'fun':
        embed = discord.Embed(
          title="Fun Commands",
          color=0x515596
        )

        return await ctx.send(embed=embed)

      if cat.lower() == 'google':
        embed = discord.Embed(
          title="Google Commands",
          color=0x515596
        )

        return await ctx.send(embed=embed)

      if cat.lower() == 'minecraft':
        embed = discord.Embed(
          title="Minecraft Commands",
          color=0x515596
        )

        return await ctx.send(embed=embed)

      if cat.lower() == 'moderation':
        embed = discord.Embed(
          title="Moderation Commands",
          color=0x515596
        )

        return await ctx.send(embed=embed)

      if cat.lower() == 'music':
        embed = discord.Embed(
          title="Music Commands",
          color=0x515596
        )

        embed.add_field(name="?join", value="Why joins to your voice channel.", inline=False)
        embed.add_field(
          name="?play youtube-video-link (or search)",
          value="Bot joins to your voice channel and plays music from a video link.",
          inline=False
        )
        embed.add_field(name="?leave", value="Leave the voice channel.", inline=False)
        embed.add_field(name="?skip", value="Skips current track.", inline=False)
        embed.add_field(name="?pause", value="Pause music.", inline=False)
        embed.add_field(name="?resume", value="Resume music.", inline=False)
        embed.add_field(name="?queue", value="Shows current queue.", inline=False)
        embed.add_field(name="?loop", value="Loops current track.", inline=False)

        return await ctx.send(embed=embed)

      if cat.lower() == 'text':
        embed = discord.Embed(
          title="Text Commands",
          color=0x515596
        )

        return await ctx.send(embed=embed)

      if cat.lower() == 'utilities':
        embed = discord.Embed(
          title="Utilites Commands",
          color=0x515596
        )

        return await ctx.send(embed=embed)

      if cat.lower() == 'other':
        pass

      if cat.lower() == 'reddit':
        pass

      else:
        await ctx.send("```Invalid Category\nCategories List:\ndatabase, economy fun, google, minecraft, moderation, music, reddit, text, utilities, counting and other```")
  
def setup(client):
    client.add_cog(Help(client))
