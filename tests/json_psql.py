import asyncio
import json
import asyncpg


async def main():
    async def init(conn):
        await conn.set_type_codec(
            "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
        )

    pool = await asyncpg.create_pool(
        dsn="postgresql://168.138.102.186/testing?user=sid&password=pM153D^kyiJ6",
        init=init,
    )

    # await pool.execute("DROP TABLE testjson;CREATE TABLE TESTJSON (name TEXT PRIMARY KEY, json_data json)")

    # await conn.execute("INSERT INTO testjson (name, json_data) VALUES ($1, $2)", "Siddhesh", json.dumps({"e": [1, 2, "3"], 'f':"235"}))
    data = await pool.fetch("SELECT * FROM testjson")
    print(data[0][1]["e"])


asyncio.new_event_loop().run_until_complete(main())
