import discord
import os
import platform
import json
from discord import role
from discord.ext import commands
from discord.ext.commands.core import command
from discord import Option
from discord.commands import slash_command
import psutil

def get_lines():
    lines = 0
    files = ['main.py', 'keep_alive.py', 'add_help.py', 'cogs/Economy.py', 'cogs/Fun.py', 'cogs/Fusion.py', 'cogs/Google.py', 'cogs/Help.py', "cogs/Minecraft.py", "cogs/Moderation.py", "cogs/Music.py", "cogs/Other.py", "cogs/Reddit.py", "cogs/Slash.py", "cogs/TextConvert.py", "cogs/Ticket.py", "cogs/Utilities.py"]
    for i in files:
        count = 0
        with open(i, 'r') as f:
            for line in f:
                count += 1
        lines += count
    return lines

class Other(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=10)
        await ctx.send(link)

    @commands.command(aliases=['bot'])
    async def botinvite(self, ctx):
        await ctx.send(embed=discord.Embed(title="Invite **Why?** to your server:", description="https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"))

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        if member == None:
            return await ctx.send("?info person <@person>\nYou didnt @ the member")
        roles = [role for role in member.roles]
        em = discord.Embed(title="Person Info",
                            description=f"For: {member.name}")
        em.add_field(name="ID:", value=member.id)
        em.set_thumbnail(url=member.avatar.url)
        em.add_field(name="Created Account:", value=member.created_at.strftime(
            "%a, %#d, %B, %Y, #I:%M %p UTC"))
        em.add_field(name="Joined Server:", value=member.joined_at.strftime(
            "%a, %#d, %B, %Y, #I:%M %p UTC"))
        em.add_field(name=f"Roles ({len(roles)}):", value=" ".join(
            role.mention for role in roles))
        await ctx.send(embed=em)

    @commands.command(aliases=['sug'])
    async def suggest(self, ctx, *, suggestion):
        sid = await self.client.fetch_channel(925157029092413460)
        await sid.send(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.send("Thank you for you suggestion!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! jk\n{round(self.client.latency * 1000)}ms")

    @commands.command()
    async def serverinfo(self, ctx):
        role_count = len(ctx.guild.roles)
        list_of_bots = [
            bot.mention for bot in ctx.guild.members if bot.bot]
        em = discord.Embed(
            title="Server Info:", description=f"For: {ctx.guild.name}", color=ctx.author.color)
        em.add_field(name="Member Count:", value=ctx.guild.member_count)
        em.add_field(name="Number of roles:", value=str(role_count))
        em.add_field(name="Bots", value=", ".join(list_of_bots))
        await ctx.send(embed=em)
    
    @commands.command()
    async def botinfo(self, ctx):
        em = discord.Embed(title = 'Why Bot', description = 'just why?')
        em.add_field(inline = False,name="Server Count", value=f"{len(self.client.guilds)}")
        mlist = []
        for i in list(self.client.get_all_members()):
            mlist.append(i.name)
        em.add_field(inline = False,name="User Count", value=len(mlist))
        em.add_field(inline = False,name="Ping", value=f"{round(self.client.latency * 1000)}ms")
        em.set_footer(text="Mostly made by FusionSid#3645")
        em.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
        em.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
        em.add_field(name = 'Available Memory', value = f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%', inline = False)
        em.add_field(inline = False,name="Python version", value= f"{platform.python_version()}")
        em.add_field(inline = False,name="Running on", value=f"{platform.system()} {platform.release()}")
        em.add_field(name="Python code", value=f"{get_lines()} of code")
        await ctx.send(embed = em)

    @commands.command()
    async def cuse(self, ctx):
        with open('./database/userdb.json') as f:
            data = json.load(f)
        for i in data:
            if i["user_id"] == ctx.author.id:
                cuse = i["command_count"]
        await ctx.send(f"You have used Why Bot {cuse} times")        
        
def setup(client):
    client.add_cog(Other(client))
