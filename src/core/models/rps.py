import discord


class RockPaperScissorsView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        self.results = {}
        self.p1 = player1
        self.p2 = player2
        super().__init__(timeout=100)

    @discord.ui.button(
        style=discord.ButtonStyle.green, label="Rock", emoji="🗿", custom_id="rock"
    )
    async def rock(self, button, interaction):
        await interaction.response.send_message(f"You chose rock", ephemeral=True)
        await self.handle_input(interaction.user, button.custom_id)

    @discord.ui.button(
        style=discord.ButtonStyle.green, emoji="📄", label="Paper", custom_id="paper"
    )
    async def paper(self, button, interaction):
        await interaction.response.send_message(f"You chose paper", ephemeral=True)
        await self.handle_input(interaction.user, button.custom_id)

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="Scissors",
        emoji="✂️",
        custom_id="scissors",
    )
    async def scissor(self, button, interaction):
        await interaction.response.send_message(f"You chose scissors", ephemeral=True)
        await self.handle_input(interaction.user, button.custom_id)

    async def handle_input(self, user, input):
        self.results[user.id] = input

        if self.results.get(self.p1.id) is None or self.results.get(self.p2.id) is None:
            return

        for button in self.children:
            button.disabled = True

        await self.message.edit(view=self)
        await super().on_timeout()

        self.stop()

        if self.results[self.p1.id] == self.results[self.p2.id]:
            await self.message.channel.send(
                embed=discord.Embed(
                    title="Rock Paper Scissors",
                    description=f"It is a Draw!",
                    color=discord.Color.random(),
                )
            )

        p1_win = discord.Embed(
            title="Rock Paper Scissors",
            description=f"Yay {self.p1.mention} wins!",
            color=discord.Color.random(),
        )
        p2_win = discord.Embed(
            title="Rock Paper Scissors",
            description=f"Yay {self.p2.mention} wins!",
            color=discord.Color.random(),
        )

        if self.results[self.p1.id] == "rock":
            if self.results[self.p2.id] == "scissors":
                await self.message.channel.send(embed=p1_win)
            elif self.results[self.p2.id] == "paper":
                await self.message.channel.send(embed=p2_win)

        elif self.results[self.p1.id] == "paper":
            if self.results[self.p2.id] == "rock":
                await self.message.channel.send(embed=p1_win)
            elif self.results[self.p2.id] == "scissors":
                await self.message.channel.send(embed=p2_win)

        elif self.results[self.p1.id] == "scissors":
            if self.results[self.p2.id] == "paper":
                await self.message.channel.send(embed=p1_win)
            elif self.results[self.p2.id] == "rock":
                await self.message.channel.send(embed=p2_win)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user not in [self.p1, self.p2]:
            await interaction.response.send_message(
                "This button is not for you!",
                ephemeral=True,
            )
            return False
        return True

    async def on_timeout(self) -> None:
        for button in self.children:
            button.disabled = True

        await self.message.edit(view=self)
        await super().on_timeout()

        self.stop()
        await self.message.reply("Timed Out")
