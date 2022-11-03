import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.models import WhyBot
from core.helpers.views import ConfirmView
from core.helpers.checks import run_bot_checks
from core.models.ttt import TicTacToeAIView, TicTacToe2PlayerView


class TicTacToeCog(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    tictactoe_cmd = SlashCommandGroup("tictactoe", "Tic tac toe commands")

    @tictactoe_cmd.command(
        name="tictactoe", description="Play against someone on your server"
    )
    async def tictactoe_multiplayer(
        self, ctx: discord.ApplicationContext, opponent: discord.Member
    ):
        if opponent == ctx.author:
            return await ctx.respond("You can't play against yourself", ephemeral=True)
        await ctx.respond("Waiting for opponent to accept", ephemeral=True)

        view = ConfirmView(target=opponent)
        em = discord.Embed(
            title="Confirm Or Deny",
            description=(
                f"{ctx.author.mention} would like to play a game of tic tac toe with"
                " you\nDo you want to play?"
            ),
            color=discord.Color.random(),
        )
        await ctx.send(content=opponent.mention, embed=em, view=view)
        await view.wait()

        if not view.accepted:
            return await ctx.respond(
                embed=discord.Embed(
                    title="Tic Tac Toe",
                    description=(
                        f"{opponent.mention} denied your request to play tic tac toe"
                        " with them"
                    ),
                    color=discord.Color.random(),
                ),
                ephemeral=True,
            )

        game = TicTacToe2PlayerView(ctx.author, opponent)
        await ctx.send(
            embed=discord.Embed(
                title="Tic Tac Toe",
                description=(
                    f"X = {opponent.display_name}\nO ="
                    f" {ctx.author.display_name}\n{opponent.display_name} starts!"
                ),
                color=discord.Color.random(),
            ),
            view=game,
        )

    @tictactoe_cmd.command(name="ai", description="Play against the bot")
    async def tictactoe_ai(self, ctx: discord.ApplicationContext):

        game = TicTacToeAIView(ctx.author)
        await ctx.respond(
            embed=discord.Embed(
                title="Tic Tac Toe",
                description=f"X = {ctx.author.display_name}\nO = Bot",
                color=discord.Color.random(),
            ),
            view=game,
        )


def setup(client):
    client.add_cog(TicTacToeCog(client))
