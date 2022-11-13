""" (module) log:
This is for logging errors and exceptions
"""

import os
import sys
import logging
import traceback
from datetime import datetime
from typing import Final, Optional

import aiofiles
from rich.panel import Panel
from rich.console import Console

import __main__
from core.utils.client_functions import get_why_config

rich_console = Console()

path: Final = os.path.join(os.path.dirname(__main__.__file__), "logfiles")

# check if log files dir exists
if not os.path.exists(path):
    # and if not make it
    os.makedirs(path)


# setup discord logger
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
discord_logfile_path = os.path.join(path, "discord.log")
handler = logging.FileHandler(filename=discord_logfile_path, encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter(
        "[%(levelname)s] (%(asctime)s) - %(message)s", "%d-%b-%y %H:%M:%S"
    )
)
logger.addHandler(handler)


LOGFILE_PATH: Final = os.path.join(path, "main.log")

# Custom exeption handler
def log_errors(etype, value, tb) -> None:
    """Logs errors to the file instead of terminal"""

    error = (
        f"{etype.__name__}:\n\tTraceback (most recent call"
        f" last):\n\t{'    '.join(traceback.format_tb(tb))}\n\t{value}"
    )

    # Pythons core module "logging" doesnt wanna work me very sad so me make this workaround:
    config = get_why_config()
    if config["LOGGING"]:
        with open(LOGFILE_PATH, "a") as f:
            f.write(
                f"[ERROR] ({datetime.now().strftime('%d-%b-%Y %H:%M:%S')}) - {error}\n"
            )

    rich_console.print(
        Panel(
            "Traceback (most recent call"
            f" last):\n\t{''.join(traceback.format_tb(tb))}\n{value}",
            title=etype.__name__,
            border_style="red",
        )
    )


async def log_normal(message: str) -> None:
    """
    Logs an error

    Parameters
        message (str): The message you want to log
    """
    async with aiofiles.open(LOGFILE_PATH, "a") as f:
        await f.write(
            f"[INFO] ({datetime.now().strftime('%d-%b-%Y %H:%M:%S')}) - {message}\n"
        )


async def convert_to_dict() -> dict:
    """
    Converts the log.txt file to a dict

    Returns
        dict: The log file
    """
    async with aiofiles.open(LOGFILE_PATH) as logs_data:
        logs = {}

        async for line in logs_data:
            if line.startswith("[INFO]"):
                continue
            if line.startswith("[ERROR]"):
                logs[line] = ""
                continue
            try:
                logs[(list(logs.keys())[-1])] += line
            except (IndexError, TypeError):
                break

    return logs


async def get_last_errors(count: int = 1) -> Optional[dict]:
    """
    Gets the last x amount of errors from the logs file

    Parameters
        count (Optional[int]): The amount of errors you want. (default = 1)

    Returns:
        dict: The last errors in a dictionary
    """
    logs: dict = await convert_to_dict()

    if len(logs) == 0:
        return None

    last_errors = {}

    last_keys = [list(logs.keys())[-(i + 1)] for i in range(count)]

    for key in last_keys:
        last_errors[key] = logs[key]
    return last_errors


# client.event -> on_error
async def on_error(event_method, *args, **kwargs):
    """
    This function is run when the client/bot encounters an error.
    I will overwrite the default client.on_error method with this one
    Basically it stops the bot from ignoring/printing error to terminal
    instead logs the error to main.log and prints with rich
    """
    # get error
    ex_type, ex_value, tb = sys.exc_info()
    log_errors(ex_type, ex_value, tb)
