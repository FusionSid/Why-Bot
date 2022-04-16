from simpcalc import simpcalc
import discord
import aiosqlite
from discord.ext import commands

async def setup_count_db(guild_id:int):
    async with aiosqlite.connect("database/counting.db") as db:
        await db.execute("INSERT INTO ServerCounting (guild_id, current_number, last_counter, counting_channel) VALUES (?, 0, 0, 0)", (guild_id,))
        await db.commit()

async def reset_count(guild_id:int):
    async with aiosqlite.connect("database/counting.db") as db:
        await db.execute()

async def get_count_data(guild_id:int):
    async with aiosqlite.connect("database/counting.db") as db:
        data = await db.execute("SELECT * FROM ServerCounting WHERE guild_id=?", (guild_id,))
        data = data.fetchall()
    if len(data) == 0:
        return await setup_count_db(guild_id)
    return {
        "guild_id": data[0][0],
        "current_number": data[0][1],
        "last_counter": data[0][2],
        "counting_channel": data[0][3]
    }

class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.guild is None or message.author.bot:
    #         return

    #     calc = simpcalc.Calculate()
    #     channel = message.channel
        
    #     counting_data = await get_count_data(message.guild.id)
    #     if counting_data["counting_channel"] != channel.id:
    #         return

    #     try:
    #         message_content = int(message.content)
    #     except:
    #         message_content = calc.calculate(message_content)

    #     if message.author.id == counting_data["last_counter"]:
    #         await reset_count(message.guild.id)

    #     if message_content != counting_data["current_number"] + 1:
    #         await reset_count(message.guild.id)


        


def setup(client):
    client.add_cog(Counting(client))