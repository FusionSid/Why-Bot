import json
import datetime

import discord
import asyncio
from discord.ext import commands

from log import log_normal
from utils import WhyBot, blacklisted


async def put_on_cooldown(self, member):
    self.users_on_cooldown.append(member.id)
    await asyncio.sleep(2)
    self.users_on_cooldown.remove(member.id)


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
        self.dm_channel = client.config.dm_reply_channel

        self.users_on_cooldown = []

        self.user_message_count = {}

    @commands.command()
    @commands.is_owner()
    async def dm_ban(self, ctx, _id: int):
        """
        This command is used to ban a user from sending dm's to the bot
        They can still send dm's but they wont be processed by the dmreply event

        Help Info:
        ----------
        Category: Owner

        Usage: dm_ban <id: int>
        """
        with open("./database/dm_banned.json") as f:
            banned = json.load(f)
        if _id not in banned:
            banned.append(_id)
            await ctx.send("User Banned")
        with open("./database/dm_banned.json", "w") as f:
            json.dump(banned, f, indent=4)

    @commands.command()
    @commands.is_owner()
    async def dm_unban(self, ctx, _id: int):
        """
        This command is used to unban a user who was banned from sending dm's to the bot

        Help Info:
        ----------
        Category: Owner

        Usage: dm_unban <id: int>
        """
        with open("./database/dm_banned.json") as f:
            banned = json.load(f)
        if _id in banned:
            banned.remove(_id)
            await ctx.send("User Unbanned")
        with open("./database/dm_banned.json", "w") as f:
            json.dump(banned, f, indent=4)

    @commands.Cog.listener()
    @commands.check(blacklisted)
    async def on_message(self, message):
        """The on message event that handles the dm's"""

        if message.author.bot: return

        if self.dm_channel == 0 or self.dm_channel == None: return 

        if isinstance(message.channel, discord.DMChannel):
            with open("./database/dm_banned.json") as f:
                banned = json.load(f)

            if message.author.id in banned:
                return await message.author.send("You have been dm banned")

            if message.author.id in self.users_on_cooldown:
                return await message.author.send("Youre on cooldown")

            await put_on_cooldown(self, message.author)

            try:
                cha = await self.client.fetch_channel(self.dm_channel)
            except discord.errors.NotFound:
                return

            em = discord.Embed(
                title=f"New DM from {message.author.name}",
                description=f"Message ID: {message.id}\nChannel ID: {message.channel.id}",
                timestamp=datetime.datetime.utcnow(),
            )

            if message.content != "" and message.content is not None:
                em.add_field(name="Content", value=f"{message.content}")
            await cha.send(content=f"{message.author.id}", embed=em)

            if message.attachments is not None:
                for attachment in message.attachments:
                    if "image/" not in str(attachment.content_type):
                        return await cha.send(attachment.url)
                    em = discord.Embed(title="** **", color=discord.Color.blue())
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_image(url=attachment.url)
                    await cha.send("** **", embed=em)

        if (
            message.channel.id == self.dm_channel
            and message.author.id == self.client.owner_id
        ):
            if message.reference is None:
                return

            _id = message.reference.message_id
            _id = await message.channel.fetch_message(_id)
            _id = int(_id.content)
            person = await self.client.fetch_user(_id)

            if message.content is not None and message.content != "":
                await person.send(message.content)
                await message.add_reaction("✅")

            if message.attachments is not None:
                for attachment in message.attachments:
                    if "image/" not in str(attachment.content_type):
                        return await person.send("** **", attachment.url)
                    em = discord.Embed(color=message.author.color)
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_image(url=attachment.url)
                    await person.send("** **", embed=em)

    @commands.command()
    @commands.is_owner()
    async def dmcontext(self, ctx, channel_id: int, limit: int = 10):
        channel = await self.client.fetch_channel(channel_id)
        description = ""
        async for message in channel.history(limit=limit):
            if message.attachments is not None:
                for i in message.attachments:
                    await ctx.send(i.url)
            if message.content == "":
                continue
            description += f"\n**{message.author.name}** ({message.created_at.strftime('%m/%d/%Y-%H:%M')}): {message.content}"

        await ctx.send(description)


def setup(client: WhyBot):
    client.add_cog(DMReply(client))
