import discord
from discord.ext import commands
import json

async def get_log_channel(self, guild):
    with open("./database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == guild.id:
            channel = i['log_channel']
            if channel == None:
              return None
            return await self.client.fetch_channel(channel)

class Log(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
      em = None
      em = discord.Embed(title="Message Edit", description=f"{before.author} edited their message")
      em.add_field(name="Before", value=before.content)
      em.add_field(name="After", value=after.content)
      
      channel = await get_log_channel(self, before.guild)
      if channel == None:
        return
      else:
        await channel.send(embed=em)

  @commands.Cog.listener()
  async def on_message_delete(self, message):
      em = None
      em = discord.Embed(title="Message Delete",description=f"{message.author} has deleted the message")
      em.add_field(name="Content:", value=f"{message.content}")

      channel = await get_log_channel(self, message.guild)
      if channel == None:
        return
      else:
        await channel.send(embed=em)


  @commands.Cog.listener()
  async def on_member_ban(self, guild, user):
    em = None
    em = discord.Embed(title="Member Banned!", description=f"{user.name} Has been banned from the server")
    channel = await get_log_channel(self, guild)
    if channel == None:
      return
    else:
      await channel.send(embed=em)
  
  @commands.Cog.listener()
  async def on_member_unban(self, guild, user):
    em = None
    em = discord.Embed(title="Member Unbanned!", description=f"{user.name} Has been unbanned from the server")
    channel = await get_log_channel(self, guild)
    if channel == None:
      return
    else:
      await channel.send(embed=em)

  @commands.Cog.listener()
  async def on_member_update(self, before, after):
      em = None
      if before.nick is not None and after.nick is None:
        em = discord.Embed(title="Nick Change", description=f"{before.name} has unicked")
        em.add_field(name="Before:", value=before.nick)
        em.add_field(name="After:", value="No Nick")

      if before.nick is None and after.nick is not None:
        em = discord.Embed(title="Nick Change", description=f"{before.name} Has nicked")
        em.add_field(name="Before:", value="No Nick")
        em.add_field(name="After:", value=after.nick)

      elif before.nick != after.nick:
        em = discord.Embed(title="Nick Change", description=f"{before.name} Has changed their nick")
        em.add_field(name="Before:", value=before.nick)
        em.add_field(name="After:", value=after.nick)

      channel = await get_log_channel(self, after.guild)
      if channel == None:
        return
      else:
        await channel.send(embed=em)


  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):
    em=discord.Embed(title="Channel Created", description=f"`{channel.name}` Has been created")
    channel = await get_log_channel(self, channel.guild)
    if channel == None:
      return
    else:
      await channel.send(embed=em)

  @commands.Cog.listener()
  async def on_guild_channel_delete(self, channel):
    em=discord.Embed(title="Channel Delete", description=f"`{channel.name}` Has been deleted")
    channel = await get_log_channel(self, channel.guild)
    if channel == None:
      return
    else:
      await channel.send(embed=em)


def setup(client):
  client.add_cog(Log(client))