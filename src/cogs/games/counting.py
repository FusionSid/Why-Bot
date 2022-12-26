import json
import asyncio

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, default_permissions

from core import BaseCog
from core.models import CountingData
from core.db import setup_counting
from core.utils import slow_safe_calculate


class Counting(BaseCog):

    counting = SlashCommandGroup("counting", "Commmands related to the counting game")

    @counting.command(description="Set the channel for the counting game")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def setchannel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(
            discord.TextChannel, "The counting channel", required=True  # noqa
        ),
    ):
        counting_data = await self.__get_counting_data(ctx.guild.id, skip_cache=True)
        if counting_data is None:
            return await setup_counting(self.client.db, ctx.guild.id)

        await self.client.db.execute(
            "UPDATE counting SET counting_channel=$1 WHERE guild_id=$2",
            channel.id,
            ctx.guild.id,
        )
        await ctx.respond(
            embed=discord.Embed(
                title="Counting Channel Set!",
                description=f"Counting channel is now: {channel.mention}",
                color=ctx.author.color,
            )
        )

        counting_data.counting_channel = channel.id
        await self.__update_cache(counting_data)

    @counting.command(description="Enable the counting game for this server")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def enable(
        self,
        ctx: discord.ApplicationContext,
    ):
        counting_data = await self.__get_counting_data(ctx.guild.id, skip_cache=True)
        if counting_data is None:
            return await setup_counting(self.client.db, ctx.guild.id)
        elif counting_data.counting_channel is None:
            return await ctx.respond(
                embed=discord.Embed(
                    title="Counting channel not set",
                    description=(
                        "Please set the counting channel first before enabling the"
                        " game.\nUse `/counting setchannel` to set it"
                    ),
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )

        try:
            channel = await self.client.fetch_channel(counting_data.counting_channel)
        except (
            discord.NotFound,
            discord.HTTPException,
            discord.ApplicationCommandInvokeError,
        ):
            return await ctx.respond(
                embed=discord.Embed(
                    title="Something went wrong fetching the channel",
                    description=(
                        "Most likely because the counting channel set was"
                        " deleted.\nReset it with `/counting setchannel`"
                    ),
                    color=ctx.author.color,
                ),
                ephemeral=True,
            )

        await self.client.db.execute(
            "UPDATE counting SET plugin_enabled=true WHERE guild_id=$1",
            ctx.guild.id,
        )

        await ctx.respond(
            embed=discord.Embed(
                title="Counting Enabled!",
                description=(
                    f"Counting game is now enabled and the channel is {channel.mention}"
                ),
                color=ctx.author.color,
            )
        )

        counting_data.plugin_enabled = True
        await self.__update_cache(counting_data)

    @counting.command(description="Toggle the bot auto evaluating math expressions")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def toggle_auto_calc(
        self,
        ctx: discord.ApplicationContext,
    ):
        counting_data = await self.__get_counting_data(ctx.guild.id, skip_cache=True)
        if counting_data is None:
            return await setup_counting(self.client.db, ctx.guild.id)

        on_or_off = not counting_data.auto_calculate

        await self.client.db.execute(
            "UPDATE counting SET auto_calculate=$1 WHERE guild_id=$2",
            on_or_off,
            ctx.guild.id,
        )

        await ctx.respond(
            embed=discord.Embed(
                title="Auto calculate toggled!",
                description=(
                    f"Auto calculate is now {'on ✅' if on_or_off else 'off ❌'}\nIf you"
                    f" wish to toggle it back {'off' if on_or_off else 'on'} run this"
                    " command again"
                ),
                color=ctx.author.color,
            )
        )

        counting_data.auto_calculate = on_or_off
        await self.__update_cache(counting_data)

    @counting.command(description="Disable counting")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def disable(
        self,
        ctx: discord.ApplicationContext,
    ):
        counting_data = await self.__get_counting_data(ctx.guild.id, skip_cache=True)
        if counting_data is None:
            return await setup_counting(self.client.db, ctx.guild.id)

        await self.client.db.execute(
            "UPDATE counting SET plugin_enabled=false WHERE guild_id=$1",
            ctx.guild.id,
        )

        await ctx.respond(
            embed=discord.Embed(
                title="Counting Disabled!",
                description=(
                    "Counting is now disabled, If you ever want to re-enable it use"
                    " `/counting enable`"
                ),
                color=ctx.author.color,
            )
        )

        counting_data.plugin_enabled = False
        await self.__update_cache(counting_data)

    @counting.command(description="Show the current number")
    @commands.guild_only()
    async def current_number(self, ctx: discord.ApplicationContext):
        counting_data = await self.__get_counting_data(ctx.guild.id, skip_cache=True)
        if counting_data is None:
            await setup_counting(self.client.db, ctx.guild.id)
        elif (
            counting_data.counting_channel is None
            or counting_data.plugin_enabled is None
            or counting_data.plugin_enabled is False
        ):
            return await ctx.respond(
                embed=discord.Embed(
                    title="Counting not setup/enabled on this server",
                    description=(
                        "Use commands `/counting setchannel` and `/counting enable` to"
                        " setup counting on this server"
                    ),
                    color=ctx.author.color,
                )
            )

        await ctx.respond(
            embed=discord.Embed(
                title=f"Current number is: {counting_data.current_number}",
                description=(
                    "That means the next number / the one you should type is:"
                    f" {counting_data.next_number}"
                ),
                color=ctx.author.color,
            )
        )

        await self.__update_cache(counting_data)

    @counting.command(description="Show the highest number this server has reached")
    @commands.guild_only()
    async def high_score(self, ctx: discord.ApplicationContext):
        counting_data = await self.__get_counting_data(ctx.guild.id, skip_cache=True)
        if counting_data is None:
            await setup_counting(self.client.db, ctx.guild.id)
        elif (
            counting_data.counting_channel is None
            or counting_data.plugin_enabled is None
            or counting_data.plugin_enabled is False
        ):
            return await ctx.respond(
                embed=discord.Embed(
                    title="Counting not setup/enabled on this server",
                    description=(
                        "Use commands `/counting setchannel` and `/counting enable` to"
                        " setup counting on this server"
                    ),
                    color=ctx.author.color,
                )
            )

        await ctx.respond(
            embed=discord.Embed(
                title=f"Current high score is: {counting_data.high_score}",
                description=(
                    "Use `/counting leaderboard` to see your position across all why"
                    " bot servers"
                ),
                color=ctx.author.color,
            )
        )

        await self.__update_cache(counting_data)

    @counting.command(description="Show the global leaderboard for counting")
    @commands.guild_only()
    async def leaderboard(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        counting_data = await self.client.db.fetch(
            "SELECT * FROM counting ORDER BY high_score"
        )
        counting_data = reversed(counting_data[:10])  # crop to 10 guilds only

        embed = discord.Embed(title="Counting Leaderboard", color=ctx.author.color)

        place = 1
        for guild in counting_data:
            try:
                guild_name = await self.client.fetch_guild(guild[0])
            except (
                discord.NotFound,
                discord.HTTPException,
                discord.ApplicationCommandInvokeError,
            ):
                continue

            embed.add_field(
                name=f"{place}: {guild_name}",
                value=f"Counting high score: {guild[4]}",
                inline=False,
            )

            place += 1

        await ctx.respond(embed=embed)

    @counting.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def ban_user(self, ctx: discord.ApplicationContext, member: discord.Member):
        counting_data = await self.__get_counting_data(ctx.guild.id, skip_cache=True)
        if member.id in counting_data.banned_counters:
            return await ctx.respond("User is already banned from counting")
        await self.client.db.execute(
            "UPDATE counting SET banned_users = array_append(banned_users, $1) WHERE guild_id=$2",
            member.id,
            ctx.guild.id,
        )
        await ctx.respond(
            embed=discord.Embed(
                title="User Banned",
                description=f"{member.mention} is banned from counting",
                color=discord.Color.random(),
            )
        )
        counting_data.banned_counters.append(member.id)
        await self.__update_cache(counting_data)

    @counting.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def unban_user(self, ctx: discord.ApplicationContext, member: discord.Member):
        counting_data = await self.__get_counting_data(ctx.guild.id, skip_cache=True)
        if member.id not in counting_data.banned_counters:
            return await ctx.respond("User is already unbanned from counting")
        await self.client.db.execute(
            "UPDATE counting SET banned_users = array_remove(banned_users, $1) WHERE guild_id=$2",
            member.id,
            ctx.guild.id,
        )
        await ctx.respond(
            embed=discord.Embed(
                title="User Unbanned",
                description=f"{member.mention} is no longer banned from counting",
                color=discord.Color.random(),
            )
        )
        counting_data.banned_counters.remove(member.id)
        await self.__update_cache(counting_data)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author.bot:
            return

        counting_data = await self.__get_counting_data(message.guild.id)
        if counting_data is None:
            return await setup_counting(self.client.db, message.guild.id)

        if (
            counting_data.plugin_enabled is None
            or counting_data.counting_channel == 0
            or counting_data.counting_channel is None
        ):
            return

        potential_number = await slow_safe_calculate(message.content, only_int=True)
        if potential_number is None:
            return

        if counting_data.auto_calculate and not message.content.isnumeric():
            self.client.loop.create_task(self.__delete_msg(potential_number, message))

        if (
            counting_data.counting_channel != message.channel.id
            or counting_data.plugin_enabled is False
        ):
            return

        if message.author.id in counting_data.banned_counters:
            return

        if potential_number != counting_data.next_number:
            em = discord.Embed(
                title=f"{message.author.display_name}, You ruined it!",
                description=(
                    f"You were supposed to type `{counting_data.next_number}`\nCount"
                    " reset to zero"
                ),
                color=message.author.color,
            )
            await self.__reset_count(counting_data)
            await message.add_reaction("❌")
            return await message.channel.send(embed=em)

        elif counting_data.last_counter == message.author.id:
            em = discord.Embed(
                title=f"{message.author.display_name}, You ruined it!",
                description=(
                    "You fool, only one person can count a time and since you did"
                    f" {counting_data.current_number} you cant do"
                    f" {counting_data.next_number}\nCount reset to zero"
                ),
                color=message.author.color,
            )
            await self.__reset_count(counting_data)
            await message.add_reaction("❌")
            return await message.channel.send(embed=em)

        await self.__update_count(counting_data, message)
        await message.add_reaction("✅")

        match counting_data.current_number:
            case 42:
                self.client.loop.create_task(
                    self.__delete_msg("You have reached the meaning of life", message)
                )
            case 69:
                self.client.loop.create_task(self.__delete_msg("Nice", message))
            case 100:
                await message.add_reaction("💯")
            case 420:
                await message.add_reaction(self.client.get_emoji(1053461527161741373))
            case 9001:
                self.client.loop.create_task(
                    self.__delete_msg("You're over 9000", message)
                )

    async def __reset_count(self, data: CountingData):
        data.last_counter = 0
        data.current_number = 0

        await self.__update_cache(data)

        self.client.loop.create_task(
            self.client.db.execute(
                "UPDATE counting SET current_number=$1, last_counter=$2 WHERE"
                " guild_id=$3",
                0,
                0,
                data.guild_id,
            )
        )

    async def __update_count(self, data: CountingData, message: discord.Message):
        # update count and last counter and highscore
        data.current_number = data.next_number
        data.last_counter = message.author.id

        await self.__update_cache(data)
        self.client.loop.create_task(
            self.client.db.execute(
                "UPDATE counting SET current_number=$1, last_counter=$2 WHERE"
                " guild_id=$3",
                data.current_number,
                data.last_counter,
                data.guild_id,
            )
        )
        self.client.loop.create_task(self.__update_high_score(data, message))

    async def __update_high_score(self, data: CountingData, message: discord.Message):
        if data.high_score is None or data.current_number > data.high_score:
            await self.client.db.execute(
                "UPDATE counting SET high_score=$1 WHERE guild_id=$2",
                data.current_number,
                data.guild_id,
            )

    async def __update_cache(self, data: CountingData):
        await self.client.redis.set(
            f"{data.guild_id}_counting", json.dumps(list(data.__dict__.values()))
        )

    async def __get_counting_data(
        self, guild_id: int, skip_cache: bool = False
    ) -> CountingData:
        key = f"{guild_id}_counting"

        if not skip_cache:
            if await self.client.redis.exists(key):
                data = json.loads(await self.client.redis.get(key))
                return CountingData(*data)

        data = await self.client.db.fetch(
            "SELECT * FROM counting WHERE guild_id=$1", guild_id
        )

        if not data:
            return None

        await self.client.redis.set(key, json.dumps(list(data[0])))
        return CountingData(*data[0])

    async def __delete_msg(self, message_content: int | str, message: discord.Message):
        try:
            msg = await message.reply(message_content)
        except discord.Forbidden:
            return

        def check(reaction: discord.reaction.Reaction, user: discord.User):
            return (
                reaction.message.id == msg.id
                and reaction.emoji == "🗑️"
                and user.id == message.author.id
            )

        try:
            await msg.add_reaction("🗑️")
            await self.client.wait_for("reaction_add", timeout=15.0, check=check)
            await msg.delete()
        except asyncio.TimeoutError:
            await msg.remove_reaction("🗑️", member=self.client.user)


def setup(client):
    client.add_cog(Counting(client))
