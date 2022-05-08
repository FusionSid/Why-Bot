import json
import sys
import asyncio

import aiosqlite
from rich.prompt import Prompt, Confirm
from rich.console import Console
from discordLevelingSystem import DiscordLevelingSystem

console = Console()

console.print("[red bold]Why Bot Setup[/]\n\n[red]If this is the first time running this file make sure you type 'y' for all the prompts\nIf its not the first time and you want to edit the config just type 'n' for the fields you dont want to edit\nEg if you just wanted to recreate the leveling db just type 'n' for all the other prompts")

cfgjs = Confirm.ask("[bold blue]\nCreate config.json?")
if cfgjs:
    dm_reply_channel = Prompt.ask("[bold yellow]Enter the ID for the dm_reply_channel", default=None)
    dm_reply_channel = (int(dm_reply_channel) if dm_reply_channel is not None else dm_reply_channel)

    suggestion_channel = Prompt.ask("[bold yellow]Enter the ID for the suggestion_channel", default=None)
    suggestion_channel = (int(suggestion_channel) if suggestion_channel is not None else suggestion_channel)

    join_alert_channel = Prompt.ask("[bold yellow]Enter the ID for the join_alert_channel", default=None)
    join_alert_channel = (int(join_alert_channel) if join_alert_channel is not None else join_alert_channel)

    leave_alert_channel = Prompt.ask("[bold yellow]Enter the ID for the leave_alert_channel", default=None)
    leave_alert_channel = (int(leave_alert_channel) if leave_alert_channel is not None else leave_alert_channel)

    bug_report_channel = Prompt.ask("[bold yellow]Enter the ID for the bug_report_channel", default=None)
    bug_report_channel = (int(bug_report_channel) if bug_report_channel is not None else bug_report_channel)

    online_alert_channel = Prompt.ask("[bold yellow]Enter the ID for the online_alert_channel", default=None)
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


    console.print("[bold green]Config.json created!")


lvldb = Confirm.ask("[bold blue]\nCreate leveling db?")
if lvldb:
    DiscordLevelingSystem.create_database_file("database")
    console.print("[bold green]Leveling db created!")    

async def main():
    async with aiosqlite.connect("database/main.db") as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS Prefix (
            guild_id INTEGER PRIMARY KEY NOT NULL, 
            prefix TEXT NOT NULL
            )"""
        )
        await db.commit()
        console.print("[green]Created Prefix Db")

        await db.execute(
            """CREATE TABLE IF NOT EXISTS Warnings (
                guild_id INTEGER,
                member_id INTEGER, 
                time INTEGER,
                reason TEXT
                )"""
        )
        await db.commit()
        console.print("[green]Created Warnings Db")

        await db.execute(
            """CREATE TABLE IF NOT EXISTS ServerCounting (
                guild_id INTEGER,
                current_number INTEGER, 
                last_counter INTEGER,
                counting_channel INTEGER
                )"""
        )
        console.print("[green]Created ServerCounting Db")

        await db.execute(
            """CREATE TABLE IF NOT EXISTS LoggingSettings (
                guild_id INTEGER,
                log_channel INTEGER,

                message_edits INTEGER,
                message_delete INTEGER,

                member_ban INTEGER,
                member_kick INTEGER,
                member_unban INTEGER,
                member_nick_change INTEGER,
                member_roles_add_remove INTEGER,
                member_join_leave INTEGER,

                channel_create_remove INTEGER,
                channel_update INTEGER,

                voice_create_remove INTEGER,
                voice_update INTEGER,
                
                thread_create_remove INTEGER,

                invite_create INTEGER
            )"""
        )
        console.print("[green]Created logging Db")
        await db.commit()

        return console.print("[bold green]\nFinished main.db!")


maindb = Confirm.ask("[bold blue]\nCreate main.db?")
if maindb:
    asyncio.run(main())


ban = Confirm.ask("[bold blue]\nCreate db_banned.json and blacklisted.json?")
if ban:
    data = []
    with open("database/dm_banned.json", "w") as f:
        json.dump(data, f, indent=4)
        console.print("[green]Created dm_banned json file")

    with open("database/blacklisted.json", "w") as f:
        json.dump(data, f, indent=4)
        console.print("[green]Created blacklisted json file")
    
    console.print("[bold green]\nFinished db_banned.json and blacklisted.json")


env = Confirm.ask("[bold blue]\nCreate .env?")
if env:
    token = Prompt.ask("Enter the bot token")
    with open("../.env", 'w') as f:
        f.write(f"TOKEN = {token}")

console.print("[bold green]\nSetup complete :)[/]\n[magenta]Use ^C to exit")
