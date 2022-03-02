import discord
import datetime
from discord.ext import commands
from utils import get_log_channel
import json

async def plugin_enabled(guild):
    with open("./database/db.json") as f:
        data = json.load(f)

    data = data[str(guild.id)]
    
    if data["settings"]['plugins']["Logging"]:
        return True
    return False


class Log(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if await plugin_enabled(before.guild) == False:
            return
        if after.author.id == self.client.user.id:
            return
        em = discord.Embed(color=discord.Color.blue(), 
            title="Message Edit", description=f"{before.author} edited their message", timestamp = datetime.datetime.utcnow())
        em.add_field(name="Before", value=before.content)
        em.add_field(name="After", value=after.content)

        channel = await get_log_channel(self.client, before.guild)
        if channel == None:
            return
        else:
            
            await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if await plugin_enabled(message.guild) == False:
            return
        if message.author.id == self.client.user.id:
            return

        em = discord.Embed(color=discord.Color.blue(), 
            title="Message Delete", description=f"{message.author} has deleted the message", timestamp = datetime.datetime.utcnow())
        em.add_field(name="Content:", value=f"{message.content}")

        channel = await get_log_channel(self.client, message.guild)
        if channel == None:
            return
        else:
            
            await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if await plugin_enabled(guild) == False:
            return
        em = discord.Embed(color=discord.Color.blue(), 
            title="Member Banned!", description=f"{user.name} Has been banned from the server", timestamp = datetime.datetime.utcnow())
        channel = await get_log_channel(self.client, guild)
        if channel == None:
            return
        else:
            
            await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if await plugin_enabled(guild) == False:
            return
        em = discord.Embed(color=discord.Color.blue(), 
            title="Member Unbanned!", description=f"{user.name} Has been unbanned from the server", timestamp = datetime.datetime.utcnow())
        channel = await get_log_channel(self.client, guild)
        
        if channel == None:
            return
        else:
            await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if await plugin_enabled(before.guild) == False:
            return
        if before.nick is not None and after.nick is None:
            em = discord.Embed(color=discord.Color.blue(), title="Nick Change",
                                description=f"{before.name} has unicked", timestamp = datetime.datetime.utcnow())
            em.add_field(name="Before:", value=before.nick)
            em.add_field(name="After:", value="No Nick")

        if before.nick is None and after.nick is not None:
            em = discord.Embed(color=discord.Color.blue(), title="Nick Change",
                                description=f"{before.name} Has nicked", timestamp = datetime.datetime.utcnow())
            em.add_field(name="Before:", value="No Nick")
            em.add_field(name="After:", value=after.nick)

        elif before.nick != after.nick:
            em = discord.Embed(color=discord.Color.blue(), 
                title="Nick Change", description=f"{before.name} Has changed their nick", timestamp = datetime.datetime.utcnow())
            em.add_field(name="Before:", value=before.nick)
            em.add_field(name="After:", value=after.nick)

        channel = await get_log_channel(self.client, after.guild)
        if channel == None:
            return
        else:
            
            await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if await plugin_enabled(channel.guild) == False:
            return
        em = discord.Embed(color=discord.Color.blue(), title="Channel Created",
                            description=f"`{channel.name}` Has been created", timestamp = datetime.datetime.utcnow())
        channel = await get_log_channel(self.client, channel.guild)
        if channel == None:
            return
        else:
            
            await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if await plugin_enabled(channel.guild) == False:
            return
        em = discord.Embed(color=discord.Color.blue(), title="Channel Delete",
                            description=f"`{channel.name}` Has been deleted", timestamp = datetime.datetime.utcnow())
        channel = await get_log_channel(self.client, channel.guild)
        if channel == None:
            return
        else:
            
            await channel.send(embed=em)


def setup(client):
    client.add_cog(Log(client))
