import discord
import asyncio
import datetime
from discord.ext import commands
from utils import is_it_me

async def put_on_cooldown(self, member):
    self.users_on_cooldown.append(member.id)
    await asyncio.sleep(2)
    self.users_on_cooldown.remove(member.id)

class DMReply(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dm_channel = 926232260166975508

        self.users_on_cooldown = []
        self.banned = []

        self.user_message_count = {}


    @commands.command()
    @commands.check(is_it_me)
    async def dm_ban(self, ctx, id:int):
        self.banned.append(id)
        await ctx.send("User Banned")
    

    @commands.command()
    @commands.check(is_it_me)
    async def dm_unban(self, ctx, id:int):
        try:
            self.banned.remove(id)
            await ctx.send("User Unbanned")
        except Exception:
            return


    @commands.command(aliases=['dmr'])
    @commands.check(is_it_me)
    async def dmreply(self, ctx, *, msg=None):
        if ctx.message.reference is None:
          return
        else:
            await ctx.message.delete()
            id = ctx.message.reference.message_id
            id = await ctx.channel.fetch_message(id)
            await id.reply(msg)
            id = int(id.content)
        person = await self.client.fetch_user(id)

        if msg is None:
            pass
        else:
            await person.send(msg)

        if ctx.message.attachments is None:
            return
        else:
            for i in ctx.message.attachments:
                em = discord.Embed( color=ctx.author.color)
                em.timestamp = datetime.datetime.utcnow()
                em.set_image(url=i.url)
                await person.send(embed=em)


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            if message.author.id in self.banned:
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
                    await person.send(message.content)
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

def setup(client):
    client.add_cog(DMReply(client))