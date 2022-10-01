""" (module) log:

This is for logging errors and exceptions
Importing the log_errors function will make all errors go to the file instead of terminal
I have added the option to print to terminal
"""
import os
import sys
import logging
import traceback
from datetime import datetime

from rich.panel import Panel
from rich.console import Console

rich_console = Console()
logfile_path = os.path.join(os.path.dirname(__file__), "main.log")

# setup discord logger
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
discord_logfile_path = os.path.join(os.path.dirname(__file__), "discord.log")
handler = logging.FileHandler(filename=discord_logfile_path, encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter(
        "[%(levelname)s] (%(asctime)s) - %(message)s", "%d-%b-%y %H:%M:%S"
    )
)
logger.addHandler(handler)

# Custom exeption handler
def log_errors(etype, value, tb):
    """Logs errors to the file instead of terminal"""

    error = f"{etype.__name__}:\n\tTraceback (most recent call last):\n\t{'    '.join(traceback.format_tb(tb))}\n\t{value}"

    # Pythons core module "logging" doesnt wanna work me very sad so me make this workaround:
    with open(logfile_path, "a") as f:
        f.write(f"[ERROR] ({datetime.now().strftime('%d-%b-%Y %H:%M:%S')}) - {error}\n")

    # sys.__excepthook__(etype, value, tb)

    rich_console.print(
        Panel(
            f"Traceback (most recent call last):\n\t{''.join(traceback.format_tb(tb))}\n{value}",
            title=etype.__name__,
            border_style="red",
        )
    )


async def log_normal(message: str):
    """
    Logs an error

    Parameters
        message (str): The message you want to log
    """
    with open(logfile_path, "a") as f:
        f.write(
            f"[INFO] ({datetime.now().strftime('%d-%b-%Y %H:%M:%S')}) - {message}\n"
        )


async def convert_to_dict() -> dict:
    """
    Converts the log.txt file to a dict

    Returns
        dict: The log file
    """
    with open(logfile_path) as logs_data:
        logs = {}

        for line in logs_data:
            if line.startswith("[ERROR]"):
                logs[line] = ""
            else:
                logs[(list(logs.keys())[-1])] += line

    return logs


async def get_last_errors(count: int = 1):
    """
    Gets the last x amount of errors from the logs file

    Parameters
        count (int): The amount of errors you want, defaults to 1

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


# event
async def on_error(event_method, *args, **kwargs):
    # get error
    ex_type, ex_value, tb = sys.exc_info()
    log_errors(ex_type, ex_value, tb)
