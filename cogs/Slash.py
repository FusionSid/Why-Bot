from discord import Client, Intents, Embed
from discord_slash import cog_ext, SlashContext


class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="sus")
    async def _sus(self, ctx: SlashContext):
        embed = Embed(title="Thats kinda sus ngl")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Slash(client))
