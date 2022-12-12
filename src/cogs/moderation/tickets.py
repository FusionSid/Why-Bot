import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, default_permissions

from core.models import WhyBot
from core.models.ticket import TicketGuild, Ticket
from core.db.setup_guild import setup_tickets
from core.helpers.checks import run_bot_checks


class Tickets(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    ticket = SlashCommandGroup("ticket", "Ticket related commands")

    async def __get_ticket_config(self, guild_id: int):
        data: list[list] = await self.client.db.fetch(
            "SELECT * FROM ticket_guild WHERE guild_id=$1", guild_id
        )
        if len(data) == 0:
            await setup_tickets(self.client.db, guild_id)
            default_data = [guild_id, [], [], False, None, []]
            return TicketGuild(*default_data)
        return TicketGuild(*data[0])

    async def __get_tickets(self, guild_id: int):
        data: list[list] = await self.client.db.fetch(
            "SELECT * FROM ticket_guild WHERE guild_id=$1", guild_id
        )
        if len(data) == 0:
            return None
        return list(map(lambda x: Ticket(*x), data))


def setup(client):
    client.add_cog(Tickets(client))
