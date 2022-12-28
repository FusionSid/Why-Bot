import re

import discord
from discord.ext import commands
from discord.commands import default_permissions

from core import WhyBot, BaseCog


class Roles(BaseCog):
    def __init__(self, client: WhyBot):
        self.edit_role_mentions = discord.AllowedMentions(
            users=False, everyone=False, roles=False, replied_user=False
        )
        super().__init__(client)

    @commands.slash_command(
        name="addrole", description="gives role / roles to a member"
    )
    @default_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def addrole(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        roles: str,
    ):

        try:
            roles = list(map(int, re.findall("\\d+", roles)))
        except ValueError:
            return await ctx.respond("Invalid input was provided", ephemeral=True)

        fetched_roles = []
        for role in roles:
            fetched_role = ctx.guild.get_role(role)
            if fetched_role is None:
                continue

            conditions = [
                ctx.author.top_role.position <= member.top_role.position,
                (ctx.guild.get_member(self.client.user.id)).top_role.position
                <= member.top_role.position,
                ctx.author.top_role.position <= fetched_role.position,
                (ctx.guild.get_member(self.client.user.id)).top_role.position
                <= fetched_role.position,
            ]
            if any(conditions):
                continue

            fetched_roles.append(fetched_role)

        if len(fetched_roles) == 0:
            return await ctx.respond(
                "Unable to give any roles because of permissions", ephemeral=True
            )

        await member.add_roles(*fetched_roles)

        em = discord.Embed(
            title="Role Given" if len(fetched_roles) == 1 else "Roles Given",
            description=f"Member: {member.mention} has been given role: {fetched_roles[0].mention}"
            if len(fetched_roles) == 1
            else f"Member: {member.mention} has been given roles: {''.join([role.mention for role in fetched_roles])}",
            color=discord.Color.random(),
        )
        em.set_footer(
            text=f"Role given by {ctx.author.name}"
            if len(roles) == 1
            else f"Roles given by {ctx.author.name}"
        )

        await ctx.respond(embed=em, allowed_mentions=self.edit_role_mentions)

    @commands.slash_command(
        name="removerole", description="removes role / roles from a member"
    )
    @default_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def removerole(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        roles: str,
    ):
        try:
            roles = list(map(int, re.findall("\\d+", roles)))
        except ValueError:
            return await ctx.respond("Invalid input was provided", ephemeral=True)

        fetched_roles = []
        for role in roles:
            fetched_role = ctx.guild.get_role(role)
            if fetched_role is None:
                continue

            conditions = [
                ctx.author.top_role.position <= member.top_role.position,
                (ctx.guild.get_member(self.client.user.id)).top_role.position
                <= member.top_role.position,
                ctx.author.top_role.position <= fetched_role.position,
                (ctx.guild.get_member(self.client.user.id)).top_role.position
                <= fetched_role.position,
            ]
            if any(conditions):
                continue

            fetched_roles.append(fetched_role)

        if len(fetched_roles) == 0:
            return await ctx.respond(
                "Unable to remove any roles because of permissions", ephemeral=True
            )

        await member.remove_roles(*fetched_roles)

        em = discord.Embed(
            title="Role Removed" if len(fetched_roles) == 1 else "Roles Removed",
            description=f"Member: {member.mention} has had these role removed: {fetched_roles[0].mention}"
            if len(fetched_roles) == 1
            else f"Member: {member.mention} has had these roles removed: \
                {''.join([role.mention for role in fetched_roles])}",
            color=discord.Color.random(),
        )
        em.set_footer(
            text=f"Role removed by {ctx.author.name}"
            if len(roles) == 1
            else f"Roles removed by {ctx.author.name}"
        )

        await ctx.respond(embed=em, allowed_mentions=self.edit_role_mentions)


def setup(client):
    client.add_cog(Roles(client))
