import discord
from discord import role
from discord.ext import commands
from discord.ext.commands.core import command

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
  

  @commands.command()
  async def info(self, ctx, cat, member:discord.Member=None):
    if cat.lower() == 'person':
      if member == None:
        return await ctx.send("?info person <@person>\nYou didnt @ the member")
      roles = [role for role in member.roles]
      em = discord.Embed(title="Person Info", description=f"For: {member.name}")
      em.add_field(name="ID:", value=member.id)
      em.set_thumbnail(url=member.avatar_url)
      em.add_field(name="Created Account:", value=member.created_at.strftime("%a, %#d, %B, %Y, #I:%M %p UTC"))
      em.add_field(name="Joined Server:", value=member.joined_at.strftime("%a, %#d, %B, %Y, #I:%M %p UTC"))
      em.add_field(name=f"Roles ({len(roles)}):", value=" ".join(role.mention for role in roles))

      
    if cat.lower() == 'server':
      role_count = len(ctx.guild.roles)
      list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
      em = discord.Embed(title="Server Info:", description = f"For: {ctx.guild.name}", color=ctx.author.color)
      em.add_field(name="Member Count:", value=ctx.guild.member_count)
      em.add_field(name="Number of roles:", value=str(role_count))
      em.add_field(name="Bots", value=", ".join(list_of_bots))
  
  @commands.command()
  async def suggest(self, ctx, *, suggestion):
    sid = self.client.fetch_user()
    await sid.send(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
    await ctx.send("Thank you for you suggestion!")

def setup(client):
    client.add_cog(Other(client))
