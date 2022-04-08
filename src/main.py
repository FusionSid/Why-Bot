"""
This is the main file for the bot
It contains functions to startup the bot
"""

__version__ = "2.0.0"
__author__ = "FusionSid"
__licence__ = "GPL-3.0 License"


import os
import time
import json

from rich.progress import Progress
from dotenv import load_dotenv
from rich.traceback import install


from log import log_normal
from utils import Config, WhyBot

install()

def start_bot(client: WhyBot):
    """
    Starts up the amazing Why Bot
    """
    cogs = []

    all_categories = list(os.listdir("cogs"))
    for category in all_categories:
        for filename in os.listdir(f"cogs/{category}"):
            if filename.endswith(".py"):
                cogs.append(f"cogs.{category}.{filename[:-3]}")

    print("\n")
    client.cogs_list = cogs

    with Progress() as progress:
        loading_cogs = progress.add_task("[bold green]Loading Cogs", total=len(cogs))
        while not progress.finished:
            for cog in cogs:
                client.load_extension(cog)
                time.sleep(0.1)
                progress.update(loading_cogs, advance=1, description=f"[bold green]Loaded[/] [blue]{cog}[/]")
        progress.update(loading_cogs, description="[bold green]Loaded all cogs")

    time.sleep(1)

    client.run(os.environ["TOKEN"])


if __name__ == "__main__":
    load_dotenv()

    with open("config.json") as f:
        config = Config(json.load(f))

    client = WhyBot(config)
    client.debug_guilds = [763348615233667082]

    start_bot(client)
