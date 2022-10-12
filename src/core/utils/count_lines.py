""" (module) line_count
Used to get the amount of lines in the current project
"""

import os
from datetime import timedelta

from aioredis import Redis

import __main__


async def get_files() -> list[str]:
    """
    Gets a list of all the files in a python project

    Returns:
        list[str]: List of file paths for the python files in the project
    """
    file_list = []
    path = os.path.dirname(os.path.abspath(__main__.__file__))
    for root, dirs, files in os.walk(path):
        if "git" in root:
            continue

        for file in files:
            file_name = os.path.join(root, file)

            if file_name.endswith(".py"):
                file_list.append(file_name)

    return file_list


async def get_lines(redis: Redis) -> int:
    """
    Gets the amount of lines in a python project

    Parameters:
        redis (Redis): an instance of redis.Redis which is connection to the redis database
            this will be used to cache the line count to speed up performance

    Returns:
        int: The amount of lines of code in the project
    """
    if await redis.exists("python_line_count"):
        # 6ms compute time, 0.3ms get from cache time
        return int(await redis.get("python_line_count"))

    file_list = await get_files()

    lines = 0

    for file in file_list:

        with open(file) as f:
            lines += len(list(f))

    await redis.set("python_line_count", lines)
    await redis.expire("python_line_count", timedelta(hours=6))
    return lines
