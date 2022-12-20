from pycord.ext import ipc
from discord.ext import commands

from core.models import WhyBot


class IPCRoutes(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @ipc.server.route()
    async def get_member_count(self, data: dict):
        guild = await self.client.fetch_guild(data.guild_id)
        return guild.member_count


def setup(client):
    client.add_cog(IPCRoutes(client))
