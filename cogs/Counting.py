import discord
import discord
from discord.ext import commands
import json

async def get_counting_channel(guild):
    with open("./database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == guild.id:
            return int(i["counting_channel"])
    return None

# Counting


async def counting(msg, guild, channel, m):
    try:
        msg = int(msg)
    except:
        return

    cc = await get_counting_channel(guild)
    
    if cc is None:
        return
    if channel.id == cc:
        with open("./database/counting.json") as f:
            data = json.load(f)
        dataid = f'{guild.id}'
        if (data[dataid] + 1) == msg:
            data[dataid] +=1
            await m.add_reaction("✅")
        else:
            data[dataid] = 0
            await m.add_reaction("❌")
            em = discord.Embed(title="You ruined it!",
                               description="Count reset to zero")
            await channel.send(embed=em)
        with open("database/counting.json", 'w') as f:
            json.dump(data, f, indent=4)


class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_message(self, message):

        channel = message.channel
        msg = message.content
        guild = message.guild

        await counting(msg, guild, channel, message)

def setup(client):
    client.add_cog(Counting(client))