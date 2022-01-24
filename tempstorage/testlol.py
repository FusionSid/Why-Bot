import discord

async def run(channel):
    em = discord.Embed(title="e", description="e")
    await channel.send(embed=em)