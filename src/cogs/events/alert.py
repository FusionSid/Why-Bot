import datetime

import discord
from discord.ext import commands

from core.models.client import WhyBot
from core.helpers.checks import run_bot_checks
from core.utils.formatters import discord_timestamp


class Alerts(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    async def setup_settings(self, member_id: int, db):
        return await db.execute(
            "INSERT INTO alerts_users (user_id) VALUES ($1)", member_id
        )

    @commands.Cog.listener()
    async def on_application_command_completion(self, ctx: discord.ApplicationContext):
        data = await self.client.db.fetch(
            "SELECT * FROM alerts_users WHERE user_id=$1", ctx.author.id
        )
        if not len(data):
            await self.setup_settings(ctx.author.id, self.client.db)
            data = [[ctx.author.id, False, False]]
        data = data[0]

        # data[1] if if they have already seen the alert
        # data[2] is if they have alert notifications toggled on
        if data[1] or data[2]:
            return

        em = discord.Embed(
            title="New Alert",
            description="You have a new alert from the devs\nUse </alert:0> to check it out\nUse </togglealerts:0> to not show these types of messages",
            color=discord.Color.random(),
        )

        try:  # try to send the message
            await ctx.followup.send(embed=em, ephemeral=True)
        except discord.HTTPException:  # frik it failed, probably perms or smth like that
            return

    @commands.slash_command()
    async def alert(self, ctx: discord.ApplicationContext):
        data = await self.client.db.fetch("SELECT * FROM alerts ORDER BY id")
        data = data[::-1][0]

        description = data[2]
        date = datetime.datetime(
            year=data[3].year, month=data[3].month, day=data[3].day
        )
        date = await discord_timestamp(int(date.timestamp()), format_type="ts")
        description += f"\n\nThis alert was made {date}"

        em = discord.Embed(
            title=data[1], description=description, color=discord.Color.random()
        )

        em.set_footer(text=f"This alert was viewed {data[4]} times")

        await ctx.respond(embed=em)

        await self.client.db.execute(
            "UPDATE alerts_users SET alert_viewed=true WHERE user_id=$1", ctx.author.id
        )
        await self.client.db.execute(
            "UPDATE alerts SET viewed=$1 WHERE id=$2", (data[4] + 1), data[0]
        )

    @commands.slash_command()
    async def togglealerts(self, ctx: discord.ApplicationContext):
        data = await self.client.db.fetch(
            "SELECT * FROM alerts_users WHERE user_id=$1", ctx.author.id
        )
        if not len(data):
            await self.setup_settings(ctx.author.id, self.client.db)
            data = [[ctx.author.id, False, False]]
        data = data[0]

        on_or_off = not data[2]

        await self.client.db.execute(
            "UPDATE alerts_users SET ignore_alerts=$1 WHERE user_id=$2",
            on_or_off,
            ctx.guild.id,
        )

        await ctx.respond(
            embed=discord.Embed(
                title="Alerts Toggled!",
                description=(
                    f"Alert notifications is now {'on ✅' if on_or_off else 'off ❌'}\nIf you"
                    f" wish to toggle it back {'off' if on_or_off else 'on'} run this"
                    " command again"
                ),
                color=discord.Color.green() if on_or_off else discord.Color.red(),
            )
        )


def setup(client):
    client.add_cog(Alerts(client))
