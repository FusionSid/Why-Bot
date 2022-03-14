import discord

async def update_activity(client):
    await client.change_presence(
        activity=discord.Game(
            f"On {len(client.guilds)} servers! | ?help"
            )
        )