import json
import traceback
import time
import datetime
import os
from os import listdir
from os.path import isfile, isdir
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import dotenv
from discord.ui import Button, View
from utils import Log
import pyfiglet
import sidspackage

dotenv.load_dotenv()

log = Log("./database/log.txt", timestamp=True)

async def get_prefix(client, message):
    try:
        data = await client.get_db()
        return data[str(message.guild.id)]['prefix']
    except Exception as err:
        print(err)
        return "?"


intents = discord.Intents.all()
allowed_mentions = discord.AllowedMentions(everyone=False)

class WhyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix, intents=intents, help_command=None, owner_id=624076054969188363, case_insensitive=True,allowed_mentions=allowed_mentions, debug_guilds=[763348615233667082])
        
        self.cp = sidspackage.ColorPrint()
        
        self.art = pyfiglet.figlet_format("Why Bot")
        self.cp.print(self.art, color="blue")

        self.cogs_list = None
        self.last_login_time = None

    async def get_db(self):
        with open("database/db.json") as f:
            data = json.load(f)
        return data


    async def update_db(self, data):
        with open("database/db.json", 'w') as f:
            json.dump(data, f, indent=4)


    @property
    async def uptime(self):
        time_right_now = datetime.datetime.now()
        seconds = int((time_right_now - self.last_login_time).total_seconds())
        time = f"{seconds}s"
        if seconds > 60:
            minutes = seconds - (seconds % 60)
            seconds = seconds - minutes
            minutes = int(minutes / 60)
            time = f"{minutes}min {seconds}s"
            if minutes > 60:
                hoursglad = minutes - (minutes % 60)
                hours = int(hoursglad / 60)
                minutes = minutes - (hours*60)
                time = f"{hours}h {minutes}min {seconds}s"
        return time


client = WhyBot()

def print_percent_done(index, total, bar_len=50, title='Loading Cogs:'):
    percent_done = (index+1)/total*100
    percent_done = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    print(f'{title} [{done_str}{togo_str}] {percent_done}% done', end='\r')

    if round(percent_done) == 100:
        print('Loaded All: ✅ ')

async def update_activity():
    await client.change_presence(activity=discord.Game(f"On {len(client.guilds)} servers! | ?help"))
    # print("Updated presence")

# On ready
@client.event
async def on_ready():
    await update_activity()
    channel = client.get_channel(925513395883606129)
    client.last_login_time = datetime.datetime.now()
    art = pyfiglet.figlet_format("CONNECTED")
    client.cp.print(art, "green")
    await channel.send("Online")
    log.log_message("Bot is online")


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

    # if blacklisted dont let them use bot
    try:
        notbl = await notblacklisted(message)
        if notbl == True:
            prefix = await get_prefix(client, message)
            if prefix in message.content:
                await update_user_db(message.author.id)
            await client.process_commands(message)

    except Exception:
        await client.process_commands(message)

    if f"<@!{client.user.id}>" in message.content or f"<@{client.user.id}>" in message.content:
        em = discord.Embed(
            title=f"Hi, my prefix is `{prefix}`", 
            color=message.author.color
        )
        return await message.channel.send(embed=em)


@tasks.loop(hours=2.0)
async def clear_stuff():
    _dir = 'tempstorage/'
    for f in os.listdir(_dir):
      os.remove(os.path.join(_dir, f))
      


def start_bot(client):
    log.log_message("Starting up bot")

    cogs = []

    all_categories = list(os.listdir("cogs"))
    for category in all_categories:
        for filename in os.listdir(f"cogs/{category}"):
            if filename.endswith(".py"):
                cogs.append(f"cogs.{category}.{filename[:-3]}")
            else:
                continue 
    
    try:
        # Loading all cogs with a progress Bar
        i = 0
        for cog in cogs:
            client.cogs_list = cogs
            client.load_extension(cog)
            print_percent_done(i, len(cogs))
            i+=1

        time.sleep(1)
        print("\n")

        clear_stuff.start()

        client.run(os.environ['TOKEN'])

    except Exception as e:
        print(f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")
        log.log_error(f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")


if __name__ == '__main__':
    start_bot(client)
