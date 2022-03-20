"""
This is the main file for the bot
It contains the client (subclass of: `discord.ext.commands.Bot`)
and the functions to start up the bot
"""

__version__ = 2.0
__author__ = "Siddhesh Zantye"

import os
import time
import json
import datetime

import discord
import aiosqlite
from dotenv import load_dotenv
from discord.ext import commands

from log import log_normal
from utils import Config


async def get_prefix(client, message):
    """
    This function gets the command_prefix for the server
    
    Parameters:
        :param: client (discord.ext.commands.Bot) : The bot
        :param: message (discord.Message) : The discord message sent

    Returns:
        str : The command prefix for the guild
    """

    async with aiosqlite.connect("database/prefix.db") as db:
        cur = await db.execute("SELECT * FROM Prefix WHERE guild_id=?", (message.guild.id,))
        prefix = await cur.fetchall()

        if len(prefix) == 0:
            prefix = "?"
            await db.execute("INSERT INTO Prefix (guild_id, prefix) VALUES (?, ?)", (message.guild.id, prefix))
            await db.commit()
        else:
            prefix = prefix[0][1]
            
    return prefix
    

class WhyBot(commands.Bot):
    """
    The Why Bot Class (subclass of: `discord.ext.commands.Bot`)

    Parameters
        :param: config (Config): Config for the bot
    """
    def __init__(
            self,
            config : Config
        ):

        self.cogs_list = []
        self.config = config
        self.version = __version__
        self.last_login_time = datetime.datetime.now()

        intents = discord.Intents.all()
        allowed_mentions = discord.AllowedMentions(everyone=False)

        super().__init__(
            intents=intents, 
            help_command=None, 
            case_insensitive=True,
            command_prefix=get_prefix, 
            owner_id=624076054969188363, # The bot owner's ID
            allowed_mentions=allowed_mentions
        )

    
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

        Parameters
            :param: user_id (int) : The id for the user. This will be appended to the List of blacklisted users
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
        
        Parameters
            :param: user_id (int) : The id for the user. This will be appended to the List of blacklisted users
        """
        with open('database/blacklisted.json') as f:
            data = json.load(f)

        if user_id in data:
            data.remove(user_id)

        with open('database/blacklisted.json', 'w') as f:
            json.dump(data, f, indent=4)


def loading_bar(
        length : int, index : int, title : str, end : str
    ):
    """
    Makes a loading bar when starting up the bot

    Parameters
        :param: length (int): The length of the list
        :param: index (int): Index of the list
        :param: title (str): The title of the loading bar
        :param: end (str): The message to say once the bar is done
    """
    percent_done = (index+1)/length*100
    done = round(percent_done/(100/50))
    togo = 50-done

    done_str = "█"*int(done)
    togo_str = "░"*int(togo)


    print(f'{title} {done_str}{togo_str} {int(percent_done)}% Done', end='\r')

    if round(percent_done) == 100:
        print(f"\n\n{end}\n")


def start_bot(client : WhyBot):
    """
    Starts up the amazing Why Bot
    """
    cogs = []

    all_categories = list(os.listdir("cogs"))
    for category in all_categories:
        for filename in os.listdir(f"cogs/{category}"):
            if filename.endswith(".py"):
                cogs.append(f"cogs.{category}.{filename[:-3]}")
    
    print("\n")
    for index, cog in enumerate(cogs):
        client.cogs_list = cogs
        client.load_extension(cog)
        loading_bar(len(cogs), index, "Loading Cogs:", "Loaded All Cogs ✅")
        time.sleep(1)


    time.sleep(1)

    client.run(os.environ['TOKEN'])


if __name__ == '__main__':
    load_dotenv()

    with open("config.json") as f:
        config = Config(json.load(f))

    client = WhyBot(config)

    start_bot(client)