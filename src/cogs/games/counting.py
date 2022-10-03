import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.utils.calc import calculate
from core.models.client import WhyBot
from core.models.counting import CountingData
from core.db.setup_guild import setup_counting
from core.helpers.checks import run_bot_checks


class Counting(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    counting = SlashCommandGroup("counting", "Commmands related to the counting game")

    async def get_counting_data(self, guild_id: int):
        data = await self.client.db.fetch(
            "SELECT * FROM counting WHERE guild_id=$1", guild_id
        )
        if not len(data):
            return None

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
        counting_data = await self.get_counting_data(ctx.guild.id)
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

    @counting.command()
    @commands.guild_only()
    @commands.check(run_bot_checks)
    @commands.has_guild_permissions(administrator=True)
    async def enable(
        self,
        ctx,
    ):
        counting_data = await self.get_counting_data(ctx.guild.id)
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

    @counting.command()
    @commands.guild_only()
    @commands.check(run_bot_checks)
    async def current_number(self, ctx):
        counting_data = await self.get_counting_data(ctx.guild.id)
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

        return await ctx.respond(
            embed=discord.Embed(
                title=f"Current number is: {counting_data.current_number}",
                description=f"That means the next number / the one you should type is: {counting_data.next_number}",
                color=ctx.author.color,
            )
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # TODO implement caching here

        if message.guild is None or message.author.bot:
            return

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
            await self.reset_count(message.guild.id)
            await message.add_reaction("❌")
            return await message.channel.send(embed=em)

        elif counting_data.last_counter == message.author.id:
            em = discord.Embed(
                title=f"{message.author.name}, You ruined it!",
                description=f"You fool, only one person can count a time and since you did {counting_data.current_number} you cant do {counting_data.next_number}\nCount reset to zero",
                color=message.author.color,
            )
            await self.reset_count(message.guild.id)
            await message.add_reaction("❌")
            return await message.channel.send(embed=em)

        # update count and last counter and highscore
        await self.update_count(message.guild.id, message.author.id)
        await message.add_reaction("✅")

    async def reset_count(self, guild_id: int):
        await self.client.db.execute(
            "UPDATE counting SET current_number=$1, last_counter=$2 WHERE guild_id=$3",
            0,
            0,
            guild_id,
        )

    async def update_count(self, guild_id: int, last_counter: int):
        await self.client.db.execute(
            "UPDATE counting SET current_number=current_number + 1, last_counter=$1 WHERE guild_id=$2",
            last_counter,
            guild_id,
        )


def setup(client):
    client.add_cog(Counting(client))


# "guild_id, last_counter, current_number, counting_channel, high_score, plugin_enabled, auto_calculate"
