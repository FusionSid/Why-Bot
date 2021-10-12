import discord
import random
from discord.ext import commands
from roastlist import roastlistpy

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
    async def roast(ctx):
        roast = random.choice(roastlistpy)
        em = discord.Embed(title=roast)
        await ctx.send(embed=em)


    @commands.command()
    async def dm(ctx, member: discord.Member, *, message):
        await ctx.channel.purge(limit=1)
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)


    @commands.command()
    async def sendroast(ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        message = random.choice(roastlistpy)
        embeddm = discord.Embed(
            title=message, description="Imagine being roasted by a bot")
        await member.send(embed=embeddm)


def setup(client):
    client.add_cog(Fun(client))


