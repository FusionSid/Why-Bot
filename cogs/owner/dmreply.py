import discord
import asyncio
import datetime
from discord.ext import commands
from utils import is_it_me
import json

async def put_on_cooldown(self, member):
    self.users_on_cooldown.append(member.id)
    await asyncio.sleep(2)
    self.users_on_cooldown.remove(member.id)

class DMReply(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dm_channel = 926232260166975508

        self.users_on_cooldown = []

        self.user_message_count = {}

    @commands.command()
    @commands.check(is_it_me)
    async def dm_ban(self, ctx, id:int):
        with open("./database/dm_banned.json") as f:
            banned = json.load(f)
        if id not in banned:
            banned.append(id)
            await ctx.send("User Banned")
        with open("./database/dm_banned.json", 'w') as f:
            json.dump(banned, f, indent=4)
    

    @commands.command()
    @commands.check(is_it_me)
    async def dm_unban(self, ctx, id:int):
        with open("./database/dm_banned.json") as f:
            banned = json.load(f)
        if id in banned:
            banned.remove(id)
            await ctx.send("User Unbanned")
        with open("./database/dm_banned.json", 'w') as f:
            json.dump(banned, f, indent=4)


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            with open("./database/dm_banned.json") as f:
                banned = json.load(f)
            if message.author.id in banned:
                return await message.author.send('You have been dm banned')
            if message.author.id in self.users_on_cooldown:
                return await message.author.send("Youre on cooldown")
            await put_on_cooldown(self,message.author)

            cha = await self.client.fetch_channel(self.dm_channel)
            em = discord.Embed(title="New DM", description=f"From {message.author.name}", color=message.author.color)
            em.timestamp = datetime.datetime.utcnow()

            if message.content != "":
                em.add_field(name="Content", value=f"{message.content}")
            await cha.send(content=f"{message.author.id}", embed=em)

            if message.attachments is not None:
                for attachment in message.attachments:
                    if "image/" not in str(attachment.content_type):
                        return await cha.send(attachment.url)
                    em = discord.Embed(title="** **", color=discord.Color.blue())
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_image(url=attachment.url)
                    await cha.send(embed=em)

        # reply
        try:
            if message.channel.id == self.dm_channel and message.author.id == self.client.owner_id:
                if message.reference is None:
                    return
                else:
                    id = message.reference.message_id
                    id = await message.channel.fetch_message(id)
                    id = int(id.content)
                person = await self.client.fetch_user(id)

                if message.content is None:
                    pass
                else:
                    sent_message = await person.send(message.content)
                    try:
                        await message.add_reaction("✅")
                    except Exception as e:
                        print(e)

                if message.attachments is None:
                    return
                else:
                    for i in message.attachments:
                        if "image/" not in str(i.content_type):
                            return await person.send(i.url)
                        em = discord.Embed(color=message.author.color)
                        em.timestamp = datetime.datetime.utcnow()
                        em.set_image(url=i.url)
                        await person.send(embed=em)

        except Exception:
            return

    @commands.command()
    async def dm_delete(self, ctx, channel_id : int, message_id:int):
        channel = await self.client.fetch_channel(channel_id)
        message = await channel.fetch_message(message_id)

        await message.delete()
        await ctx.message.add_reaction("✅")

def setup(client):
    client.add_cog(DMReply(client))