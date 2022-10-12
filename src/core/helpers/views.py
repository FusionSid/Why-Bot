import asyncpg
import discord
from core.utils.formatters import number_suffix


class RickRollView(discord.ui.View):
    """
    View with a button that says claim but after clicking the button you get rickrolled
    It also updates a counter with the amount of people rickrolled from the view

    Parameter:
        db (asyncpg.Pool): the connection to the psql database, used to update the counter
    """

    def __init__(self, db: asyncpg.Pool):
        self.db = db
        self.key = "rickroll_counter"
        super().__init__(timeout=500)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Claim")
    async def claim_button(self, button, interaction):
        button.style = discord.ButtonStyle.red
        button.label = "Claimed"
        button.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send("https://imgur.com/NQinKJB", ephemeral=True)

        count = await self.db.fetch("SELECT value FROM counters WHERE key=$1", self.key)
        count = count[0][0] + 1 if len(count) else None

        if count is None:
            await self.db.execute(
                "INSERT INTO counters (key, value) VALUES ($1, 1)",
                self.key,
            )
            count = 1

        await interaction.followup.send(
            f"You were the {await number_suffix(count)} person to get rickrolled\nLMAO imagine couldn't be me",
            ephemeral=True,
        )

        await self.db.execute(
            "UPDATE counters SET value=$1 WHERE key=$2", count, self.key
        )

    async def on_timeout(self) -> None:
        self.children[0].label = (
            "Timed Out"
            if self.children[0].label != "Claimed"
            else self.children[0].label
        )
        self.children[0].disabled = True
        await self.message.edit(view=self)

        return await super().on_timeout()


class BotInfoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.grey,
                label="Website / Dashboard",
                url="https://why.fusionsid.xyz/",
            )
        )
        self.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.grey,
                label="Source Code",
                url="https://github.com/FusionSid/Why-Bot",
            )
        )
        self.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.grey,
                label="Discord Server",
                url="https://discord.gg/Jm8QPF6xbN",
            )
        )
