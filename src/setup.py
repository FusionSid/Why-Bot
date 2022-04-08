import json


dm_reply_channel = int(input("Enter the ID for the dm_reply_channel"))
join_alert_channel = int(input("Enter the ID for the join_alert_channel"))
leave_alert_channel = int(input("Enter the ID for the leave_alert_channel"))
online_alert_channel = int(input("Enter the ID for the online_alert_channel"))


config = {
    "dm_reply_channel": dm_reply_channel,
    "join_alert_channel": join_alert_channel,
    "leave_alert_channel": leave_alert_channel,
    "online_alert_channel": online_alert_channel,
}


with open("config.json", "w") as f:
    json.dump(config, f, indent=4)


print("Setup Complete :)")

# Create prefix database
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
