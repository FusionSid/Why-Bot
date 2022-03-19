"""
I will delete this file (or put in another folder) once I finish the bot and host it
"""

import asyncio

import aiosqlite

from log import log_errors

async def main():
    async with aiosqlite.connect("database/prefix.db") as db:
        await db.execute("""CREATE TABLE Prefix (
            guild_id INTEGER PRIMARY KEY NOT NULL, 
            prefix TEXT NOT NULL
            )""")


asyncio.new_event_loop().run_until_complete(main())