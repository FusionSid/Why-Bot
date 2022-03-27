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

from dotenv import load_dotenv

from log import log_normal
from utils import Config, WhyBot, loading_bar


def start_bot(client : WhyBot):
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
    for index, cog in enumerate(cogs):
        client.cogs_list = cogs
        client.load_extension(cog)
        loading_bar(len(cogs), index, "Loading Cogs:", "Loaded All Cogs ✅")
        time.sleep(1)


    time.sleep(1)

    client.run(os.environ["TOKEN"])


if __name__ == "__main__":
    load_dotenv()

    with open("config.json") as f:
        config = Config(json.load(f))

    client = WhyBot(config)
    client.debug_guilds=[763348615233667082]

    start_bot(client)