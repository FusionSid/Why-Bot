import re
import asyncio

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.helpers.why_leveling import (
    get_level_data,
    get_member_data,
    xp_needed,
    update_member_data,
    get_all_member_data,
)
from core.models import WhyBot
from core.helpers.checks import run_bot_checks
from core.db.setup_guild import setup_leveling_guild


RATE = 1
PER = 60


class Leveling(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.guild_cooldowns: dict[int, commands.CooldownMapping] = {}
        self.cog_check = run_bot_checks

    leveling = SlashCommandGroup("leveling", "Leveling system related commands")

    async def is_member_cooldown(self, message: discord.Message):
        bucket = self.guild_cooldowns[message.guild.id].get_bucket(message)
        cooldown = bucket.update_rate_limit()

        if cooldown is None:
            return False

        return True

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None or message.author.bot:
            return

        if self.guild_cooldowns.get(message.guild.id) is None:
            self.guild_cooldowns[
                message.guild.id
            ] = commands.CooldownMapping.from_cooldown(
                RATE, PER, commands.BucketType.user
            )

        on_cooldown = await self.is_member_cooldown(message)
        if on_cooldown is True:
            return

        leveling_data = await get_level_data(self.client.db, message.guild.id)
        if leveling_data is None:
            return await setup_leveling_guild(self.client.db, message.guild.id)

        if (
            leveling_data.plugin_enabled is False
            or message.channel.id in leveling_data.no_xp_channels
            or bool(
                set(leveling_data.no_xp_roles)
                & {role.id for role in message.author.roles}
            )
        ):
            return

        member_data = await get_member_data(
            self.client.db, message.author, message.guild.id
        )

        give_xp_amount = leveling_data.get_per_minute_xp()
        member_data.member_total_xp += give_xp_amount

        next_level_xp = await xp_needed(member_data.member_level + 1)
        add_level, current_xp = divmod(member_data.member_total_xp, next_level_xp)

        if not add_level:
            current_xp -= await xp_needed(member_data.member_level)

        member_data.member_level += add_level
        member_data.member_xp = current_xp

        await update_member_data(self.client.db, message, member_data)

        # Handle level up message:
        if add_level:
            # if its disabled
            if not leveling_data.level_up_enabled:
                return
            levelup_message = leveling_data.level_up_text
            member = message.author
            replace_cases = {
                "{member.name}": member.name,
                "{member.displayname}": member.display_name,
                "{member.mention}": member.mention,
                "{server.name}": message.guild.name,
                "{level.old}": member_data.member_level - add_level,
                "{level}": member_data.member_level,
            }
            for code, replace_to in replace_cases.items():
                levelup_message = levelup_message.replace(code, str(replace_to))

            def check(reaction: discord.reaction.Reaction, user):
                return (
                    reaction.message.id == msg.id
                    and reaction.emoji == "🗑️"
                    and user.id == message.author.id
                )

            try:
                msg = await message.reply(
                    embed=discord.Embed(
                        title=member.display_name,
                        description=levelup_message,
                        color=discord.Color.green(),
                    )
                )
                try:
                    await msg.add_reaction("🗑️")
                    await self.client.wait_for(
                        "reaction_add", timeout=15.0, check=check
                    )
                    await msg.delete()
                except asyncio.TimeoutError:
                    await msg.remove_reaction("🗑️", member=self.client.user)
            except (discord.Forbidden, discord.HTTPException):
                pass  # message failed to send (probably due to perms)

    @leveling.command(description="Toggle the leveling system")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def toggle_leveling(
        self,
        ctx: discord.ApplicationContext,
    ):
        leveling_data = await get_level_data(self.client.db, ctx.guild.id)
        if leveling_data is None:
            return await setup_leveling_guild(self.client.db, ctx.guild.id)

        on_or_off = not leveling_data.plugin_enabled

        await self.client.db.execute(
            "UPDATE leveling_guild SET plugin_enabled=$1 WHERE guild_id=$2",
            on_or_off,
            ctx.guild.id,
        )

        await ctx.respond(
            embed=discord.Embed(
                title="Leveling Toggled!",
                description=(
                    f"Leveling system is now {'on ✅' if on_or_off else 'off ❌'}\nIf you"
                    f" wish to toggle it back {'off' if on_or_off else 'on'} run this"
                    " command again"
                ),
                color=discord.Color.green(),
            )
        )

    @leveling.command(
        description="Calculate the amount of xp you need to reach a certain level"
    )
    @commands.guild_only()
    async def xp_needed(self, ctx: discord.ApplicationContext, level: int = None):
        member_data = await get_member_data(self.client.db, ctx.author, ctx.guild.id)
        if level is None:
            next_level = member_data.member_level + 1
            next_level_xp = await xp_needed(next_level)
            return await ctx.respond(
                embed=discord.Embed(
                    title="XP Calculator",
                    description=f"Amount of XP required for level {next_level} = {next_level_xp}\nAmount of XP"
                    f" you need to get to reach level {next_level} = {next_level_xp - member_data.member_total_xp}",
                    color=discord.Color.random(),
                )
            )

        level_xp = await xp_needed(level)
        return await ctx.respond(
            embed=discord.Embed(
                title="XP Calculator",
                description=f"Amount of XP required for level {level} = {level_xp}\nAmount of "
                f"XP you need to get to reach level {level_xp} = {level_xp - member_data.member_total_xp}",
                color=discord.Color.random(),
            )
        )

    @leveling.command(description="Toggle the level up message from being sent")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def toggle_level_up(
        self,
        ctx: discord.ApplicationContext,
    ):
        leveling_data = await get_level_data(self.client.db, ctx.guild.id)
        if leveling_data is None:
            return await setup_leveling_guild(self.client.db, ctx.guild.id)

        on_or_off = not leveling_data.level_up_enabled

        await self.client.db.execute(
            "UPDATE leveling_guild SET level_up_enabled=$1 WHERE guild_id=$2",
            on_or_off,
            ctx.guild.id,
        )

        await ctx.respond(
            embed=discord.Embed(
                title="Level Up Message Toggled!",
                description=(
                    "Level Up Message system is now"
                    f" {'on ✅' if on_or_off else 'off ❌'}\nIf you wish to toggle it"
                    f" back {'off' if on_or_off else 'on'} run this command again"
                ),
                color=discord.Color.green(),
            )
        )

    @leveling.command(description="Set the amount of xp given for leveling")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def set_xp(
        self,
        ctx: discord.ApplicationContext,
        xp: discord.Option(
            str,
            description="XP given per minute. Type a number like '5' or a range like '15-30'",
        ),
    ):
        if not re.match("[0-9-]", xp):
            return await ctx.respond("Invalid Input!")

        if xp.isnumeric():
            await self.client.db.execute(
                "UPDATE leveling_guild SET per_minute=$1 WHERE guild_id=$2",
                xp,
                ctx.guild.id,
            )
            return await ctx.respond(
                embed=discord.Embed(
                    title="Per minute XP updated!",
                    description=f"Per minute xp set to: {xp}",
                    color=discord.Color.random(),
                )
            )

        split_range = xp.split("-")

        if (
            len(split_range) == 2
            and split_range[0].isnumeric()
            and split_range[1].isnumeric()
        ):
            await self.client.db.execute(
                "UPDATE leveling_guild SET per_minute=$1 WHERE guild_id=$2",
                xp,
                ctx.guild.id,
            )
            return await ctx.respond(
                embed=discord.Embed(
                    title="Per minute XP updated!",
                    description=f"Per minute xp set to a range from {split_range[0]} to {split_range[1]}",
                    color=discord.Color.random(),
                )
            )
        return await ctx.respond("Invalid Input!")

    @leveling.command(description="Set the text displayed when a user levels up")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def set_level_text(
        self,
        ctx: discord.ApplicationContext,
        text: discord.Option(
            str, "The text you want to be sent when a user levels up"
        ) = None,
    ):
        if text is None:
            options = [
                "{member.name}",
                "{member.displayname}",
                "{member.mention}",
                "{server.name}",
                "{level.old}",
                "{level}",
            ]
            embed = discord.Embed(
                title="Level up text help page",
                description=(
                    "The message you set with this command will be shown when a user"
                    " levels up.\nYou can also set placeholder                    "
                    " codes in this text which will be replaced with the relevant"
                    " information later"
                ),
                color=discord.Color.green(),
            )
            embed.add_field(name="Options:", value="\n".join(options), inline=False)
            embed.add_field(
                name="Example:",
                value="GG {member.name}, you just reached level \\**{level}**!",
                inline=False,
            )
            return await ctx.respond(embed=embed)

        await self.client.db.execute(
            "UPDATE leveling_guild SET level_up_text=$1 WHERE guild_id=$2",
            text,
            ctx.guild.id,
        )

        await ctx.respond(
            embed=discord.Embed(
                title="Level up text set!",
                description=f"Text set to:\n{text}",
                color=discord.Color.green(),
            )
        )

    @leveling.command(description="Show your rank for leveling")
    @commands.guild_only()
    async def rank(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        data = await get_all_member_data(self.client.db, ctx.guild.id)
        for _idx, _member in enumerate(data):
            if _member[1] == ctx.author.id:
                member = _member
                idx = _idx
                break
        else:
            return await ctx.respond(
                "You were not found in the database\nMaybe send some messages or check"
                " if counting is enabled"
            )

        current_level_xp = await xp_needed(member[4])
        next_level_xp = await xp_needed(member[4] + 1)

        await ctx.respond(
            embed=discord.Embed(
                title=f"{ctx.author.display_name} - Rank #{idx+1}",
                description=(
                    f"Level: {member[4]}. XP: {member[3]}/{next_level_xp-current_level_xp}. Total XP:"
                    f" {member[5]}\n\n**This embed is a placeholder for an image card**"
                ),
            )
        )

    @leveling.command(description="Show the leveling leaderboard for the server")
    @commands.guild_only()
    async def leaderboard(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        data = await get_all_member_data(self.client.db, ctx.guild.id)
        embed = discord.Embed(
            title="Leaderboard",
            description="**This embed is a placeholder for an image lb coming soon**",
        )
        for rank, member in enumerate(data[:10]):
            current_level_xp = await xp_needed(member[4])
            next_level_xp = await xp_needed(member[4] + 1)

            embed.add_field(
                name=f"{member[2]} - Rank #{rank+1}",
                value=(
                    f"Level: {member[4]}. XP: {member[3]}/{next_level_xp-current_level_xp}. Total XP:"
                    f" {member[5]}"
                ),
                inline=False,
            )
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Leveling(client))
