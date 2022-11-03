import asyncio

import discord
from discord.ext import commands
from discord.commands import default_permissions

from core.models import WhyBot
from core.helpers.checks import run_bot_checks


class Channels(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    @commands.slash_command()
    @default_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def create_channel(
        self,
        ctx: discord.ApplicationContext,
        channel_name: str,
        category: discord.CategoryChannel = None,
        slowmode: int = None,
        nsfw: bool = False,
    ):
        try:
            channel = await ctx.guild.create_text_channel(
                channel_name, category=category, slowmode_delay=slowmode, nsfw=nsfw
            )
        except discord.HTTPException:
            return await ctx.respond("Failed to create thing")

        await ctx.respond(
            embed=discord.Embed(
                title="Created te Channel!",
                description=f"Created text channel {channel.mention}",
                color=discord.Color.green(),
            )
        )

    @commands.slash_command()
    @default_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def delete_channel(
        self, ctx: discord.ApplicationContext, channel: discord.TextChannel
    ):
        try:
            await channel.delete()
        except discord.HTTPException:
            return await ctx.respond("Failed to delete the channel")

        await ctx.respond(
            embed=discord.Embed(
                title="Deleted Channel!",
                description=f"Deleted channel {channel.name}",
                color=discord.Color.green(),
            )
        )

    @commands.slash_command()
    @default_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def create_vc(
        self,
        ctx: discord.ApplicationContext,
        channel_name: str,
        category: discord.CategoryChannel = None,
        reason: str = None,
        user_limit: int = None,
    ):
        try:
            channel = await ctx.channel.create_voice_channel(
                channel_name, category=category, reason=reason, user_limit=user_limit
            )
        except discord.HTTPException:
            return await ctx.respond("Failed to create channel")

        await ctx.respond(
            embed=discord.Embed(
                title="Created Channel!",
                description=f"Created voice channel {channel.mention}",
                color=discord.Color.green(),
            )
        )

    @commands.slash_command()
    @default_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def delete_vc(
        self, ctx: discord.ApplicationContext, channel: discord.VoiceChannel
    ):
        try:
            await channel.delete()
        except discord.HTTPException:
            return await ctx.respond("Failed to delete the channel")

        await ctx.respond(
            embed=discord.Embed(
                title="Deleted Channel!",
                description=f"Deleted channel {channel.name}",
                color=discord.Color.green(),
            )
        )

    @commands.slash_command()
    @default_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lockdown(
        self, ctx: discord.ApplicationContext, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        em = discord.Embed(
            title="Lockdown",
            description=f"Channel ({channel.mention}) is now in lockdown",
            color=ctx.author.color,
        )
        return await ctx.respond(embed=em)

    @commands.slash_command()
    @default_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unlock(
        self, ctx: discord.ApplicationContext, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        em = discord.Embed(
            title="Unlocked",
            description=f"Channel ({channel.mention}) is now longer in lockdown",
            color=ctx.author.color,
        )
        return await ctx.respond(embed=em)

    @commands.slash_command()
    @default_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slowmode(
        self,
        ctx: discord.ApplicationContext,
        seconds: int = 5,
        channel: discord.TextChannel = None,
    ):
        if channel is None:
            channel = ctx.channel
        if seconds > (60 * 60) * 6:
            return await ctx.respond(
                embed=discord.Embed(
                    title="To long!",
                    description="Can't set slowmode to more than 6 hours",
                    color=discord.Color.red(),
                    ephemeral=True,
                )
            )
        elif seconds <= 0:
            await channel.edit(slowmode_delay=0)
            em = discord.Embed(
                title="Slowmode",
                description="Slowmode has been disabled",
                color=ctx.author.color,
            )
            return await ctx.respond(embed=em)

        await channel.edit(slowmode_delay=seconds)
        em = discord.Embed(
            title="Slowmode",
            description=(
                f"Slowmode has been set to {seconds} seconds for {channel.mention}"
            ),
            color=ctx.author.color,
        )
        return await ctx.respond(embed=em)

    @commands.slash_command()
    @default_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def remove_slowmode(
        self, ctx: discord.ApplicationContext, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = ctx.channel
        await channel.edit(slowmode_delay=0)
        em = discord.Embed(
            title="Slowmode",
            description=f"Slowmode has been disabled for {channel.mention}",
            color=ctx.author.color,
        )
        return await ctx.respond(embed=em)

    @commands.slash_command()
    @default_permissions(manage_channels=True)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def clear(self, ctx: discord.ApplicationContext, amount: int = 10):
        if amount < 50:
            await ctx.channel.purge(limit=amount + 1)
            em = discord.Embed(
                color=ctx.author.color,
                title="Channel Message Purge",
                description=f"Cleared {amount} messages from {ctx.channel.mention}",
            )
            return await ctx.respond(embed=em, ephemeral=True)

        em = discord.Embed(
            color=discord.Color.red(),
            title="To many messages!",
            description="Can't clear more than 50 messages at a time",
        )
        await ctx.respond(embed=em, ephemeral=True)

    @commands.slash_command()
    @default_permissions(manage_channels=True)
    @commands.has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def purgeuser(self, ctx: discord.ApplicationContext, member: discord.Member):
        check_func = lambda message: member == message.author
        tasks = [
            channel.purge(limit=1000, check=check_func)
            for channel in ctx.guild.text_channels
        ]

        asyncio.gather(*tasks)

        em = discord.Embed(
            color=ctx.author.color,
            title="Channel Message Purge",
            description=f"Purged messages from {member.mention}",
        )
        return await ctx.send(embed=em)


def setup(client):
    client.add_cog(Channels(client))
