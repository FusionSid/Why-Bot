from dataclasses import dataclass

import discord


@dataclass
class TicketGuild:
    guild_id: int
    roles_allowed: list[int]
    ping_roles: list[int]
    create_button: bool
    category: int
    banned_users: list[int]


@dataclass
class Ticket:
    ticket_id: int
    guild_id: int
    channel_id: int
    ticket_creator: int
    time_created: int


async def get_button(guild_id: int) -> discord.ui.Button:
    return discord.ui.Button()


class TicketView(discord.ui.View):
    def __init__(self, button: discord.ui.Button):
        super().__init__(timeout=None)
        self.add_item(button)
