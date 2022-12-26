from typing import Final, Optional

import discord
import asyncpg

from core.models.level import LevelingDataGuild, LevelingDataMember


def xp_needed(level: int) -> int:
    """
    Calculate the xp needed for any level

    Parameters:
        level (int): The level to calculate xp needed

    Returns:
        int: The amount of xp to reach the level provided
    """

    x, y = 0.125, 2
    return int((level / x) ** y)


async def get_level_data(
    db: asyncpg.Pool, guild_id: int
) -> Optional[LevelingDataGuild]:
    """
    This function gets the leveling data for a guild

    Parameters:
        db (asyncpg.Pool): the connection pool to the database. This is found in client.db.
        guild_id (int): The guild id of the guild to get leveling data for

    Returns:
        Optional[LevelingDataGuild]: If data for the guild is not found it returns None else
            it returns a LevelingDataGuild object with the data in it
    """

    data = await db.fetch("SELECT * FROM leveling_guild WHERE guild_id=$1", guild_id)
    if not data:
        return None

    return LevelingDataGuild(*data[0])


async def get_member_data(
    db: asyncpg.Pool, member: discord.Member, guild_id: int
) -> LevelingDataMember:
    """
    This function gets the leveling data for a single member

    Parameters:
        db (asyncpg.Pool): the connection pool to the database. This is found in client.db.
        member (discord.Member): The member to get the data for
        guild_id (int): The guild where to get the data for as members can be in multiple
            guilds with different leveling data

    Returns:
        LevelingDataMember: it returns a LevelingDataMember object with the mmeber's data in it
    """

    data = await db.fetch(
        "SELECT * FROM leveling_member WHERE member_id=$1 AND guild_id=$2",
        member.id,
        guild_id,
    )

    if not data:
        DEFAULT_MEMBER_DATA: Final[int] = [
            guild_id,
            member.id,
            f"{member.name}#{member.discriminator}",
            0,
            0,
            0,
        ]
        await db.execute(
            "INSERT INTO leveling_member (guild_id, member_id, member_name, member_xp,"
            " member_level, member_total_xp) VALUES ($1, $2, $3, $4, $5, $6)",
            *DEFAULT_MEMBER_DATA,
        )
        return LevelingDataMember(*DEFAULT_MEMBER_DATA)

    return LevelingDataMember(*data[0])


async def update_member_data(
    db: asyncpg.Pool, message: discord.Message, member_data: LevelingDataMember
) -> None:
    """
    Updates the data for a member

    Parameters:
        db (asyncpg.Pool): the connection pool to the database. This is found in client.db.
        message (discord.Message): The message that was sent. This is used to get things
            like guild id and extra info
        member_data (LevelingDataMember): The object with the new data
    """

    member = message.author
    await db.execute(
        """UPDATE leveling_member
        SET member_name=$1, member_xp=$2, member_level=$3, member_total_xp=$4
        WHERE member_id=$5 AND guild_id=$6
        """,
        f"{member.name}#{member.discriminator}",
        member_data.member_xp,
        member_data.member_level,
        member_data.member_total_xp,
        message.author.id,
        message.guild.id,
    )


async def get_all_member_data(db: asyncpg.Pool, guild_id: int):
    """
    Gets member data for all the members in a guild. This is used for leaderboards

    Parameters:
        db (asyncpg.Pool)
    """

    data = await db.fetch(
        "SELECT * FROM leveling_member WHERE guild_id=$1 ORDER BY member_total_xp",
        guild_id,
    )

    return data[::-1]
