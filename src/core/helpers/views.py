import asyncpg
import discord
from simpcalc import simpcalc
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


class CalculatorView(discord.ui.View):
    """This is a view for the calculator"""

    def __init__(self, ctx):
        self.expr = ""
        self.ctx = ctx
        super().__init__(timeout=100)
        self.calc = simpcalc.Calculate()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="1", row=0)
    async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "1"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="2", row=0)
    async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "2"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="3", row=0)
    async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "3"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="+", row=0)
    async def plus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "+"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="4", row=1)
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "4"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="5", row=1)
    async def five(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "5"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="6", row=1)
    async def six(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "6"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="/", row=1)
    async def divide(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "/"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "7"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "8"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "9"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="*", row=2)
    async def multiply(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.expr += "*"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "."
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "0"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="=", row=3)
    async def equal(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            self.expr = await self.calc.calculate(self.expr)
        except:  # if you are function only, change this to BadArgument
            return await interaction.response.send_message(
                "Um, looks like you provided a wrong expression...."
            )
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="-", row=3)
    async def minus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "-"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="(", row=4)
    async def left_bracket(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.expr += "("
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label=")", row=4)
    async def right_bracket(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.expr += ")"
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.red, label="C", row=4)
    async def clear(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = ""
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.red, label="<==", row=4)
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = self.expr[:-1]
        await interaction.response.edit_message(content=f"```\n{self.expr}\n```")

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "This calculator is not for you. Use /calculator to get your own.",
                ephemeral=True,
            )
            return False
        return True

    async def on_timeout(self) -> None:
        for button in self.children:
            button.disabled = True

        await self.message.edit(view=self)
        return await super().on_timeout()


class ConfirmView(discord.ui.View):
    def __init__(self, target: discord.Member):
        self.target = target
        self.accepted = False
        super().__init__(timeout=10)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True

        await self.message.edit(view=self)

        await interaction.response.send_message("You accepted!", ephemeral=True)
        self.accepted = True
        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def deny_callback(self, button, interaction):
        for button in self.children:
            button.disabled = True

        await self.message.edit(view=self)

        await interaction.response.send_message("You Denied!", ephemeral=True)
        self.accepted = False
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.target:
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
