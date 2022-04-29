import asyncio
import datetime

import discord
from discord.ext import commands

import log.log
from utils import blacklisted

class Channels(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def create_channel(self, ctx):
        pass


    @commands.command()
    async def delete_channel(self, ctx):
        pass


    @commands.command()
    async def create_vc(self, ctx):
        pass


    @commands.command()
    async def delete_vc(self, ctx):
        pass


    @commands.command()
    @commands.check(blacklisted)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lockdown(self, ctx, channel : discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        em = discord.Embed(
            title = "Lockdown",
            description = f"Channel ({channel.mention}) is now in lockdown",
            color = ctx.author.color,
            timestamp=datetime.datetime.now()
        )
        return await ctx.send(embed=em)


    @commands.command()
    @commands.check(blacklisted)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unlock(self, ctx, channel : discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        em = discord.Embed(
            title = "Unlocked",
            description = f"Channel ({channel.mention}) is now longer in lockdown",
            color = ctx.author.color,
            timestamp=datetime.datetime.now()
        )
        return await ctx.send(embed=em)


    @commands.command()
    @commands.check(blacklisted)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slowmode(self, ctx, seconds: int = 5):
        if seconds > (60*60)*6:
            return await ctx.send(embed=discord.Embed(
                title = "To long!",
                description = "Can't set slowmode to more than 6 hours",
                color = ctx.author.color,
                timestamp = datetime.datetime.now()
            ))
        elif seconds <= 0:
            await ctx.channel.edit(slowmode_delay=0)
            em = discord.Embed(
                title = "Slowmode",
                description = "Slowmode has been disabled",
                color = ctx.author.color,
                timestamp=datetime.datetime.now()
            )
            return await ctx.send(embed=em)

        await ctx.channel.edit(slowmode_delay=seconds)
        em = discord.Embed(
            title = "Slowmode",
            description = f"Slowmode has been set to {seconds} seconds",
            color = ctx.author.color,
            timestamp=datetime.datetime.now()
        )
        return await ctx.send(embed=em)


    @commands.command()
    @commands.check(blacklisted)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rslowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        em = discord.Embed(
            title = "Slowmode",
            description = "Slowmode has been disabled",
            color = ctx.author.color,
            timestamp=datetime.datetime.now()
        )
        return await ctx.send(embed=em)


    @commands.command()
    @commands.check(blacklisted)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def clear(self, ctx, amount: int = 10):
        if amount < 50:
            await ctx.channel.purge(limit=amount+1)
            em = discord.Embed(
                color = ctx.author.color,
                title = "Channel Message Purge",
                description = f"Cleared {amount} messages from {ctx.channel.mention}",
                timestamp = datetime.datetime.now()
            )
            return await ctx.send(embed=em)

        em = discord.Embed(
            color = ctx.author.color,
            title = "To many messages!",
            description = "Can't clear more than 50 messages at a time",
            timestamp = datetime.datetime.now()
        )
        await ctx.send(embed=em)


    @commands.command()
    @commands.check(blacklisted)
    @commands.has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def purgeuser(self, ctx, member:discord.Member):
        check_func = lambda message: member == message.author
        loop = asyncio.get_event_loop()
        for channel in ctx.guild.text_channels:
            loop.create_task(channel.purge(limit=1000, check=check_func))
        em = discord.Embed(
            color = ctx.author.color,
            title = "Channel Message Purge",
            description = f"Purged messages from {member.mention}",
            timestamp = datetime.datetime.now()
        )
        return await ctx.send(embed=em)

def setup(client):
    client.add_cog(Channels(client))