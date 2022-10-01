import asyncio
import aioredis
from datetime import timedelta


async def main():
    redis = aioredis.from_url("", decode_responses=True, password="", port=6379)

    name = await redis.get("name")
    if name is None:
        name = input("What is your name? ")
        await redis.set("name", name)
        await redis.expire("name", timedelta(minutes=1))
        return print("Hello", name)
    print("Hello", name)


if __name__ == "__main__":
    asyncio.run(main())
