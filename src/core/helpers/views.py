import discord


class RickRollView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=5)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Claim")
    async def claim_button(self, button, interaction):
        button.style = discord.ButtonStyle.red
        button.label = "Claimed"
        button.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send("https://imgur.com/NQinKJB", ephemeral=True)
        await interaction.followup.send(
            "You were the {} person to get rickrolled", ephemeral=True
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
