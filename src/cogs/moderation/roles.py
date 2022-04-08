import datetime

import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.edit_role_mentions = discord.AllowedMentions(users=False,everyone=False,roles=False,replied_user=False)

    
    @commands.command(name = "giverole", description="gives role / roles to a member")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def giverole(self, ctx : commands.Context, member: discord.Member, roles: commands.Greedy[discord.Role]):
        for role in roles:
            if role in member.roles:
                em = discord.Embed(
                    title="Member already has role",
                    description="Role: {} is already in member: {}'s list of roles".format(role.mention, member.mention),
                    color=discord.Color.red(),
                )
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em, allowed_mentions=self.edit_role_mentions)

                roles.remove(role)

            try:
                await member.add_roles(role)

            except discord.errors.Forbidden:
                em = discord.Embed(
                    title="Missing permissions",
                    description="You don't have permissions to give role: {} to member: {}".format(role.mention, member.mention),
                    color=discord.Color.red(),
                )
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em, allowed_mentions=self.edit_role_mentions)

                await ctx.message.add_reaction("⚠️")

                roles.remove(role)
                continue
        
        if len(roles) == 0:
            return
        
        em = discord.Embed(
            title="Role Given" if len(roles) == 1 else "Roles Given",
            description=f"Member: {member.mention} has been given role: {roles[0].mention}" if len(roles) == 1 else f"Member: {member.mention} has been given roles: {''.join([role.mention for role in roles])}",
            color = member.color,
            timestamp=datetime.datetime.now()
        )
        em.set_footer(text=f"Role given by {ctx.author.name}" if len(roles) == 1 else f"Roles given by {ctx.author.name}")

        await ctx.send(embed=em, allowed_mentions=self.edit_role_mentions)


    @commands.command(name = "takerole", description="removes role / roles from a member")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def takerole(self, ctx : commands.Context, member: discord.Member, roles: commands.Greedy[discord.Role]):
        for role in roles:
            if role not in member.roles:
                em = discord.Embed(
                    title="Member doesn't have role",
                    description="Role: {} is not in member: {}'s list of roles".format(role.mention, member.mention),
                    color=discord.Color.red(),
                )
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em, allowed_mentions=self.edit_role_mentions)

                roles.remove(role)
                continue

            try:
                await member.remove_roles(role)

            except discord.errors.Forbidden:
                em = discord.Embed(
                    title="Missing permissions",
                    description="You don't have permissions to remove role: {} to member: {}".format(role.mention, member.mention),
                    color=discord.Color.red(),
                )
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em, allowed_mentions=self.edit_role_mentions)

                await ctx.message.add_reaction("⚠️")

                roles.remove(role)

        if len(roles) == 0:
            return

        
        em = discord.Embed(
            title="Role Removed" if len(roles) == 1 else "Roles Removed",
            description=f"Role: {roles[0].mention} has been removed from Member: {member.mention}" if len(roles) == 1 else f"Roles: {''.join([role.mention for role in roles])} has been removed from {member.mention}",
            color = member.color,
            timestamp=datetime.datetime.now()
        )
        em.set_footer(text=f"Role removed by {ctx.author.name}" if len(roles) == 1 else f"Roles removed by {ctx.author.name}")

        await ctx.send(embed=em, allowed_mentions=self.edit_role_mentions)



def setup(client):
    client.add_cog(Roles(client))