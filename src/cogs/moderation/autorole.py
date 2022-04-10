from typing import Union
from dataclasses import dataclass

import discord
import aiosqlite
from discord.ext import commands


@dataclass
class AutoroleData:
    all: Union[list, None]
    member: Union[list, None]
    bot: Union[list, None]


async def get_autorole_data(guild_id: int):
    async with aiosqlite.connect("database/autorole.db") as db:
        data = await db.execute("SELECT * FROM Autorole WHERE guild_id=?", (guild_id,))
        data = await data.fetchall()

    if len(data) == 0:
        return None

    all = []
    member = []
    bot = []

    for row in data:
        if row[1] is not None:
            all.append(row[1])

        if row[2] is not None:
            bot.append(row[1])

        if row[3] is not None:
            member.append(row[1])

    guild_data = AutoroleData(
        all if len(all) != 0 else None,
        member if len(member) != 0 else None,
        bot if len(bot) != 0 else None,
    )

    return guild_data


async def add_role_db(guild_id: int, autorole_type: str, roles: list[int]):
    for role in roles:
        async with aiosqlite.connect("database/autorole.db") as db:
            role_in_db = await db.execute("SELECT * FROM Autorole WHERE guild_id={} AND {}={}".format(guild_id, autorole_type, role.id))
            role_in_db = await role_in_db.fetchall()
            if len(role_in_db) == 0:
                await db.execute("INSERT INTO Autorole (guild_id, {}) VALUES ({}, {})".format(autorole_type, guild_id, role.id))

                await db.commit()

    return await get_autorole_data(guild_id)


async def remove_role_db(guild_id: int, autorole_type: str, roles: list[int]):
    for role in roles:
        async with aiosqlite.connect("database/autorole.db") as db:
            role_in_db = await db.execute("SELECT * FROM Autorole WHERE guild_id={} AND {}={}".format(guild_id, autorole_type, role.id))
            role_in_db = await role_in_db.fetchall()
            if len(role_in_db) != 0:
                await db.execute("DELETE FROM Autorole WHERE guild_id={} AND {}={}".format(autorole_type, guild_id, role.id))
            await db.commit()

    return await get_autorole_data(guild_id)


async def reset_all_db(guild_id: int):
    async with aiosqlite.connect("database/autorole.db") as db:
        await db.execute("DELETE FROM Autorole WHERE guild_id={}".format(guild_id,))


class Autorole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def autorole(self, ctx:commands.Context):
        if ctx.invoked_subcommand: return
        autorole_data = await get_autorole_data(ctx.guild.id)
        
        if autorole_data is None: return

        await ctx.send(str(autorole_data))

    @autorole.command()
    async def addroles(
        self, ctx, autorole_type: str, roles: commands.Greedy[discord.Role]
    ): 
        print(roles, ctx.guild.id, autorole_type)
        await add_role_db(ctx.guild.id, autorole_type, roles)

    @autorole.command()
    async def removeroles(
        self, ctx, autorole_type: str, roles: commands.Greedy[discord.Role]
    ):
        for role in roles:
            await remove_role_db(ctx.guild.id, autorole_type, role.id)


    @autorole.command()
    async def reset(self, ctx):
        autorole_data = await get_autorole_data()


def setup(client):
    client.add_cog(Autorole(client))
