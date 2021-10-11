import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rps(self, ctx, rps:str):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors")
        rps = rps.lower()
        if rps == 'rock':
            if cpu_choice == 'rock':
                em.description = "It's a tie!"
            elif cpu_choice == 'scissors':
                em.description = "You win!"
            elif cpu_choice == 'paper':
                em.description = "You lose!"

        elif rps == 'paper':
            if cpu_choice == 'paper':
                em.description = "It's a tie!"
            elif cpu_choice == 'rock':
                em.description = "You win!"
            elif cpu_choice == 'scissors':
                em.description = "You lose!"

        elif rps == 'scissors':
            if cpu_choice == 'scissors':
                em.description = "It's a tie!"
            elif cpu_choice == 'paper':
                em.description = "You win!"
            elif cpu_choice == 'rock':
                em.description = "You lose!"

        else:
            em.description = "Invalid Input"

        em.add_field(name="Your Choice", value=rps)
        em.add_field(name="Bot Choice", value=cpu_choice)
        await ctx.send(embed=em)

    @commands.command()
    async def numberguess(self, ctx):
        num = random.randint(0, 100)
        tries = 0
        errorem = discord.Embed(title = "Invalid Input", description = "Please enter a valid number from 0 - 100")
        em = discord.Embed(title="Number Guesser")

        while guess != num:
            guess = await self.client.wait_for("message", check=wfcheck)
            try:
                guess = int(guess)
                tries += 1

                if guess == num:
                    em.description = f"Correct\nYou guessed it in {tries} tries"
                elif guess > num:
                    em.description("To high guess lower")
                elif guess < num:
                    em.description("To low guess higher")

                elif guess > 100:
                    await ctx.send(embed=errorem)
                elif guess < 0:
                    await ctx.send(embed=errorem)
                else:
                    await ctx.send(embed=errorem)

                await ctx.send(embed = em)
            except:
                await ctx.send(embed = errorem)
            

def setup(client):
    client.add_cog(Fun(client))


