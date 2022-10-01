import sys

from rich.text import Text
from rich.panel import Panel
from rich.console import Console


class BaseException(Exception):
    """
    Base class for other exceptions to inherit form
    """

    pass


class ConfigNotFound(BaseException):
    def __init__(self) -> None:
        # print error message
        error_message = Panel(
            Text.from_markup(
                "[yellow] Config file (config.yaml) was not found. Please run setup.py to create config files"
            ),
            title="CONFIG FILE NOT FOUND!!!",
            border_style="red",
        )
        Console().print(error_message, justify="left")
        sys.exit(1)
