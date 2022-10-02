"""
This is the main file for the bot
It contains functions to startup the bot
"""

__version__ = "2.0.0"
__author__ = "FusionSid"
__licence__ = "GPL-3.0 License"


import os
import sys
import time

from rich.progress import Progress
from rich.traceback import install

from core.models.client import WhyBot
from core.helpers.logger import log_errors, on_error
from core.utils.client_functions import get_why_config


def start_bot(client: WhyBot):
    """
    Starts up the amazing Why Bot
    """
    cogs = {}
    path = os.path.join(os.path.dirname(__file__), "cogs")

    for category in os.listdir(path):
        if not os.path.isdir(
            os.path.join(path, category)
        ):  # if its not a folder continue
            continue

        for filename in os.listdir(os.path.join(path, category)):
            if os.path.isfile(
                os.path.join(path, category, filename)
            ) and filename.endswith(".py"):
                cog_name = filename[:-3]  # remove .py from name
                cogs[cog_name] = f"cogs.{category}.{cog_name}"

    print("\n")
    client.cogs_list = cogs  # for cog functions later like reload, load, unload

    with Progress() as progress:
        loading_cogs = progress.add_task("[bold green]Loading Cogs", total=len(cogs))
        while not progress.finished:
            for cog in cogs.values():
                client.load_extension(cog)
                time.sleep(0.1)
                progress.update(
                    loading_cogs,
                    advance=1,
                    description=f"[bold green]Loaded[/] [blue]{cog}[/]",
                )
        progress.update(loading_cogs, description="[bold green]Loaded all cogs")

    time.sleep(1)

    client.event(on_error)
    client.run(client.config["BOT_TOKEN"])


if __name__ == "__main__":
    install(show_locals=True)
    sys.excepthook = log_errors

    config = get_why_config()
    client = WhyBot(config)

    # Start
    start_bot(client)
