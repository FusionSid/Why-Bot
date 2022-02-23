import asyncio
import aiosqlite

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def convertToImage(binary_data):
    with open("image.png", 'wb') as file:
        file.write(binary_data)

async def insert_into_db(id, time, name, desc = None, image = None):
    async with aiosqlite.connect("todo.db") as db:
        if desc is None:
            sqlite_insert_query = """INSERT INTO "123" (id, time, name, image) VALUES (?, ?, ?, ?)"""
        elif image is None:
            sqlite_insert_query = """INSERT INTO "123" (id, time, name, desc) VALUES (?, ?, ?, ?)"""
        elif image is None and desc is None:
            sqlite_insert_query = """INSERT INTO "123" (id, time, name) VALUES (?, ?, ?)"""
        else:
            sqlite_insert_query = """INSERT INTO "123" (id, time, name, desc, image) VALUES (?, ?, ?, ?, ?)"""
        
        photo = await convertToBinaryData(photo)
        data_tuple = (id, time, name, desc, image)
        await db.execute(sqlite_insert_query, data_tuple)
        await db.commit()
    

async def main():
    async with aiosqlite.connect("todo.db") as db:
        await db.execute("""CREATE TABLE "123" (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            time TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            image BLOB,
            );""")
        await db.commit()

loop = asyncio.new_event_loop()
loop.create_task(main())
loop.run_forever()

