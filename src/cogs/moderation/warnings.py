import time
import datetime

import discord
import aiosqlite
from discord.ext import commands

from utils import blacklisted


async def warn_member(guild_id: int, member: discord.Member, reason: str):
    time_right_now = int(time.time())
    async with aiosqlite.connect("database/main.db") as db:
        await db.execute(
            "INSERT INTO Warnings (guild_id, member_id, time, reason) VALUES (?, ?, ?, ?)",
            (guild_id, member.id, time_right_now, reason),
        )
        await db.commit()


async def get_warnings(guild_id: int, member_id: int):
    async with aiosqlite.connect("database/main.db") as db:
        data = await db.execute(
            "SELECT * FROM Warnings WHERE member_id=? AND guild_id=?",
            (member_id, guild_id),
        )
        data = await data.fetchall()
        if len(data) == 0:
            return None
        return data


class Warnings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(blacklisted)
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
        await warn_member(ctx.guild.id, member, reason)
        em = discord.Embed(
            title="Member Warned",
            description=f"{member.name} was warned by {ctx.author.name}",
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
        )
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(blacklisted)
    @commands.has_permissions(administrator=True)
    async def warnings(self, ctx, member: discord.Member):
        warnings = await get_warnings(ctx.guild.id, member.id)
        if warnings is None:
            return await ctx.send("Member has no warnings")
        em = discord.Embed(
            title="Warnings",
            description=f"List of warnings for {member.mention}",
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
        )
        for warning in warnings:
            reason = warning[3]
            time_rn = warning[2]

            em.add_field(name=f"<t:{time_rn}>", value=reason)
        await ctx.send(embed=em)

    @commands.command()
    @commands.check(blacklisted)
    @commands.has_permissions(administrator=True)
    async def clear_warnings(self, ctx, member: discord.Member):
        async with aiosqlite.connect("database/main.db") as db:
            await db.execute(
                "DELETE FROM Warnings WHERE member_id=? AND guild_id=?",
                (member.id, ctx.guild.id),
            )
            await db.commit()

        em = discord.Embed(
            title="Member Warnings Cleared",
            description=f"{ctx.author.name} cleared all {member.name}'s warnings",
            color=ctx.author.color,
            timestamp=datetime.datetime.now(),
        )
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Warnings(client))
