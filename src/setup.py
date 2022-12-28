import re
import os
import sys
import asyncio
import subprocess
from typing import Callable

import yaml
from rich.console import Console
from rich.prompt import Prompt, Confirm

from core.db import create_tables


console = Console()
PATH = os.path.dirname(__file__)


def clear():
    subprocess.call("clear" if os.name == "posix" else "cls")


def install_requirements() -> None:
    """Install the required libraries from requirements.txt"""

    console.print("[bold blue]Requirements:")
    section_text = [
        "In this section the script will ask you to install requirements",
        "It is recomended that you use a virtual env when installing them but this is not required",
        "Saying 'y' to the next prompt will install all the packages in src/requirements.txt",
    ]
    for text in section_text:
        console.print(f"[blue]{text}")

    if Confirm.ask("[bold blue]\nWould you like to install requirements?"):
        requirements_path = os.path.join(PATH, "requirements.txt")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", requirements_path]
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print("[red bold]Failed to install requirements D:[/]")

    clear()


def create_db_tables() -> None:
    """Create the database tables"""

    console.print("[bold blue]Database Tables:")
    var_path = os.path.join(PATH, "core/db/create_tables.py")
    section_text = [
        "In this section the script will ask you to create the db tables",
        "Make sure you have already put the PostgreSQL database url in your config.yaml file",
        "By default the script will create all the tables. If the table exists it will DELETE it and remake it",
        "If you don't want that to happen or just want to make a specific table please edit TABLES_TO_CREATE",
        f'TABLES_TO_CREATE is located at: "{var_path}", line 152',
    ]
    for text in section_text:
        console.print(f"[blue]{text}")

    if Confirm.ask(
        "[bold blue]\nWould you like to create the tables in TABLES_TO_CREATE?"
    ):
        asyncio.run(create_tables())

    clear()


def create_config_file() -> None:
    """Create the config.yaml file"""

    console.print("[bold blue]Config File:")
    selfhost_path = os.path.join(PATH, "..", "docs/SELFHOSTING.md")
    section_text = [
        "In this section the script will ask you to create the config.yaml file",
        "There will be a series of prompts asking for the data needed.",
        f"If you are not sure how to get the values or keys for a prompt read the selfhosting guide: {selfhost_path}",
        "Also not that answering 'y' to the next prompt will overwrite the current config.yaml if there is one",
        "So if you don't want that happening and just want to edit one value modify it directly in the file",
    ]
    for text in section_text:
        console.print(f"[blue]{text}")

    create_file = Confirm.ask(
        "[bold blue]\nWould you like to create the config.yaml file?"
    )
    if not create_file:
        return clear()

    config_path = os.path.join(PATH, "config.example.yaml")

    with open(config_path, "r") as f:
        data: dict = yaml.load(f, Loader=yaml.SafeLoader)

    new_config_file_data = {key: None for key in data}

    for key, val in data.items():
        value = None

        if type(val) == str:
            value = Prompt.ask(
                f"[bold yellow]Enter the value for '{key}' (type=string)",
                default=None,
            )
        elif type(val) == int:
            value = Prompt.ask(
                f"[bold yellow]Enter the value for '{key}' (type=integer)",
                default=None,
            )
            value = int(value) if value is not None and value.isnumeric() else 0
        elif type(val) == bool:
            value = Prompt.ask(
                f"[bold yellow]Enter the value for '{key}' (type=list)",
                choices=["true", "false"],
                default="false",
            )
            value = True if value.lower() == "true" else False
        elif type(val) == list:
            console.print(
                "[bold yellow]Enter each item sperated by a comma or space eg: 123, 42 123"
            )
            value = Prompt.ask(
                f"[bold yellow]Enter the value for '{key}' (type=list)",
                default=None,
            )
            value = (
                [int(x) for x in re.findall("\\d+", value) if x.isnumeric()]
                if value is not None
                else []
            )

        if value is not None:
            new_config_file_data[key] = value

        clear()

    with open(os.path.join(PATH, "config.aml"), "w") as f:
        yaml.dump(new_config_file_data, f)

    clear()


def is_first_time() -> bool:
    """Ask user if its their first time"""

    console.print("[red bold]Why Bot Setup\n")

    section_text = [
        "Welcome to the why bot setup script",
        "Please make sure you have the prerequisites that are found in the README",
        "Also if this is your first time running the script please answer 'y' to most of the prompts",
    ]
    for text in section_text:
        console.print(f"[red]{text}")

    is_first_time = Confirm.ask(
        "[bold red]\nIs this your first time running this script?"
    )
    clear()
    return is_first_time


def first_time() -> None:
    install_requirements()
    create_config_file()
    create_db_tables()


def main() -> None:
    if is_first_time():
        return first_time()

    options: dict[str, list[str | Callable[[], None]]] = {
        "req": ["Goes to the install requirements section", install_requirements],
        "cfg": ["Goes to the create new config file section", create_config_file],
        "dbt": ["Goes to the create db tables section", create_db_tables],
        "exit": ["Exits the script"],
    }
    while True:
        console.print("[b u green]Options:")
        for key, value in options.items():
            console.print(f"[b green]{key}:[/] [green]{value[0]}")
        option = options.get(Prompt.ask("[b green]What would you like to do?"), None)
        if option is None:
            clear()
            continue
        if len(option) == 1:
            break

        option[1]()


if __name__ == "__main__":
    clear()
    main()
