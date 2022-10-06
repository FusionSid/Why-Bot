import time
import datetime

import psutil
import discord
import platform
from discord.ext import commands

from core.models import WhyBot
from core.utils.count_lines import get_lines
from core.helpers.checks import blacklist_check


class Info(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.slash_command(name="info", description="Gets info on a member")
    @commands.check(blacklist_check)
    async def info(self, ctx, member: discord.Member = None):
        """
        This command is used to get info on a member
        """

        if member == None:
            member = ctx.author

        roles = [role for role in member.roles]
        em = discord.Embed(
            title="Person Info",
            description=f"For: {member.name}",
            color=ctx.author.color,
        )
        em.timestamp = datetime.datetime.utcnow()

        if str(member.status) == "online":
            status = "🟢 Online"
        elif str(member.status) == "offline":
            status = "🔴 Offline"
        elif str(member.status) == "dnd":
            status = "⛔ Do not disturb"
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
        em.add_field(
            name="Created Account:",
            value=f"<t:{int(time.mktime(member.created_at.timetuple()))}>",
            inline=False,
        )
        em.add_field(
            name="Joined Server:",
            value=f"<t:{int(time.mktime(member.joined_at.timetuple()))}>",
            inline=False,
        )
        em.add_field(name="Highest Role:", value=member.top_role.mention, inline=False)

        if len(roles) > 15:
            em.add_field(name="Roles:", value=f"{len(roles)}", inline=False)
        else:
            em.add_field(
                name=f"Roles ({len(roles)}):",
                value=" ".join(role.mention for role in roles),
                inline=False,
            )

        em.set_thumbnail(url=member.avatar.url)

        await ctx.respond(embed=em)

    @commands.slash_command(name="serverinfo", description="Shows server info")
    @commands.guild_only()
    @commands.check(blacklist_check)
    async def serverinfo(self, ctx):
        """
        This command is used to get info on the server
        """

        em = discord.Embed(
            title="Server Info:",
            description=f"For: {ctx.guild.name}",
            color=ctx.author.color,
        )

        em.add_field(
            name="Channels:",
            value=f"**Text:** {len(ctx.guild.text_channels)}\n**Voice:** {len(ctx.guild.voice_channels)}",
        )
        em.add_field(name="Roles:", value=len(ctx.guild.roles))

        bots = 0
        members = 0

        for member in ctx.guild.members:
            if member.bot:
                bots += 1
            else:
                members += 1

        em.add_field(
            name="Members:",
            value=f"**Total:** {ctx.guild.member_count}\n**Humans:** {members}\n**Bots:** {bots}",
        )
        em.add_field(
            name="Created: ",
            value=f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}>",
        )
        em.add_field(name="ID:", value=ctx.guild.id)

        em.set_author(
            name=f"Server Owner: {ctx.guild.owner.name}",
            icon_url=ctx.guild.owner.avatar.url,
        )
        em.set_thumbnail(url=ctx.guild.icon.url)

        em.timestamp = datetime.datetime.utcnow()

        await ctx.respond(embed=em)

    @commands.slash_command(name="botinfo", description="Gets info on Why Bot")
    @commands.check(blacklist_check)
    async def botinfo(self, ctx):
        """
        This command is used to get info on the bot
        """

        em = discord.Embed(
            title="Why Bot", description="Just Why?", color=ctx.author.color
        )

        em.timestamp = datetime.datetime.utcnow()

        em.add_field(
            inline=True, name="Server Count", value=f"{len(self.client.guilds)}"
        )
        em.add_field(
            inline=True,
            name="User Count",
            value=len(list(self.client.get_all_members())),
        )
        em.add_field(
            inline=True,
            name="Command Count",
            value=f"{len(self.client.application_commands)} commands",
        )
        em.add_field(inline=True, name="Active User Count", value="e")
        em.add_field(
            inline=True, name="Ping", value=f"{round(self.client.latency * 1000)}ms"
        )
        em.add_field(inline=True, name="Uptime", value=(await self.client.uptime))
        em.add_field(inline=True, name="CPU Usage", value=f"{psutil.cpu_percent()}%")
        em.add_field(
            inline=True,
            name="Memory Usage",
            value=f"{psutil.virtual_memory().percent}% of ({round((psutil.virtual_memory().total/1073741824), 2)}GB)",
        )
        em.add_field(
            inline=True,
            name="Available Memory",
            value=f"{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%",
        )
        em.add_field(
            inline=True, name="Python version", value=f"{platform.python_version()}"
        )
        em.add_field(
            inline=True,
            name="Running on",
            value=f"{platform.system()} {platform.release()}",
        )
        em.add_field(
            inline=True,
            name="Python code",
            value=f"{(await get_lines(self.client.redis))} lines of code",
        )

        em.set_footer(text="Made by FusionSid#3645")
        await ctx.respond(embed=em)


def setup(client: WhyBot):
    client.add_cog(Info(client))
