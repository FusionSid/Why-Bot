import re
import discord
from discord.ext import commands
from discord.commands import default_permissions

from core.models import WhyBot
from core.helpers.checks import run_bot_checks


class Banning(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    @commands.slash_command()
    @default_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, reason=None):
        if (
            ctx.author.top_role.position > member.top_role.position
            and (ctx.guild.get_member(self.client.user.id)).top_role.position
            > member.top_role.position
        ):
            if reason is not None:
                reason = f"{reason} - Requested by {ctx.author.name} ({ctx.author.id})"
            await member.ban(
                reason="".join(
                    reason
                    if reason is not None
                    else f"Requested by {ctx.author} ({ctx.author.id})"
                )
            )
            await ctx.respond(f"Banned {member} successfully.")
        else:
            await ctx.respond(
                "Sorry, you cannot perform that action due to role hierarchy\nMake sure"
                " both you and the bot have higher perms then the target member"
            )

    @commands.slash_command()
    @default_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def massban(
        self,
        ctx,
        members: discord.Option(str, "User ids or ping users seperated by a space"),
        reason=None,
    ):
        try:
            members = [int(i) for i in re.sub("\<|\>|@", "", members).split(" ")]
        except ValueError:
            return await ctx.respond("Invalid input was provided", ephemeral=True)
        banned_members = []
        for member in members:
            try:
                member = await self.client.fetch_user(member)
            except discord.NotFound:
                continue
            if (
                ctx.author.top_role.position > member.top_role.position
                and (ctx.guild.get_member(self.client.user.id)).top_role.position
                > member.top_role.position
            ):
                if reason is not None:
                    reason = (
                        f"{reason} - Requested by {ctx.author.name} ({ctx.author.id})"
                    )
                await member.ban(
                    reason="".join(
                        reason
                        if reason is not None
                        else f"Requested by {ctx.author} ({ctx.author.id})"
                    )
                )
                banned_members.append(member)

        names = "- \n".join([member.name for member in banned_members])
        em = discord.Embed(
            title="Banned Members",
            description=f"**Banned {len(banned_members)} members:**\n{names}",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"Could not ban {len(members)-len(banned_members)} members",
            value="- \n".join(
                [member.name for member in members if member not in banned_members]
            ),
        )
        await ctx.respond(embed=em)

    @commands.slash_command()
    @default_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, reason=None):
        if (
            ctx.author.top_role.position > member.top_role.position
            and (ctx.guild.get_member(self.client.user.id)).top_role.position
            > member.top_role.position
        ):
            if reason is not None:
                reason = f"{reason} - Requested by {ctx.author.name} ({ctx.author.id})"
            await member.kick(
                reason="".join(
                    reason
                    if reason is not None
                    else f"Requested by {ctx.author} ({ctx.author.id})"
                )
            )
            await ctx.respond(f"Kicked {member} successfully.")
        else:
            await ctx.respond(
                "Sorry, you cannot perform that action due to role hierarchy\nMake sure"
                " both you and the bot have higher perms then the target member"
            )

    @commands.slash_command()
    @default_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def masskick(
        self,
        ctx,
        members: discord.Option(str, "User ids or ping users seperated by a space"),
        reason=None,
    ):
        try:
            members = [int(i) for i in re.sub("\<|\>|@", "", members).split(" ")]
        except ValueError:
            return await ctx.respond("Invalid input was provided", ephemeral=True)
        kicked_members = []
        for member in members:
            try:
                member = await self.client.fetch_user(member)
            except discord.NotFound:
                continue
            if (
                ctx.author.top_role.position > member.top_role.position
                and (ctx.guild.get_member(self.client.user.id)).top_role.position
                > member.top_role.position
            ):
                if reason is not None:
                    reason = (
                        f"{reason} - Requested by {ctx.author.name} ({ctx.author.id})"
                    )
                await member.kick(
                    reason="".join(
                        reason
                        if reason is not None
                        else f"Requested by {ctx.author} ({ctx.author.id})"
                    )
                )
                kicked_members.append(member)

        names = "- \n".join([member.name for member in kicked_members])
        em = discord.Embed(
            title="kickned Members",
            description=f"**Kicked {len(kicked_members)} members:**\n{names}",
            color=ctx.author.color,
        )
        em.add_field(
            name=f"Could not kick {len(members)-len(kicked_members)} members",
            value="- \n".join(
                [member.name for member in members if member not in kicked_members]
            ),
        )
        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Banning(client))
