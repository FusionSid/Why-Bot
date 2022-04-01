"""
I will delete this file (or put in another folder) once I finish the bot and host it
"""

import asyncio

import aiosqlite


async def main():
    async with aiosqlite.connect("database/prefix.db") as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS Prefix (
            guild_id INTEGER PRIMARY KEY NOT NULL, 
            prefix TEXT NOT NULL
            )"""
        )
        await db.commit()

asyncio.new_event_loop().run_until_complete(main())
