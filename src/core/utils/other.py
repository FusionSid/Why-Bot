from typing import Any


async def chunkify(big_list: int, chunk_size: int = 10) -> list[list[Any]]:
    """
    This function splits up a list into chunks of specified size

    Parameters:
        big_list (int): The list that will be split into chunks
        chunk_size (Optional[int]): The size of each chunk. The default size is 10

    Returns:
        list[list[Any]]: A list of lists. Each sub list is a chunk.
    """
    return [big_list[i : i + chunk_size] for i in range(0, len(big_list), chunk_size)]