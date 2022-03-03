"""
Our program, who art in memory,
    called by thy name;
  thy operating system run;
thy function be done at runtime
  as it was on development.
Give us this day our daily output.
And forgive us our code duplication,
    as we forgive those who
  duplicate code against us.
And lead us not into frustration;
  but deliver us from GOTOs.
    For thine is algorithm,
the computation, and the solution,
    looping forever and ever.
          Return;
"""

# If you are reading this code - I'm sorry

import os
import json
import datetime
import time
import discord
from discord.ext import commands, tasks
import dotenv
import pyfiglet
from utils import Log, update_activity
import sidspackage

dotenv.load_dotenv()

log = Log("./database/log.txt", timestamp=True)

async def get_prefix(client, message):
    """
    This function gets the command_prefix for the server

    Args:
        client (discord.ext.commands.Bot) : The bot
        message (discord.Message) : The discord message sent

    Returns:
        str : The command prefix for the guild
    """
    try:
        data = await client.get_db()
        return data[str(message.guild.id)]['prefix']

    except Exception: # If any error occurs just return the default prefix: ?
        return "?"


intents = discord.Intents.all()
allowed_mentions = discord.AllowedMentions(everyone=False) # Disables the bot from being able to @everyone


class WhyBot(commands.Bot):
    """
    Why Bot: A subclass of `discord.ext.commands.Bot`
    """
    def __init__(self):
        super().__init__(command_prefix=get_prefix, intents=intents, help_command=None, owner_id=624076054969188363, case_insensitive=True,allowed_mentions=allowed_mentions)
        
        self.cp = sidspackage.ColorPrint()
        
        self.cogs_list = None # List of cogs
        self.last_login_time = datetime.datetime.now() # Uptime

        self.why_ascii_art = pyfiglet.figlet_format("Why Bot")
        self.cp.print(self.why_ascii_art, color="blue")


    async def get_db(self):
        """
        This function returns the main database file.
        Yes i'm to lazy to make an actualy db so im using json

        Returns:
            Dict : The json file
        """
        with open("database/db.json") as f:
            data = json.load(f)
        return data


    async def update_db(self, data):
        """
        This function updates the main database file.

        Args:
            data (Dict) : This is the json data that will be dumped into the file
        """
        with open("database/db.json", 'w') as f:
            json.dump(data, f, indent=4)


    async def get_user_db(self):
        """
        This function returns the user database file.

        Returns:
            Dict : The json file
        """
        with open("database/userdb.json") as f:
            data = json.load(f)
        return data


    async def update_user_db(self, data):
        """
        This function updates the user database file.

        Args:
            data (Dict) : This is the json data that will be dumped into the file
        """
        with open("database/userdb.json", 'w') as f:
            json.dump(data, f, indent=4)

        
    @property
    async def uptime(self):
        """
        This function returns the uptime for the bot. 

        Returns:
            str : Formated string with the uptime
        """
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


    @property
    def get_why_emojies(self):
        """
        This function returns the emojis for the bot

        Returns:
            Dict : A dictionary of emojis
        """
        return {
            "why" : "<:why:932912321544728576>"
        }

    
    @property
    def blacklisted_users(self):
        """
        This function returns all the blacklisted users

        Returns:
            List : List of blacklisted users
        """
        with open("database/blacklisted.json") as f:
            data = json.load(f)
        return data


    async def blacklist_user(self, user_id : int):
        """
        This function is used to blacklist a user so they cant use why bot anymore

        Args:
            user_id (int) : The id for the user. This will be appended to the List of blacklisted users
        """
        with open("database/blacklisted.json") as f:
            data = json.load(f)

        if user_id not in data:
            data.append(user_id)

        with open('database/blacklisted.json', 'w') as f:
            json.dump(data, f, indent=4)

    
    async def whitelist_user(self, user_id : int):
        """
        This function is used to whitelist a user so they can use why bot

        Args:
            user_id (int) : The id for the user. This will be appended to the List of blacklisted users
        """
        with open('database/blacklisted.json') as f:
            data = json.load(f)

        if user_id in data:
            data.remove(user_id)

        with open('database/blacklisted.json', 'w') as f:
            json.dump(data, f, indent=4)

    
    async def is_user_blacklisted(self, user_id : int):
        """
        This function is used to check if a user is blacklisted or not

        Args:
            user_id (int) : The id of the user you want to check

        Returns:
            Boolean : If user is blacklisted it will return True
                else it returns False
        """
        with open('database/blacklisted.json') as f:
            data = json.load(f)

        if user_id in data:
            return True
        
        return False


client = WhyBot()


# On ready
@client.event
async def on_ready():
    """Called when the bot is ready"""
    await update_activity(client)
    channel = client.get_channel(925513395883606129)
    art = pyfiglet.figlet_format("CONNECTED")
    client.cp.print(art, "green")
    await channel.send("Online")
    log.log_message("Bot is online")


async def update_user_db(user_id):
    """
    This function updates the command count for a user and 
    if they dont exist in the database it adds the user to it

    Args:
        user_id (int) : The id of the user

    """
    data = await client.get_user_db()

    try:
        data[str(user_id)]['command_count'] += 1

    except KeyError: # If user is not in the database, Then add them to the database
        user_data = {
            "user_id": user_id,
            "command_count": 1,
            "settings": {},
            "on_pinged": {"title": None, "description": None, "color": None},
            "on_pinged_toggled" : True
        }
        data[str(user_id)] = user_data

    await client.update_user_db(data)


@tasks.loop(hours=2.0)
async def clear_stuff():
    """
    This is a loop that runs every 2h
    It clears out all the files in the temporary storage directory
    """
    _dir = 'tempstorage/'
    for f in os.listdir(_dir):  
        os.remove(os.path.join(_dir, f))


# On Message
@client.event
async def on_message(message):
    """
    The on message event, Run when theres a message
    This function checks if the user is blacklisted or if the client.user is mentioned
    in the message content

    Args:
        message (discord.Message) : The message

    """
    if message.author == client.user:
        return  # if bot - no

    # if blacklisted dont let them use bot
    try:
        user_blacklisted = await client.is_user_blacklisted(message.author.id)

        if user_blacklisted:
            return

        prefix = await get_prefix(client, message)

        if prefix in message.content:
            await update_user_db(message.author.id)

        await client.process_commands(message)

    except Exception:
        await client.process_commands(message)

    # Check if why is mentioned in message
    if client.user.mentioned_in(message) and message.mention_everyone == False:
        if message.reference is not None:
            msg = await message.channel.fetch_message(message.reference.message_id)
            if msg.author.id == client.user.id:
                return
        em = discord.Embed(
            title=f"Hi, my prefix is `{prefix}`", 
            color=message.author.color
        )
        return await message.channel.send(embed=em)
      

def print_percent_done(index, total, bar_len=50, title='Loading Cogs:'):
    """This function makes a cool loading bar to visualize the bot loading cogs"""
    percent_done = (index+1)/total*100
    percent_done = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    print(f'{title} [{done_str}{togo_str}] {percent_done}% done', end='\r')

    if round(percent_done) == 100:
        print('Loaded All: ✅ ')


def start_bot(client):
    """
    This function starts the discord bot
    It loads all the cogs and starts the tasks

    Args:
        client (discord.ext.commands.Bot) : This is the client
    
    """
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
