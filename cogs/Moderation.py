import discord
from discord.ext import commands
import os
import json
import aiofiles

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
  @commands.has_permissions(administrator=True)
  async def giverole(self,ctx,role:discord.Role, user:discord.Member):
    await user.add_roles(role)
    await ctx.send(f"{user} has been given the {role} role")
  

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def takerole(self,ctx,role:discord.Role, user:discord.Member):
    await user.remove_roles(role)
    await ctx.send(f"{role} has been removed from {user}")
  

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def ban(self,ctx,user:discord.Member, *, reason=None):
    await user.ban(reason=reason)
    await ctx.send(f"User {user} has been banned")


  @commands.command()
  @commands.has_permissions(administrator=True)
  async def kick(self,ctx,user:discord.Member, *, reason=None):
    await user.kick(reason=reason)
    await ctx.send(f"User {user} has been kicked")


  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def lockdown(self,ctx, channel:discord.TextChannel=None):
    if channel == None:
      channel = ctx.channel
    await channel.send("Channel is now in lockdown")
    await channel.set_permissions(ctx.guild.default_role, send_messages=False)
  

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def unlock(self,ctx, channel:discord.TextChannel=None):
    if channel == None:
      channel = ctx.channel
    await channel.send("Channel is no longer in lockdown")
    await channel.set_permissions(ctx.guild.default_role, send_messages=True)
  

  @commands.command()
  async def clear(self,ctx,amount:int):
    await ctx.channel.purge(limit=amount+1)

  
  @commands.command()
  @commands.has_permissions(administrator=True)
  async def reactrole(self, ctx, emoji, role: discord.Role, *, message):
      embedVar = discord.Embed(description=message)
      msg = await ctx.channel.send(embed=embedVar)
      await msg.add_reaction(emoji)
      cd = os.getcwd()
      os.chdir("/home/runner/Why-Bot/")
      with open("reactrole.json") as json_file:
          data = json.load(json_file)

          new_react_role = {
              "role_name": role.name,
              "role_id": role.id,
              "emoji": emoji,
              "message_id": msg.id,
          }

          data.append(new_react_role)

      with open("reactrole.json", "w") as f:
          json.dump(data, f, indent=4)

      os.chdir(cd)

def setup(client):
    client.add_cog(Moderation(client))


