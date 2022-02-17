import discord

async def update_activity(client):
    """
    Used to updates the bots discord.Game activity
    to show the current server count

    Args:

    client (discord.ext.commands.Bot) : The bot, This will be used to update the guild count

    """
    await client.change_presence(
        activity=discord.Game(
            f"On {len(client.guilds)} servers! | ?help"
            )
        )


