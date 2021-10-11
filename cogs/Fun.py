import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
  def __init__(self, client):
    self.client = client

    @commands.command()
    async def rps(self, ctx, rps:str):
        choices = ["Rock", "Paper", "Scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors")
        if rps == 'rock':
            if cpu_choice == 'rock':
                em.title = "It's a tie!"
            elif cpu_choice == 'scissors':
                em.title = "You win!"
            elif cpu_choice == 'paper':
                em.title = "You lose!"

        elif rps == 'paper':
            if cpu_choice == 'paper':
                em.title = "It's a tie!"
            elif cpu_choice == 'rock':
                em.title = "You win!"
            elif cpu_choice == 'scissors':
                em.title = "You lose!"

        elif rps == 'scissors':
            if cpu_choice == 'scissors':
                em.title = "It's a tie!"
            elif cpu_choice == 'paper':
                em.title = "You win!"
            elif cpu_choice == 'rock':
                em.title = "You lose!"

        else:
            em.title = "Invalid Input"

        em.add_field(name="Your Choice", value=rps)
        em.add_field(name="Bot Choice", value=cpu_choice)
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Fun(client))
