""" (module) line_count

Used to get the amount of lines in the current project
"""


import os
from typing import List

async def get_files() -> List[str]:
    """
    Gets a list of all the files in a python project
    """
    file_list = []

    for root, dirs, files in os.walk("."):
        if "git" in root:
            continue

        for file in files:
            file_name = os.path.join(root,file)
            
            if file_name.endswith(".py"):
                file_list.append(file_name)

    return file_list


async def get_lines() -> int:
    """
    Gets the amount of lines in a python project
    """
    file_list = await get_files()

    lines = 0

    for file in file_list:
        file = file.lstrip("./")

        with open(file) as f:
            lines += len(list(f))

    return lines