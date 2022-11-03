import discord
from discord.ext import commands
import pycord.wavelink as wavelink


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


async def get_player(self, ctx: discord.ApplicationContext):
    if isinstance(ctx, (discord.ApplicationContext, commands.Context)):
        return
