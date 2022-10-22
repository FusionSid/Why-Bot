import io
import time
import datetime

import discord
from discord.ext import commands

from core.models import WhyBot
from core.helpers.checks import blacklist_check
from core.utils.formatters import format_seconds


class DMReply(commands.Cog):
    """
    This is the dmreply cog
    It is used to provide support to the users of the bot
    When a dm is sent to the bot it will be copied and sent to the dm reply channel
    The bot owner will have the option to reply to the message
    You can send images, videos messages etc
    """

    def __init__(self, client: WhyBot):
        self.client = client

        dm_channel = self.client.config["dm_reply_channel"]
        if dm_channel == 0 or dm_channel == None:
            self.dm_reply_channel = None
        self.dm_reply_channel = dm_channel

        self.cooldown = commands.CooldownMapping.from_cooldown(
            10, 60, commands.BucketType.user
        )

    async def is_member_cooldown(self, message: discord.Message):
        bucket = self.cooldown.get_bucket(message)
        cooldown = bucket.update_rate_limit()

        if cooldown is None:
            return False

        retry_after = await format_seconds(int(cooldown))
        em = discord.Embed(
            title="Wow buddy, Slow it down\nYou are on cooldown from sending dms",
            description=(
                f"Try again {f'in **{retry_after}' if retry_after != '' else 'now'}**"
            ),
            color=discord.Color.red(),
        )
        await message.reply(embed=em)

        return True

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """The on message event that handles the dm's"""

        if message.author.bot:
            return

        # this should only run once
        if self.dm_reply_channel is not None and isinstance(self.dm_reply_channel, int):
            try:
                self.dm_reply_channel = await self.client.fetch_channel(
                    self.dm_reply_channel
                )
            except discord.errors.NotFound:
                self.dm_reply_channel = None

        if not await blacklist_check(message.author.id):
            return

        # check if in dm / thread
        if not isinstance(message.channel, discord.DMChannel):
            if (
                not isinstance(message.channel, discord.Thread)
                or message.author.id != self.client.owner_id
            ):
                return

            data = await self.client.db.fetch(
                "SELECT * FROM dmreply WHERE thread_id=$1", message.channel.id
            )
            if not len(data):
                return

            person = await self.client.fetch_user(data[0][0])

            if message.content is not None and message.content != "":
                await person.send(message.content)
                await message.add_reaction("✅")

            if message.attachments is not None:
                for attachment in message.attachments:
                    return await person.send(attachment.url)
            return

        # If user is on cooldown
        if await self.is_member_cooldown(message):
            return

        # if error getting dm reply channel or not set
        if self.dm_reply_channel is None:
            return await message.channel.send(
                "The owner has disabled the dm reply feature from the bot"
            )

        channel = self.dm_reply_channel
        author = message.author
        thread_id = await self.client.db.fetch(
            "SELECT * FROM dmreply WHERE user_id=$1", author.id
        )

        if not len(thread_id):
            thread_id = None

        thread = None

        if thread_id is not None:
            try:
                thread = channel.get_thread(thread_id[0][1])
            except discord.NotFound:
                thread = None
            if thread is None:
                await self.client.db.execute(
                    "DELETE FROM dmreply WHERE user_id=$1", author.id
                )

        if thread is None:
            emb = discord.Embed(
                title=author.name,
                color=discord.Color.random(),
                timestamp=datetime.datetime.now(),
            )
            emb.set_thumbnail(url=author.avatar.url)

            emb.add_field(name="User ID:", value=author.id, inline=False)
            emb.add_field(
                name="Created Account:",
                value=f"<t:{int(time.mktime(author.created_at.timetuple()))}>",
                inline=False,
            )

            shared_guilds = [
                guild.name for guild in self.client.guilds if author in guild.members
            ]
            emb.add_field(
                name=f"Shared Guilds: ({len(shared_guilds)})",
                value=", ".join(shared_guilds),
            )

            message_to_create_thread = await channel.send(embed=emb)
            thread = await message_to_create_thread.create_thread(name=author.name)
            await self.client.db.execute(
                "INSERT INTO dmreply (user_id, thread_id) VALUES ($1, $2)",
                author.id,
                thread.id,
            )
        if message.content != "" and message.content is not None:
            await thread.send(message.content)

        if message.attachments is not None:
            for attachment in message.attachments:
                await thread.send(attachment.url)

    @commands.slash_command()
    @commands.is_owner()
    async def dm_ban(self, ctx, _id: int):
        """
        TODO
        """
        pass

    @commands.slash_command()
    @commands.is_owner()
    async def dm_unban(self, ctx, _id: int):
        """
        TODO
        """
        pass

    @commands.slash_command()
    @commands.is_owner()
    async def close_thread(self, ctx, author_id: str, archive: bool = False):
        try:
            author_id = int(author_id)
        except ValueError:
            return await ctx.respond("Not found")

        thread_id = await self.client.db.fetch(
            "SELECT * FROM dmreply WHERE user_id=$1", author_id
        )

        if not len(thread_id):
            thread_id = None

        if thread_id is not None:
            try:
                thread: discord.Thread = self.dm_reply_channel.get_thread(
                    thread_id[0][1]
                )
            except discord.NotFound:
                return await ctx.respond("Not found")

        messages = "\n".join(
            [
                f"{message.author.name}: {message.content}\n---"
                async for message in thread.history(oldest_first=True)
                if message.content is not None or message.content != ""
            ]
        )
        file = io.BytesIO(messages.encode())
        await ctx.respond(file=discord.File(file, "messages.txt"), ephemeral=True)

        if archive:
            return await thread.archive()

        await thread.delete()


def setup(client: WhyBot):
    client.add_cog(DMReply(client))
