""" (module) log:

This is for logging errors and exceptions
Importing the log_errors function will make all errors go to the file instead of terminal
I have added the option to print to terminal
"""

import sys
import logging
import traceback

from rich.panel import Panel
from rich.console import Console

rich_console = Console()


logging.basicConfig(
    filename="log/logs.txt",
    format="[%(levelname)s] (%(asctime)s) - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


def log_errors(etype, value, tb):
    """Logs errors to the file instead of terminal"""

    error = f"{etype.__name__}:\n\tTraceback (most recent call last):\n\t{'    '.join(traceback.format_tb(tb))}\n\t{value}"
    logging.error(error)

    # Commenting out this line will stop errors being printed to console
    # sys.__excepthook__(etype, value, tb)
    
    rich_console.print(
        Panel(
            f"Traceback (most recent call last):\n\t{''.join(traceback.format_tb(tb))}\n{value}",
            title=etype.__name__,
            border_style="red",
        )
    )


sys.excepthook = log_errors


async def log_normal(message: str):
    """
    Logs an error

    Parameters
        :param: message (str): The message you want to log
    """
    logging.info(message)


async def convert_to_dict() -> dict:
    """
    Converts the log.txt file to a dict

    Returns
        Dict: The log file
    """
    with open("log/logs.txt") as logs_data:
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
        :param: count (int): The amount of errors you want, defaults to 1
    """
    logs: dict = await convert_to_dict()

    if len(logs) == 0:
        return None

    last_errors = {}

    last_keys = [list(logs.keys())[-(i + 1)] for i in range(count)]

    for key in last_keys:
        last_errors[key] = logs[key]

    return last_errors
