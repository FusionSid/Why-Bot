import asyncpg
import asyncio


async def setup_counting(db: asyncpg.Pool, guild_id: int):
    try:
        await db.execute("INSERT INTO counting (guild_id) VALUES ($1)", guild_id)
    except asyncpg.UniqueViolationError:
        print("Bruhh this should be running")


async def create_tables(db: asyncpg.Pool, guild_id: int):
    things_to_setup = [setup_counting]
    tasks = [setup_function(db, guild_id) for setup_function in things_to_setup]
    await asyncio.gather(*tasks)
