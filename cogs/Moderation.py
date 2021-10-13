import discord
from discord.ext import commands
import os
import json

class Moderation(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def report(self,ctx,type_:str):
    def wfcheck(m):
      return m.channel == ctx.channel and m.author == ctx.author
    cd = os.getcwd()
    os.chdir("/home/runner/Why-Bot/Setup")
    with open(f"{ctx.guild.id}.json") as f:
      content = json.load(f)
    if content[0]["mod_channel"] == None:
      return
    else:
      channel = int(content[0]["mod_channel"])
    os.chdir(cd)
    em = discord.Embed(title="REPORT")

    if type_.lower() == "member":

      await ctx.send("Enter the @ of the member")
      member = await self.client.wait_for("message", check=wfcheck)
      member = member.content
      await ctx.send("Please give a short description about why you are reporting this person")
      reason = await self.client.wait_for("message", check=wfcheck)
      reporter = reason.author
      reason = reason.content
      em.description = "Member Report"
      em.add_field(name="Member:", value=member)
      em.add_field(name="Reason:", value=reason)
      em.add_field(name="Report By:", value=reporter)
      cha = await self.client.fetch_channel(channel)
      await cha.send(embed=em)

    elif type_.lower() == "message":

      await ctx.send("Enter the id of the message")
      messageid = await self.client.wait_for("message", check=wfcheck)
      messageid = messageid.content

      try:
        int(messageid)
      except:
        return

      await ctx.send("Please give a short description about why you are reporting this message")
      reason = await self.client.wait_for("message", check=wfcheck)
      reporter = reason.author
      reason = reason.content

      message = await ctx.channel.fetch_message(messageid)
      messagecontent = message.content
      messageauthor = message.author

      em.description = "Message Report"
      em.add_field(name="Message Id:", value=messageid)
      em.add_field(name="Reason:", value=reason)
      em.add_field(name="Message Content:", value=messagecontent)
      em.add_field(name="Message Author:", value=messageauthor)
      em.add_field(name="Report By:", value=reporter)
      cha = await self.client.fetch_channel(channel)
      await cha.send(embed=em)

    elif type_.lower() == "bug":

      await ctx.send("Please give a short description about the issure/bug")
      reason = await self.client.wait_for("message", check=wfcheck)
      reporter = reason.author
      reason = reason.content
      em.description = "Bug Report"
      em.add_field(name="Reason", value=reason)
      em.add_field(name="Report By:", value=reporter)

      cha = await self.client.fetch_channel(896932591620464690)
      await cha.send(embed=em)
      
  @commands.command()
  async def giverole(self,ctx,role:discord.Role, user:discord.Member):
    pass
  
  @commands.command()
  async def takerole(self,ctx,role:discord.Role, user:discord.Member):
    pass
  
  @commands.command()
  async def ban(self,ctx,user:discord.Member):
    pass

  @commands.command()
  async def kick(self,ctx,user:discord.Member):
    pass

  @commands.command()
  async def lockdown(self,ctx, channel:discord.TextChannel=None):
    channel = channel or ctx.channel

    if ctx.guild.default_role not in channel.overwrites:
      overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
      }
      await ctx.send(embed=discord.Embed(title="Channel is now in lockdown"))
      await channel.edit(overwites=overwrites)
  
  @commands.command()
  async def clear(self,ctx,amount:int):
    await ctx.channel.purge(limit=amount+1)

def setup(client):
    client.add_cog(Moderation(client))


