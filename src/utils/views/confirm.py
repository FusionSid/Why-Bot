import discord


class ConfirmView(discord.ui.View):
    def __init__(self, target:discord.Member):
        self.target= target
        self.value = False
        super().__init__(timeout=10)


    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm_callback(self, button, interaction):
        self.value = True
        self.stop()


    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def deny_callback(self, button, interaction):
        self.value = False
        self.stop()


    async def interaction_check(self, interaction) -> bool:
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("This isnt for you", ephemeral=True)
            return False
        else:
            return True


    async def on_timeout(self) -> None:
        self.value = False
        self.stop()