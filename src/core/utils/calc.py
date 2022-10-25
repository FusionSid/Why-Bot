""" (module) calc
Used to calculate an expression using the mathjs api
"""

import urllib

import aiohttp
import numexpr


async def slow_safe_calculate(expr: str, only_int: bool = False) -> int | str | None:
    """
    Calculates a math expression using the mathjs API

    Parameters:
        expr (str): The expression to evaluate
        only_int (Optional[bool]): If this is True it will return the result only if its int
            if its not an int it will return None. (By default this option is False)

    Returns:
        int | str | None: It will return int if the result is already numeric or the result is int
            it will return str if the result is something like a float
            it will reutrn None if only_int is True and the result is not int
    """
    if expr.isnumeric():
        return int(expr)

    expression = urllib.parse.quote(expr.replace("**", "^"))
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.mathjs.org/v4/?expr={expression}") as r:
            result = await r.text()

    if only_int and result.isnumeric() == False:
        return None

    if only_int:
        return int(result)

    return result


async def calculate(expr: str) -> float | None:
    """
    Evaluates a math expression with numexpr

    Parameters:
        expr (str): the expression to evaluate

    Returns:
        Optional[float[]: It will return the result of the expression and if it
            fails then it will return None
    """
    try:
        result = numexpr.evaluate(expr)
    except (
        OverflowError,
        AttributeError,
        SyntaxError,
        ZeroDivisionError,
        KeyError,
        ValueError,
    ):
        return None

    return result
