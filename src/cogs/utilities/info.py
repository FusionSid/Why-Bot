import time
import datetime

import psutil
import discord
import platform
from discord.ext import commands

from core.models import WhyBot
from core.helpers.views import BotInfoView
from core.utils.count_lines import get_lines
from core.helpers.checks import run_bot_checks
from core.utils.formatters import discord_timestamp


class Info(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    async def get_info(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        roles = list(member.roles)
        em = discord.Embed(
            title="User Info",
            description=f"For: {member.name}{' [BOT]' if member.bot else ''}\nDisplay Name: {member.display_name}",
            color=ctx.author.color,
        )
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

        if member.bot:
            em.add_field(
                name="Bot Status",
                value=(
                    f"Bot is {'' if member.public_flags.verified_bot else 'not '}a"
                    " verified bot"
                ),
            )

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

    @commands.slash_command(name="info", description="Gets info on a member")
    async def info(self, ctx, member: discord.Member = None):
        """
        This command is used to get info on a member
        """
        await self.get_info(ctx, member)

    @commands.user_command(name="Get User Info")
    async def info_user_cmd(self, ctx, member: discord.Member):
        if member.id == self.client.user.id:
            return await self.botinfo(ctx)

        await self.get_info(ctx, member)

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
        created_text = (
            "**Server"
            f' Created:**\n{await discord_timestamp(created_at, "md_yt")} ({await discord_timestamp(created_at, "ts")})'
        )

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
            title=f"Why Bot v{self.client.version}",
            description="Just Why?",
            color=discord.Color.random(),
        )

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
            name="Active User Count",
            value=len(
                await self.client.db.fetch("SELECT DISTINCT user_id FROM command_stats")
            ),
        )
        em.add_field(
            inline=True,
            name="Command Count",
            value=f"{len(self.client.application_commands)} commands",
        )
        em.add_field(
            inline=True, name="Ping", value=f"{round(self.client.latency * 1000)}ms"
        )
        em.add_field(
            inline=True,
            name="Uptime",
            value=f"{(await self.client.uptime)} (since {await discord_timestamp(int(self.client.last_login_time.timestamp()), 'md_yt')})",
        )
        em.add_field(inline=True, name="CPU Usage", value=f"{psutil.cpu_percent()}%")
        em.add_field(
            inline=True,
            name="Memory Usage",
            value=(
                f"{psutil.virtual_memory().percent}% of"
                f" ({round((psutil.virtual_memory().total/1073741824), 2)}GB)"
            ),
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
            name="Lines of python code",
            value=f"{(await get_lines(self.client.redis))} lines of code",
        )
        em.add_field(
            inline=True,
            name="User ID:",
            value=self.client.user.id,
        )
        em.set_thumbnail(url=self.client.user.avatar.url)
        em.set_footer(
            text="Made by FusionSid#3645",
            icon_url=self.client.get_user(self.client.owner_id).avatar.url,
        )
        await ctx.respond(embed=em, view=BotInfoView())

    @commands.slash_command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        em = discord.Embed(title=f"{member.name}'s Avatar:")
        em.set_image(url=member.avatar.url)
        await ctx.respond(embed=em)

    @commands.user_command(name="Get user avatar")
    async def avatar2(self, ctx, member: discord.Member):
        em = discord.Embed(title=f"{member.name}'s Avatar:")
        em.set_image(url=member.avatar.url)
        await ctx.respond(embed=em)

    @commands.command(
        name="invites",
        description="Get the amount of people that a member has invited to the server",
    )
    async def invites(self, ctx, member: discord.Member = None):
        """
        This command is used to get the amount of people that a member has invited to the server
        """
        if member is None:
            member = ctx.author

        total_invites = 0
        for invite in await ctx.guild.invites():
            if invite.inviter == member:
                total_invites += invite.uses

        em = discord.Embed(
            title="Invites",
            # This line has been stolen from simplex bot
            description=(
                f"{member.mention} has invited"
                f" {total_invites} member{'' if total_invites == 1 else 's'} to the"
                " server!"
            ),
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
        )
        await ctx.respond(embed=em)

    @commands.command(
        name="inviteslb", description="Get a leaderboard of the invites in the server"
    )
    async def inviteslb(self, ctx):
        """
        This command is used to get a leaderboard of the invites in the server
        """

        em = discord.Embed(
            title="Leaderboard",
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
        )
        total_invites = {}
        for invite in await ctx.guild.invites():
            try:
                total_invites[invite.inviter.name] += invite.uses
            except KeyError:
                total_invites[invite.inviter.name] = invite.uses
        total_invites = dict(
            sorted(total_invites.items(), reverse=True, key=lambda item: item[1])
        )

        for key, value in total_invites.items():
            if value != 0:
                em.add_field(name=key, value=value, inline=False)

        await ctx.respond(embed=em)


def setup(client: WhyBot):
    client.add_cog(Info(client))
