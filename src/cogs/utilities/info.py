import time
import datetime

import psutil
import discord
import platform
from discord.ext import commands

from core.models import WhyBot
from core.utils.count_lines import get_lines
from core.helpers.checks import run_bot_checks
from core.utils.formatters import discord_timestamp


class Info(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    @commands.slash_command(name="info", description="Gets info on a member")
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
        emojis = self.client.get_why_emojies
        if str(member.status) == "online":
            status = f"{emojis['online']} Online"
        elif str(member.status) == "offline":
            status = f"{emojis['offline']} Offline"
        elif str(member.status) == "dnd":
            status = f"{emojis['dnd']} Do not disturb"
        elif str(member.status) == "invisible":
            status = f"{emojis['offline']} Invisible"
        elif str(member.status) == "idle":
            status = f"{emojis['idle']} Idle"
        else:
            status = f"{emojis['online']} Online"

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
    async def serverinfo(self, ctx: commands.Context):
        """
        This command is used to get info on the server
        """
        GUILD = ctx.guild

        text = len(GUILD.text_channels)
        voice = len(GUILD.voice_channels)
        total = len(GUILD.channels)
        other = total - (text + voice)
        categories = len(GUILD.categories)
        channel_text = f"""**Channels:**
            **{text}** Text channels
            **{voice}** Voice channels
            **{other}** Other channel types
            **{total}** Total Channels
            **{categories}** Total Categories"""

        members = GUILD.members
        humans = len([m for m in members if not m.bot])
        bots = len(members) - humans
        member_text = f"""**Members:**
            **{humans}** Humans
            **{bots}** Bots
            **{len(members)}** Total Members"""

        emojis_text = f"**Emoji Count:**\n{len(GUILD.emojis)}"
        role_text = f"**Role Count:**\n{len(GUILD.roles)}"

        created_at = int(time.mktime(GUILD.created_at.timetuple()))
        created_text = f'**Server Created:**\n{await discord_timestamp(created_at, "md_yt")} ({await discord_timestamp(created_at, "ts")})'

        server_id_text = f"**Server ID:** {GUILD.id}"
        level_text = f"""\
        **Verification Level:** {GUILD.verification_level.name}
        **2FA:** {'on' if bool(GUILD.mfa_level) else 'off'}
        **NSFW Level:** {GUILD.nsfw_level.name}"""

        feature_text = "**Features:**\n" + ", ".join(GUILD.features)

        things = "\n\n".join(
            [
                channel_text,
                member_text,
                emojis_text,
                role_text,
                created_text,
                level_text,
                feature_text,
            ]
        )
        description = f"{server_id_text}\n\n{things}"

        em = discord.Embed(
            title=f"Server Info for {ctx.guild.name}",
            description=description,
            color=ctx.author.color,
        )
        em.set_author(
            name=f"Server Owner: {ctx.guild.owner.name}",
            icon_url=ctx.guild.owner.avatar.url,
        )
        em.set_thumbnail(url=ctx.guild.icon.url)

        await ctx.respond(embed=em)

    @commands.slash_command(name="botinfo", description="Gets info on Why Bot")
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
