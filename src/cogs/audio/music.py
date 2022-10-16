import discord
from discord.ext import commands
import pycord.wavelink as wavelink
from discord import ApplicationContext

from core.models import WhyBot
from core.helpers.music import Player


class Music(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.pool = wavelink.NodePool()
        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        nodes = [
            {
                "host": "168.138.102.186",
                "port": 2333,
                "password": "shitcodengl",
                "https": False,
                "region": discord.VoiceRegion.sydney,
                "identifier": "MAIN",
            },
            {"host": "lava.link", "port": 80, "password": "dismusic", "https": False},
        ]

        for node in nodes:
            await self.pool.create_node(bot=self.client, **node)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        self.client.console.print(
            f"\n[bold green]Music Node ({node.identifier}) is ready!"
        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            members = [i for i in before.channel.members if not i.bot]

    @commands.slash_command()
    async def play(self, ctx: ApplicationContext, search: str):
        """Play a song with the given search query.
        If not connected, connect to our voice channel.
        """
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            vc: wavelink.Player = ctx.voice_client
        print(vc.node.identifier)
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        print(search.author)
        await vc.play(search)

    @commands.slash_command()
    async def join(self, ctx, channel: discord.VoiceChannel = None):
        pass


def setup(client):
    client.add_cog(Music(client))
