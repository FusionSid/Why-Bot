import discord

async def get_log_channel(client, guild):
    """
    This function is used to find the guilds log channel
    This channel is used to log things like message edits or kicks

    Args:
    client (discord.ext.commands.Bot) : This is the discord bot
    guild (discord.Guild) : This is the guild

    Returns:
    discord.TextChannel : This is the log channel
    """
    data = await client.get_db()

    if data[str(guild.id)]['log_channel'] is None:
        return None

    channel = data[str(guild.id)]['log_channel']
    return await client.fetch_channel(channel)