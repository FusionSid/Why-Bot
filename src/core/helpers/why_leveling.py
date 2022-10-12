import discord
import asyncpg

from core.models.level import LevelingDataGuild, LevelingDataMember


async def xp_needed(level: int):
    x, y = 0.125, 2
    return int((level / x) ** y)


async def get_level_data(db: asyncpg.Pool, guild_id: int) -> LevelingDataGuild | None:
    data = await db.fetch("SELECT * FROM leveling_guild WHERE guild_id=$1", guild_id)
    if not len(data):
        return None

    return LevelingDataGuild(*data[0])


async def get_member_data(db: asyncpg.Pool, member: discord.Member, guild_id: int):
    data = await db.fetch(
        "SELECT * FROM leveling_member WHERE member_id=$1 AND guild_id=$2",
        member.id,
        guild_id,
    )

    if not len(data):
        default_data = [
            guild_id,
            member.id,
            f"{member.name}#{member.discriminator}",
            0,
            0,
            0,
        ]
        await db.execute(
            "INSERT INTO leveling_member (guild_id, member_id, member_name, member_xp, member_level, member_total_xp) VALUES ($1, $2, $3, $4, $5, $6)",
            *default_data,
        )
        return LevelingDataMember(*default_data)

    return LevelingDataMember(*data[0])


async def update_member_data(
    db: asyncpg.Pool, message: discord.Message, member_data: LevelingDataMember
):
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
    print(member_data)


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
