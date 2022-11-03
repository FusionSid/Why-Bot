import time
import datetime

import discord
from discord.ext import commands

from core.models import WhyBot
from core.utils.other import chunkify


class Server(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.slash_command(guild_ids=[763348615233667082, 938913935774605442])
    @commands.is_owner()
    async def server_list(self, ctx: discord.ApplicationContext):
        """
        This command is used to list the servers the bots in
        It makes an embed with a list of the servers
        """
        em = discord.Embed(
            title=f"Connected on {str(len(self.client.guilds))} servers:",
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow(),
        )

        if len(self.client.guilds) < 10:
            for guild in self.client.guilds:
                em.add_field(
                    name=guild.name,
                    value=(
                        f"Owner: {guild.owner.name}\nMembers: {guild.member_count}\nID:"
                        f" {guild.id}"
                    ),
                    inline=True,
                )
            return await ctx.respond(embed=em)

        chunked_list = await chunkify(self.client.guilds)

        em = discord.Embed(
            title=f"Connected on {str(len(self.client.guilds))} servers:",
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow(),
        )

        await ctx.send(embed=em)
        for chunk in chunked_list:
            em = discord.Embed(
                title="** **",
                color=ctx.author.color,
                timestamp=datetime.datetime.utcnow(),
            )
            for guild in chunk:
                em.add_field(
                    name=guild.name,
                    value=(
                        f"Owner: {guild.owner.name}\nMembers: {guild.member_count}\nID:"
                        f" {guild.id}"
                    ),
                    inline=True,
                )
            await ctx.respond(embed=em)

    @commands.slash_command(guild_ids=[763348615233667082, 938913935774605442])
    @commands.is_owner()
    async def fetch_server_info(self, ctx: discord.ApplicationContext, server_id: int):
        """This command is used to get info on a server that the bot is in"""

        guild = self.client.get_guild(server_id)

        em = discord.Embed(
            title="Server Info:",
            description=f"For: {guild.name}",
            color=ctx.author.color,
        )
        em.add_field(name="Member Count:", value=guild.member_count, inline=False)
        em.add_field(
            name="Created: ",
            value=f"<t:{int(time.mktime(guild.created_at.timetuple()))}>",
            inline=False,
        )
        em.add_field(name="ID:", value=guild.id, inline=False)

        em.set_thumbnail(url=guild.icon.url)
        em.set_author(
            name=f"Guild Owner: {guild.owner.name}", icon_url=guild.owner.avatar.url
        )

        await ctx.respond(embed=em)

    @commands.slash_command(
        description="fetch user info",
        guild_ids=[763348615233667082, 938913935774605442],
    )
    @commands.is_owner()
    async def fetch_user_info(self, ctx: discord.ApplicationContext, user: str):
        """
        This command is used to fetch info a specific user.
        It is useful if you are messaging someone in dmreply and want to know who you are messaging
        """

        try:
            user = await self.client.fetch_user(int(user))
        except discord.NotFound:
            return

        emb = discord.Embed(
            title=user.name,
            color=discord.Color.random(),
            timestamp=datetime.datetime.now(),
        )
        emb.set_thumbnail(url=user.avatar.url)

        emb.add_field(name="User ID:", value=user.id, inline=False)
        emb.add_field(
            name="Created Account:",
            value=f"<t:{int(time.mktime(user.created_at.timetuple()))}>",
            inline=False,
        )

        shared_guilds = [
            guild.name for guild in self.client.guilds if user in guild.members
        ]
        emb.add_field(
            name=f"Shared Guilds: ({len(shared_guilds)})",
            value=", ".join(shared_guilds),
        )

        emb.timestamp = datetime.datetime.now()

        data = await self.client.db.fetch(
            "SELECT * FROM command_stats WHERE user_id=$1", user.id
        )
        if len(data):
            usage = sum(i[3] for i in data)
            emb.add_field(
                name="Command Usage",
                value=f"This user has used the bot {usage} times",
                inline=False,
            )
        else:
            emb.add_field(
                name="Why Bot Usage",
                value=f"This user has not used any why bot commands",
                inline=False,
            )

        await ctx.respond(embed=emb)


def setup(client):
    client.add_cog(Server(client))
