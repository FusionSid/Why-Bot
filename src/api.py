from fastapi import FastAPI, APIRouter
import aiosqlite


class WhyAPI(FastAPI):
    """
    WhyAPI
    """

    def __init__(self) -> None:
        super().__init__()
        # Docs config
        self.title = "Why-Bot API"
        self.description = "### API for why bot lmao"
        self.license_info = {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        }

app = WhyAPI()

@app.get("/api/get-prefix")
async def get_prefix(guild_id:int):
    async with aiosqlite.connect("database/main.db") as db:
        cur = await db.execute("SELECT * FROM Prefix WHERE guild_id=?", (guild_id,))
        prefix = await cur.fetchall()

        if len(prefix) == 0:
            prefix = "?"
            await db.execute("INSERT INTO Prefix (guild_id, prefix) VALUES (?, ?)", (guild_id, prefix))
            await db.commit()
        else:
            prefix = prefix[0][1]
    
    return {
        "prefix": prefix
    }