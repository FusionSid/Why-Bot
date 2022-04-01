import time
import datetime
from typing import Union

import discord
from discord.ext import commands

from utils import WhyBot, kwarg_to_embed

class Server(commands.Cog):
    def __init__(self, client : WhyBot):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def server_list(self, ctx):
        em = discord.Embed(
            title = f"Connected on {str(len(self.client.guilds))} servers:",
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )

        if len(self.client.guilds) < 10:
            for guild in self.client.guilds:
                em.add_field(name=guild.name, value=f"Owner: {guild.owner.name}\nMembers: {guild.member_count}\nID: {guild.id}", inline=True)
            return await ctx.send(embed=em)

        chunk_size = 15
        chunked_list = list()

        for i in range(0, len(self.client.guilds), chunk_size):
            chunked_list.append(self.client.guilds[i:i+chunk_size])

        em = discord.Embed(
            title = f"Connected on {str(len(self.client.guilds))} servers:",
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )

        await ctx.send(embed=em)
        for chunk in chunked_list:
            em = discord.Embed(
                title = "** **",
                color=ctx.author.color,
                timestamp=datetime.datetime.utcnow()
            )
            for guild in chunk:
                em.add_field(name=guild.name, value=f"Owner: {guild.owner.name}\nMembers: {guild.member_count}\nID: {guild.id}", inline=True)
            await ctx.send(embed=em)


    @commands.command()
    @commands.is_owner()
    async def server_fetch_info(self, ctx, server_id : int):
        guild = self.client.get_guild(server_id)
        
        em = discord.Embed(title="Server Info:", description=f"For: {guild.name}", color=ctx.author.color)
        em.add_field(name="Member Count:", value=guild.member_count) 
        em.add_field(name="Created: ", value=f"<t:{int(time.mktime(guild.created_at.timetuple()))}>")
        em.add_field(name="ID:", value=guild.id)

        em.set_thumbnail(url=guild.icon.url)
        em.set_author(name=f"Guild Owner: {guild.owner.name}", icon_url=guild.owner.avatar.url)
        
        await ctx.send(embed=em)


    @commands.command()
    @commands.is_owner()
    async def message_server(self, ctx, server_id : int, *, message):
        data = await kwarg_to_embed(self.client, ctx, message)
        em = data[0]

        guild = await self.client.fetch_guild(server_id)
        # send to announcment channel


    @commands.command()
    @commands.is_owner()
    async def message_all_servers(self, ctx, *, message):
        data = await kwarg_to_embed(self.client, ctx, message)
        em = data[0]

        for guild in self.client.guilds:
            pass # send to announcment channel
    

    @commands.command()
    @commands.is_owner()
    async def fetch_user_info(self, ctx, user_id : Union[int, discord.Member]):
        pass


def setup(client):
    client.add_cog(Server(client))