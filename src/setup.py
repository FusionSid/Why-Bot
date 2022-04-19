import json
import sys
import asyncio

import aiosqlite
from rich.prompt import Prompt
from rich.console import Console
from discordLevelingSystem import DiscordLevelingSystem

console = Console()

dm_reply_channel = Prompt.ask("Enter the ID for the dm_reply_channel", default=None)
dm_reply_channel = (int(dm_reply_channel) if dm_reply_channel is not None else dm_reply_channel)

suggestion_channel = Prompt.ask("Enter the ID for the suggestion_channel", default=None)
suggestion_channel = (int(suggestion_channel) if suggestion_channel is not None else suggestion_channel)

join_alert_channel = Prompt.ask("Enter the ID for the join_alert_channel", default=None)
join_alert_channel = (int(join_alert_channel) if join_alert_channel is not None else join_alert_channel)

leave_alert_channel = Prompt.ask("Enter the ID for the leave_alert_channel", default=None)
leave_alert_channel = (int(leave_alert_channel) if leave_alert_channel is not None else leave_alert_channel)

bug_report_channel = Prompt.ask("Enter the ID for the bug_report_channel", default=None)
bug_report_channel = (int(bug_report_channel) if bug_report_channel is not None else bug_report_channel)

online_alert_channel = Prompt.ask("Enter the ID for the online_alert_channel", default=None)
online_alert_channel = (int(online_alert_channel) if online_alert_channel is not None else online_alert_channel)


config = {
    "dm_reply_channel": dm_reply_channel,
    "join_alert_channel": join_alert_channel,
    "leave_alert_channel": leave_alert_channel,
    "online_alert_channel": online_alert_channel,
    "bug_report_channel": bug_report_channel,
    "suggestion_channel": suggestion_channel
}


with open("config.json", "w") as f:
    json.dump(config, f, indent=4)

DiscordLevelingSystem.create_database_file("database")
console.print("[blue]Created leveling db")    

async def main():
    async with aiosqlite.connect("database/main.db") as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS Prefix (
            guild_id INTEGER PRIMARY KEY NOT NULL, 
            prefix TEXT NOT NULL
            )"""
        )
        await db.commit()
        console.print("[blue]Created Prefix Db")
        await db.execute(
            """CREATE TABLE IF NOT EXISTS Warnings (
                guild_id INTEGER,
                member_id INTEGER, 
                time INTEGER,
                reason TEXT
                )"""
        )
        await db.commit()
        console.print("[blue]Created Warnings Db")
        await db.execute(
            """CREATE TABLE IF NOT EXISTS ServerCounting (
                guild_id INTEGER,
                current_number INTEGER, 
                last_counter INTEGER,
                counting_channel INTEGER
                )"""
        )
        await db.commit()
        console.print("[blue]Created ServerCounting Db")
        return console.print("[green]finished main.db")

asyncio.run(main())


data = []
with open("database/dm_banned.json", "w") as f:
    json.dump(data, f, indent=4)
    console.print("[blue]Created dm_banned json file")

with open("database/blacklisted.json", "w") as f:
    json.dump(data, f, indent=4)
    console.print("[blue]Created blacklisted json file")

token = Prompt.ask("Enter the bot token")
with open("../.env", 'w') as f:
    f.write(f"TOKEN = {token}")

console.print("[green]Setup complete :) Use ^C to exit")