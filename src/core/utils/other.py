async def chunkify(big_list: int, chunk_size: int) -> list:
    return [big_list[i : i + chunk_size] for i in range(0, len(big_list), chunk_size)]
