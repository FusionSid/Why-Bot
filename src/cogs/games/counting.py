import time
import json
import asyncio

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.utils.calc import calculate
from core.models import WhyBot
from core.models.counting import CountingData
from core.db.setup_guild import setup_counting
from core.helpers.checks import run_bot_checks


class Counting(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.guilds: list[int] = []

    counting = SlashCommandGroup("counting", "Commmands related to the counting game")

    async def put_on_cooldown(self, guild):
        self.guilds.append(guild)
        await asyncio.sleep(0.5)

        try:
            self.guilds.remove(guild)
        except ValueError:
            return

    async def get_counting_data(
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

        if not len(data):
            return None

        await self.client.redis.set(key, json.dumps(list(data[0])))
        return CountingData(*data[0])

    @counting.command()
    @commands.guild_only()
    @commands.check(run_bot_checks)
    @commands.has_guild_permissions(administrator=True)
    async def setchannel(
        self,
        ctx,
        channel: discord.Option(
            discord.TextChannel, "The counting channel", required=True
        ),
    ):
        counting_data = await self.get_counting_data(ctx.guild.id, skip_cache=True)
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
        await self.update_cache(counting_data)

    @counting.command()
    @commands.guild_only()
    @commands.check(run_bot_checks)
    @commands.has_guild_permissions(administrator=True)
    async def enable(
        self,
        ctx,
    ):
        counting_data = await self.get_counting_data(ctx.guild.id, skip_cache=True)
        if counting_data is None:
            return await setup_counting(self.client.db, ctx.guild.id)
        elif counting_data.counting_channel is None:
            return await ctx.respond(
                embed=discord.Embed(
                    title="Counting channel not set",
                    description="Please set the counting channel first before enabling the game.\nUse `/counting setchannel` to set it",
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
                    description="Most likely because the counting channel set was deleted.\nReset it with `/counting setchannel`",
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
                description=f"Counting game is now enabled and the channel is {channel.mention}",
                color=ctx.author.color,
            )
        )

        counting_data.plugin_enabled = True
        await self.update_cache(counting_data)

    @counting.command()
    @commands.guild_only()
    @commands.check(run_bot_checks)
    @commands.has_guild_permissions(administrator=True)
    async def disable(
        self,
        ctx,
    ):
        counting_data = await self.get_counting_data(ctx.guild.id, skip_cache=True)
        if counting_data is None:
            return await setup_counting(self.client.db, ctx.guild.id)

        await self.client.db.execute(
            "UPDATE counting SET plugin_enabled=false WHERE guild_id=$1",
            ctx.guild.id,
        )

        await ctx.respond(
            embed=discord.Embed(
                title="Counting Disabled!",
                description=f"Counting is now disabled, If you ever want to re-enable it use `/counting enable`",
                color=ctx.author.color,
            )
        )

        counting_data.plugin_enabled = False
        await self.update_cache(counting_data)

    @counting.command()
    @commands.guild_only()
    @commands.check(run_bot_checks)
    async def current_number(self, ctx):
        counting_data = await self.get_counting_data(ctx.guild.id, skip_cache=True)
        if counting_data is None:
            await setup_counting(self.client.db, ctx.guild.id)
        elif (
            counting_data.counting_channel is None
            or counting_data.plugin_enabled is None
            or counting_data.plugin_enabled == False
        ):
            return await ctx.respond(
                embed=discord.Embed(
                    title="Counting not setup/enabled on this server",
                    description="Use commands `/counting setchannel` and `/counting enable` to setup counting on this server",
                    color=ctx.author.color,
                )
            )

        await ctx.respond(
            embed=discord.Embed(
                title=f"Current number is: {counting_data.current_number}",
                description=f"That means the next number / the one you should type is: {counting_data.next_number}",
                color=ctx.author.color,
            )
        )

        await self.update_cache(counting_data)

    @counting.command()
    @commands.guild_only()
    @commands.check(run_bot_checks)
    async def high_score(self, ctx):
        counting_data = await self.get_counting_data(ctx.guild.id, skip_cache=True)
        if counting_data is None:
            await setup_counting(self.client.db, ctx.guild.id)
        elif (
            counting_data.counting_channel is None
            or counting_data.plugin_enabled is None
            or counting_data.plugin_enabled == False
        ):
            return await ctx.respond(
                embed=discord.Embed(
                    title="Counting not setup/enabled on this server",
                    description="Use commands `/counting setchannel` and `/counting enable` to setup counting on this server",
                    color=ctx.author.color,
                )
            )

        await ctx.respond(
            embed=discord.Embed(
                title=f"Current high score is: {counting_data.high_score}",
                description=f"Use `/counting leaderboard` to see your position across all why bot servers",
                color=ctx.author.color,
            )
        )

        await self.update_cache(counting_data)

    @counting.command()
    @commands.guild_only()
    @commands.check(run_bot_checks)
    async def leaderboard(self, ctx):
        await ctx.defer()
        counting_data = await self.client.db.fetch(
            "SELECT * FROM counting ORDER BY high_score"
        )
        counting_data = counting_data[:10]  # crop to 10 guilds only

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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author.bot:
            return

        if message.guild.id in self.guilds:
            try:
                await message.add_reaction("🇸")
                await message.add_reaction("🇵")
                await message.add_reaction("🇦")
                await message.add_reaction("🇲")
                return await message.add_reaction("🛑")
            except (discord.NotFound, discord.Forbidden):
                pass  # probably deleted their message

        counting_data = await self.get_counting_data(message.guild.id)
        if counting_data is None:
            return await setup_counting(self.client.db, message.guild.id)

        if (
            counting_data.plugin_enabled == False
            or counting_data.plugin_enabled is None
            or counting_data.counting_channel == 0
            or counting_data.counting_channel is None
            or counting_data.counting_channel != message.channel.id
        ):
            return

        potential_number = await calculate(message.content, only_int=True)
        if potential_number is None:
            return

        if potential_number != counting_data.next_number:
            em = discord.Embed(
                title=f"{message.author.name}, You ruined it!",
                description=f"You were supposed to type `{counting_data.next_number}`\nCount reset to zero",
                color=message.author.color,
            )
            await self.reset_count(counting_data)
            await message.add_reaction("❌")
            return await message.channel.send(embed=em)

        elif counting_data.last_counter == message.author.id:
            em = discord.Embed(
                title=f"{message.author.name}, You ruined it!",
                description=f"You fool, only one person can count a time and since you did {counting_data.current_number} you cant do {counting_data.next_number}\nCount reset to zero",
                color=message.author.color,
            )
            await self.reset_count(counting_data)
            await message.add_reaction("❌")
            return await message.channel.send(embed=em)

        await self.update_count(counting_data, message.author.id)
        await self.put_on_cooldown(message.guild.id)
        await message.add_reaction("✅")

    async def reset_count(self, data: CountingData):
        data.last_counter = 0
        data.current_number = 0

        await self.update_cache(data)

        self.client.loop.create_task(
            self.client.db.execute(
                "UPDATE counting SET current_number=$1, last_counter=$2 WHERE guild_id=$3",
                0,
                0,
                data.guild_id,
            )
        )

    async def update_count(self, data: CountingData, last_counter: int):
        # update count and last counter and highscore
        data.current_number = data.next_number
        data.last_counter = last_counter

        await self.update_cache(data)
        self.client.loop.create_task(
            self.client.db.execute(
                "UPDATE counting SET current_number=$1, last_counter=$2 WHERE guild_id=$3",
                data.current_number,
                data.last_counter,
                data.guild_id,
            )
        )
        self.client.loop.create_task(self.update_high_score(data))

    async def update_high_score(self, data: CountingData):
        if data.high_score is None or data.current_number > data.high_score:
            await self.client.db.execute(
                "UPDATE counting SET high_score=$1 WHERE guild_id=$2",
                data.current_number,
                data.guild_id,
            )

    async def update_cache(self, data: CountingData):
        await self.client.redis.set(
            f"{data.guild_id}_counting", json.dumps(list(data.__dict__.values()))
        )


def setup(client):
    client.add_cog(Counting(client))
