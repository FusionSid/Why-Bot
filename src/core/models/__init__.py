from discord.ext import commands

from .client import WhyBot
from .counting import CountingData
from .level import (
    LevelingDataGuild,
    LevelingDataMember,
)
from .rps import RockPaperScissorsView
from .tag import Tag
from .ticket import TicketGuild, Ticket, TicketView, NewTicketView, ClosedTicketView
from .ttt import TicTacToeAIView, TicTacToe2PlayerView
from core.helpers.checks import run_bot_checks

__all__ = [
    "WhyBot",
    "CountingData",
    "LevelingDataGuild",
    "LevelingDataMember",
    "RockPaperScissorsView",
    "Tag",
    "TicketGuild",
    "Ticket",
    "TicketView",
    "NewTicketView",
    "ClosedTicketView",
    "TicTacToeAIView",
    "TicTacToe2PlayerView",
]


class BaseCog(commands.Cog):
    """base class for cogs"""

    def __init__(self, client: WhyBot) -> None:
        self.client = client
        self.cog_check = run_bot_checks
