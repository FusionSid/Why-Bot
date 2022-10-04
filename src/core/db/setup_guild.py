import asyncpg
import asyncio


async def setup_counting(db: asyncpg.Pool, guild_id: int):
    try:
        await db.execute(
            "INSERT INTO counting (guild_id, high_score) VALUES ($1, 0)", guild_id
        )
    except asyncpg.UniqueViolationError:
        return


async def create_tables(db: asyncpg.Pool, guild_id: int):
    things_to_setup = [setup_counting]
    tasks = [setup_function(db, guild_id) for setup_function in things_to_setup]
    await asyncio.gather(*tasks)
