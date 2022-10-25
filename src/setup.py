import os
import asyncio

import yaml
from rich.console import Console
from rich.prompt import Prompt, Confirm

from core.db.create_tables import create_tables

console = Console()

console.print(
    "[red bold]Why Bot Setup[/]\n\n[red]If this is the first time running this file"
    " make sure you type 'y' for all the prompts\nIf its not the first time and you"
    " want to edit the config just type 'n' for the fields you dont want to edit"
)

yaml_config = {
    "BOT_OWNER_ID": 0,
    "DEFAULT_PREFIX": "?",
    "BOT_CLIENT_ID": 0,
    "BOT_CLIENT_SECRET": "",
    "BOT_ID": 0,
    "MAIN_GUILD": 0,
    "LOGGING": True,
    "DEBUG_GUILD_MODE": False,
    "join_alert_channel": 0,
    "leave_alert_channel": 0,
    "online_alert_channel": 0,
    "bug_report_channel": 0,
    "suggestion_channel": 0,
    "dm_reply_channel": 0,
    "BOT_TOKEN": "",
    "DATABASE_URL": "",
    "REDIS_URI": "",
    "REDIS_PASSWORD": "",
    "HYPIXEL_API_KEY": "",
    "PRAW_CLIENT_SECRET": "",
    "PRAW_CLIENT_ID": "",
    "GOOGLE_IMAGE_API": "",
    "NASA_API_KEY": "",
    "WEATHER_API_KEY": "",
    "GENIUS_API_KEY": "",
    "YOUTUBE_API_KEY": "",
}

do_yaml = Confirm.ask(
    "[bold blue]\nWould you like to create the setup.yaml file?\nIf this is your time runnning it you should choose: y"
)

if do_yaml:
    yes_for_all = Confirm.ask(
        "[bold blue]\nWould you like to say yes for all prompts?\nIf this is your first time runnning it you should choose y"
    )
    for key in yaml_config:
        if not yes_for_all:
            do_this = Confirm.ask(
                f"[bold blue]\nWould you like to edit the value of: '{key}'"
            )
            if not do_this:
                continue
        value = Prompt.ask(f"[bold yellow]Enter the value for: '{key}'", default=None)
        yaml_config[key] = value

    path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(path, "w") as file:
        data = yaml.dump(yaml_config, file)

create_databases = Confirm.ask(
    f"[bold blue]\nCreate databases?\nYou can choose which ones specificaly by editing the list named 'tables_to_create' in core/db/create_tables.py"
)
if create_databases:
    asyncio.run(create_tables())
