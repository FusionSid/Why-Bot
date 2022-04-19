import discord
from discord.ext import commands
from utils.views import ConfirmView

class RPS(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.emojis = {
            "Rock" : "👊",
            "Paper" : "🖐️",
            "Scissors" : "✌️"
        }

    
    @commands.command()
    async def rps_multiplayer(self, ctx, opponent:discord.Member):
        view = ConfirmView(target=opponent)
        em = discord.Embed(title="Confirm Or Deny", description=f"{opponent.mention} would you like to play a game of rock paper scissors with {ctx.author.mention}", color=ctx.author.color)
        message = await ctx.send(embed=em,view=view)
        await view.wait()
        they_said = "yes" if view.value else "no"
        for button in view.children:
            button.disabled = True
        await message.edit(view=view)
        await ctx.send(f"They said {they_said}")
        # Test lmao ^ will add the game later



def setup(client):
    client.add_cog(RPS(client))