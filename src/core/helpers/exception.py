import sys

from rich.text import Text
from rich.panel import Panel
from rich.console import Console


class BaseException(Exception):
    """
    Base class for other exceptions to inherit form
    """

    def __init__(self, title: str, message: str) -> None:
        error_message = Panel(
            Text.from_markup(f"[yellow]{message}"),
            title=title,
            border_style="red",
        )
        Console().print(error_message, justify="left")
        sys.exit(1)


class ConfigNotFound(BaseException):
    def __init__(self) -> None:
        super().__init__(
            "CONFIG FILE NOT FOUND!!!",
            "Config file (config.yaml) was not found.\nPlease run setup.py to create config files",
        )


class InvalidDatabaseUrl(BaseException):
    def __init__(self) -> None:
        super().__init__(
            "INVALID DATABASE URL!!!",
            "Invalid postgresql connection string was provided.\nPlease provide the correct string in config",
        )
