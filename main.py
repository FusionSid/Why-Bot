import json
import os
from os import listdir
from os.path import isfile, join
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from embed_gen import keep_alive
import dotenv
from discord.ui import Button, View
from datetime import datetime
from utils.other import log

dotenv.load_dotenv()


async def get_prefix(client, message):
    try:
        with open('database/db.json') as f:
            data = json.load(f)
        for i in data:
            if i['guild_id'] == message.guild.id:
                return i['prefix']
    except:
        return "?"


intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None, owner_id=624076054969188363)


async def update_activity():
    await client.change_presence(activity=discord.Game(f"On {len(client.guilds)} servers! | ?help"))
    print("Updated presence")


# On ready
@client.event
async def on_ready():
    print("=======================\nConnected\n=========")
    await update_activity()
    channel = client.get_channel(925513395883606129)
    await channel.send("Online")


# Blacklist system
async def notblacklisted(message):
    with open("database/blacklisted.json") as f:
        blacklisted = json.load(f)  # Check if blacklisted
    for user in blacklisted:
        if message.author.id == user:
            return False
    return True  # If notblacklisted return true else return false


async def update_user_db(user):
    with open("database/userdb.json") as f:
        data = json.load(f)
    found = False
    for i in data:
        if i['user_id'] == user:
            found = True
            i["command_count"] = i["command_count"] + 1
    if found == False:
        user_data = {
            "user_id": user,
            "command_count": 1,
            "settings": {},
            "on_pinged": {"title": None, "description": None, "color": None}
        }
        data.append(user_data)
    with open("database/userdb.json", 'w') as f:
        json.dump(data, f, indent=4)

# On Message


@client.event
async def on_message(message):
    if message.author == client.user:
        return  # if bot - no

    if isinstance(message.channel, discord.DMChannel):
        cha = await client.fetch_channel(926232260166975508)
        em = discord.Embed(
            title="New DM", description=f"From {message.author.name}")
        em.add_field(name="Content", value=f"{message.content}")
        msg = await cha.send(content=f"{message.author.id}", embed=em)

    # Fome variables that come in useful later
    channel = message.channel
    msg = message.content
    guild = message.guild

    # if blacklisted dont let them use bot
    try:
        notbl = await notblacklisted(message)
        if notbl == True:
            prefix = await get_prefix(client, message)
            if prefix in message.content:
                await update_user_db(message.author.id)
            await client.process_commands(message)
    except:
        await client.process_commands(message)


@tasks.loop(hours=1)
async def post_logs():
    file = discord.File("./other/log.txt")
    cha = await client.fetch_channel(896932591620464690)
    await cha.send(file=file)

    dir = './tempstorage/'
    for f in os.listdir(dir):
      os.remove(os.path.join(dir, f))
 


def start_bot(client):

    client.remove_command("help")
    keep_alive()
    lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
    no_py = [s.replace('.py', '') for s in lst]
    startup_extensions = ["cogs." + no_py for no_py in no_py]
    try:
        for cogs in startup_extensions:
            client.load_extension(cogs)  # Startup all cogs

            print(f"Loaded {cogs}")

        print("\nAll Cogs Loaded\n===============\nLogging into Discord...")

        post_logs.start()
        client.run(os.environ['TOKEN'])

    except Exception as e:
        print(
            f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")
        log(
            f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")


if __name__ == '__main__':
    start_bot(client)
