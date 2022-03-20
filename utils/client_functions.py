""" (module) client_functions

Useful functions for the WhyBot client
"""

import discord
from discord.ext import commands

async def update_activity(client : commands.Bot):
    await client.change_presence(
        activity=discord.Game(
            f"On {len(client.guilds)} servers! | ?help"
            )
        )