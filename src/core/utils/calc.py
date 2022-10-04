""" (module) calc
Used to calculate an expression using the mathjs api
"""

import urllib

import aiohttp


async def calculate(expr: str, only_int: bool = False) -> str | int | None:
    expression = urllib.parse.quote(expr.replace("**", "^"))
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.mathjs.org/v4/?expr={expression}") as r:
            result = await r.text()

    if only_int and result.isnumeric() == False:
        return None

    if only_int:
        return int(result)

    return result
