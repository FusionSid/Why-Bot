import discord
from discord.ext import commands

from core.models import WhyBot
from core.helpers.views import ConfirmView
from core.helpers.checks import run_bot_checks
from core.models.rps import RockPaperScissorsView


class RockPaperScissors(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    @commands.slash_command(name="rps")
    async def rock_paper_scissors_command(
        self, ctx: discord.ApplicationContext, opponent: discord.Member
    ):

        if opponent == ctx.author:
            return await ctx.respond("You can't play against yourself", ephemeral=True)

        await ctx.respond("Waiting for opponent to accept", ephemeral=True)

        view = ConfirmView(target=opponent)
        em = discord.Embed(
            title="Confirm Or Deny",
            description=(
                f"{ctx.author.mention} would like to play a game of rock paper scissors"
                " with you\nDo you want to play?"
            ),
            color=discord.Color.random(),
        )

        await ctx.send(content=opponent.mention, embed=em, view=view)
        await view.wait()

        if not view.accepted:
            return await ctx.send(
                embed=discord.Embed(
                    title="Rock Paper Scissors",
                    description=(
                        f"{opponent.mention} denied your request to rock paper scissors"
                        " with them"
                    ),
                    color=discord.Color.random(),
                ),
                ephemeral=True,
            )

        game = RockPaperScissorsView(ctx.author, opponent)
        await ctx.respond(
            f"{opponent.mention} accepted to play with you. Game is now starting...",
            ephemeral=True,
        )
        await ctx.send(
            embed=discord.Embed(
                title="Rock Paper Scissors",
                description=(
                    f"{ctx.author.mention} & {opponent.mention} choose your move:"
                ),
                color=discord.Color.random(),
            ),
            view=game,
        )


def setup(client):
    client.add_cog(RockPaperScissors(client))
