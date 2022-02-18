import discord
import datetime
import json
from utils.checks import plugin_enabled
import os
import time
import platform
from discord.ext import commands
import psutil

async def get_lines():
    lines = 0
    files = []
    for i in os.listdir():
        if i.endswith(".py"):
            files.append(i)
    for i in os.listdir("cogs/"):
        for file in os.listdir('cogs/'+i):
            if file.endswith(".py"):
                files.append(f"cogs/{i}/{file}")
    for i in os.listdir("utils/"):
        if i.endswith(".py"):
            files.append(f"utils/{i}")
    for i in files:
        count = 0
        with open(i, 'r') as f:
            for line in f:
                count += 1
        lines += count
    return lines

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(extras={"category": "Utilities"}, usage="info [@user]", help="This command shows a message with info on a user.", description="Returns info on a user")
    @commands.check(plugin_enabled)
    async def info(self, ctx, member: discord.Member = None):
        if member == None:
            return await ctx.send(f"{ctx.prefix}info person <@person>\nYou didnt @ the member")
        roles = [role for role in member.roles]
        em = discord.Embed(title="Person Info",
                           description=f"For: {member.name}", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        if str(member.status) == "online":
            status = "🟢 Online"
        elif str(member.status) == "offline":
            status = "🔴 Offline"
        elif str(member.status) == "dnd":
            status = '⛔ Do not disturb'
        elif str(member.status) == "invisible":
            status = "🔴 Invisible"
        elif str(member.status) == "idle":
            status = "🌙 Idle"
        elif str(member.status) == "streaming":
            status = "📷 Streaming"
        else:
            status = member.status
        em.add_field(name="Status:", value=status, inline=False)

        em.add_field(name="ID:", value=member.id, inline=False)
        em.set_thumbnail(url=member.avatar.url)
        em.add_field(name="Created Account:",
                     value=f"<t:{int(time.mktime(member.created_at.timetuple()))}>", inline=False)
        em.add_field(name="Joined Server:",
                     value=f"<t:{int(time.mktime(member.joined_at.timetuple()))}>", inline=False)
        em.add_field(name="Highest Role:",
                     value=member.top_role.mention, inline=False)

        data = await self.client.get_db()
        warnings = data[str(ctx.guild.id)]['warnings']
        if str(member.id) not in warnings:
            em.add_field(name="Warnings", value="This user has no warnings")
        else:
            em.add_field(name="Warnings", value=len(warnings[str(member.id)]))
        if len(roles) > 15:
            em.add_field(name="Roles:", value=f"{len(roles)}", inline=False)
        else:
            em.add_field(name=f"Roles ({len(roles)}):", value=" ".join(
                role.mention for role in roles), inline=False)
        await ctx.send(embed=em)

    @commands.command(extras={"category": "Utilities"}, usage="ping", help="Shows the bots ping", description="Shows bot ping")
    @commands.check(plugin_enabled)
    async def ping(self, ctx):
        await ctx.send(f"Pong! jk\n{round(self.client.latency * 1000)}ms")

    @commands.command(extras={"category": "Utilities"}, usage="serverinfo", help="Returns info on this server.", description="shows server info")
    @commands.check(plugin_enabled)
    async def serverinfo(self, ctx):
        em = discord.Embed(
            title="Server Info:", description=f"For: {ctx.guild.name}", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.set_thumbnail(url=ctx.guild.icon.url)
        em.set_author(
            name=f"Guild Owner: {ctx.guild.owner.name}", icon_url=ctx.guild.owner.avatar.url)
        em.add_field(
            name="Channels:", value=f"**Text:** {len(ctx.guild.text_channels)}\n**Voice:** {len(ctx.guild.voice_channels)}")
        em.add_field(name="Roles:", value=len(ctx.guild.roles))
        bots = 0
        members = 0
        for i in ctx.guild.members:
            if i.bot:
                bots += 1
            else:
                members += 1
        em.add_field(
            name="Members:", value=f"**Total:** {ctx.guild.member_count}\n**Humans:** {members}\n**Bots:** {bots}")
        em.add_field(
            name="Created: ", value=f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}>")
        em.add_field(name="ID:", value=ctx.guild.id)
        await ctx.send(embed=em)

    @commands.command(extras={"category": "Utilities"}, usage="botinfo", help="This command shows info on the bot", description="Info about Why bot")
    @commands.check(plugin_enabled)
    async def botinfo(self, ctx):
        with open("./database/userdb.json") as f:
            data = json.load(f)
        active = len(data)
        em = discord.Embed(title='Why Bot', description='Just Why?', color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.add_field(inline=True, name="Server Count",
                     value=f"{len(self.client.guilds)}")
        mlist = []
        for i in list(self.client.get_all_members()):
            mlist.append(i.name)
        em.add_field(inline=True, name="User Count", value=len(mlist))
        em.add_field(inline=True, name="Command Count",
                     value=f"{len(self.client.commands)} commands")
        em.add_field(inline=True, name="Active User Count", value=active)
        em.add_field(inline=True, name="Ping",
                     value=f"{round(self.client.latency * 1000)}ms")
        em.add_field(inline=True, name="Uptime", value=(await self.client.uptime))
        em.set_footer(text="Made by FusionSid#3645")
        em.add_field(name='CPU Usage',
                     value=f'{psutil.cpu_percent()}%', inline=True)
        em.add_field(name='Memory Usage',
                     value=f'{psutil.virtual_memory().percent}% of ({round((psutil.virtual_memory().total/1073741824), 2)}GB)', inline=True)
        em.add_field(name='Available Memory',
                     value=f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%', inline=True)
        em.add_field(inline=True, name="Python version",
                     value=f"{platform.python_version()}")
        em.add_field(inline=True, name="Running on",
                     value=f"{platform.system()} {platform.release()}")
        em.add_field(name="Python code", value=f"{(await get_lines())} of code")
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(plugin_enabled)
    async def uptime(self, ctx):
        await ctx.send(embed=discord.Embed(title="Uptime:", description=f"I have been up for: **{(await self.client.uptime)}**"))


def setup(client):
    client.add_cog(Info(client))