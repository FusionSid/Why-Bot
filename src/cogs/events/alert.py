import time

import discord
from discord.ext import commands

from core.models.client import WhyBot
from core.helpers.checks import run_bot_checks
from core.helpers.views import InputModalView
from core.utils.formatters import discord_timestamp
from core.utils.client_functions import GUILD_IDS


class Alerts(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    async def __setup_settings(self, member_id: int):
        return await self.client.db.execute(
            "INSERT INTO alerts_users (user_id) VALUES ($1)", member_id
        )

    @commands.Cog.listener()
    async def on_application_command_completion(self, ctx: discord.ApplicationContext):
        data = await self.client.db.fetch(
            "SELECT * FROM alerts_users WHERE user_id=$1", ctx.author.id
        )
        if not data:
            await self.__setup_settings(ctx.author.id)
            data = [[ctx.author.id, False, False]]
        data = data[0]

        # data[1] if if they have already seen the alert
        # data[2] is if they have alert notifications toggled on
        if data[1] or data[2]:
            return

        em = discord.Embed(
            title="New Alert",
            description="You have a new alert from the devs\nUse </alert:0> to check it out\n\
                Use </togglealerts:0> to not show these types of messages",
            color=discord.Color.random(),
        )

        try:  # try to send the message
            await ctx.followup.send(embed=em, ephemeral=True)
        except discord.HTTPException:  # frik it failed, probably perms or smth like that
            return

    @commands.slash_command(description="Shows the latest update from the why bot devs")
    async def alert(self, ctx: discord.ApplicationContext):
        data = await self.client.db.fetch("SELECT * FROM alerts ORDER BY id")
        data = data[::-1][0]

        description = data[2]
        date = discord_timestamp(data[3], format_type="ts")
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

    @commands.slash_command(
        description="Disables the new alert message that shows when theres a new update"
    )
    async def togglealerts(self, ctx: discord.ApplicationContext):
        data = await self.client.db.fetch(
            "SELECT * FROM alerts_users WHERE user_id=$1", ctx.author.id
        )
        if not data:
            await self.__setup_settings(ctx.author.id)
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

    @commands.slash_command(description="Creates a new alert", guild_ids=GUILD_IDS)
    @commands.is_owner()
    async def newalert(self, ctx, name):
        input = InputModalView(
            title="Alert Value", label="Enter the value of the alert:"
        )
        await ctx.send_modal(input)
        await input.wait()

        if input.value is None:
            return await ctx.respond(
                "Not creating alert as input was either None or invalid", ephemeral=True
            )

        # create tag
        await self.client.db.execute(
            """INSERT INTO alerts (
                alert_title, alert_message, time_created
            ) VALUES ($1, $2, $3)""",
            name,
            input.value,
            int(time.time()),
        )

        await self.client.db.execute("UPDATE alerts_users SET alert_viewed=false")

        await ctx.respond(
            "Alert Created! It will look like this:",
            embed=discord.Embed(
                title=name, description=input.value, color=discord.Color.random()
            ),
        )


def setup(client):
    client.add_cog(Alerts(client))
