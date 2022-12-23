import time
import inspect
import functools
from typing import Any, Optional, Callable


async def chunkify(
    big_list: list[Any], chunk_size: Optional[int] = 10
) -> list[list[Any]]:
    """
    This function splits up a list into chunks of specified size

    Parameters:
        big_list (list[Any]): The list that will be split into chunks
        chunk_size (Optional[int]): The size of each chunk. The default size is 10

    Returns:
        list[list[Any]]: A list of lists. Each sub list is a chunk.
    """
    return [big_list[i : i + chunk_size] for i in range(0, len(big_list), chunk_size)]


def functime(func: Callable, ns=False):
    @functools.wraps(func)
    async def wrapper(*args: tuple, **kwargs: dict):
        if ns:
            start = time.perf_counter_ns()
        else:
            start = time.perf_counter()

        # run function
        if inspect.iscoroutinefunction(func):
            await func(*args, **kwargs)
        else:
            func(*args, **kwargs)

        if ns:
            stop = time.perf_counter_ns()
        else:
            stop = time.perf_counter()

        print("Function Execution Time:", stop - start)

    return wrapper
