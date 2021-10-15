import discord
from discord.ext import commands

def calculator(num1, operator, num2):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "/":
        return num1 / num2
    elif operator == "x":
        return num1 * num2

class Utilities(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def calc(self, ctx, n1: int, op, n2: int):
      ans = calculator(n1, op, n2)
      await ctx.send(embed=discord.Embed(title='Calculator Result:', description=ans))
  
def setup(client):
    client.add_cog(Utilities(client))