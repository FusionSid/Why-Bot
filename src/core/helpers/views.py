import discord

KEY = "rickroll_counter"

from core.utils.formatters import number_suffix


class RickRollView(discord.ui.View):
    def __init__(self, db):
        self.db = db
        super().__init__(timeout=500)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Claim")
    async def claim_button(self, button, interaction):
        button.style = discord.ButtonStyle.red
        button.label = "Claimed"
        button.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send("https://imgur.com/NQinKJB", ephemeral=True)

        count = await self.db.fetch("SELECT value FROM counters WHERE key=$1", KEY)
        count = count[0][0] + 1 if len(count) else None

        if count is None:
            await self.db.execute(
                "INSERT INTO counters (key, value) VALUES ($1, 1)",
                KEY,
            )
            count = 1

        await interaction.followup.send(
            f"You were the {await number_suffix(count)} person to get rickrolled\nLMAO imagine couldn't be me",
            ephemeral=True,
        )

        await self.db.execute("UPDATE counters SET value=$1 WHERE key=$2", count, KEY)

    async def on_timeout(self) -> None:
        self.children[0].label = (
            "Timed Out"
            if self.children[0].label != "Claimed"
            else self.children[0].label
        )
        self.children[0].disabled = True
        await self.message.edit(view=self)

        return await super().on_timeout()
