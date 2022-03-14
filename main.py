import discord
from discord.ext import commands
import datetime
import json
import aiosqlite
import os
import time
from dotenv import load_dotenv
from log import log_errors

load_dotenv()


class Config():
    def __init__(self, data):
        self.join_alert_channel = data["join_alert_channel"]
        self.leave_alert_channel = data["leave_alert_channel"]
        self.online_alert_channel = data["online_alert_channel"]
        self.owner_id = data["owner_id"]


async def get_prefix(client, message):
    """
    This function gets the command_prefix for the server
    
    Parameters:
        client (discord.ext.commands.Bot) : The bot
        message (discord.Message) : The discord message sent

    Returns:
        str : The command prefix for the guild
    """

    async with aiosqlite.connect("database/prefixs.db") as db:
        cur = await db.execute("SELECT * FROM Prefix WHERE guild_id={}".format(message.guild.id))
        prefix = await cur.fetchall()

        if len(prefix) != 1:
            prefix = "?"
            await db.execute("INSERT INTO Prefix (guild_id, prefix) VALUES ({}, '{}')".format(message.guild.id, prefix))
            await db.commit()

    return prefix
    

class WhyBot(commands.Bot):
    def __init__(
            self,
            config
        ):
        intents = discord.Intents.all()
        allowed_mentions = discord.AllowedMentions(everyone=False)

        super().__init__(
            command_prefix=get_prefix, 
            intents=intents, 
            help_command=None, 
            owner_id=config.owner_id, 
            case_insensitive=True,
            allowed_mentions=allowed_mentions)

        self.last_login_time = datetime.datetime.now()

    
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
        Parameters:
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
        Parameters:
            user_id (int) : The id for the user. This will be appended to the List of blacklisted users
        """
        with open('database/blacklisted.json') as f:
            data = json.load(f)

        if user_id in data:
            data.remove(user_id)

        with open('database/blacklisted.json', 'w') as f:
            json.dump(data, f, indent=4)


    @property
    async def config(self):
        """
        Returns a dict of config for the bot
        """
        with open("config.json") as f:
            data = json.load(f)

        return data


# Startup Bot:
def loading_bar(length, index, title, end):
    percent_done = (index+1)/length*100
    done = round(percent_done/(100/50))
    togo = 50-done

    done_str = "█"*int(done)
    togo_str = "░"*int(togo)


    print(f'{title} {done_str}{togo_str} {int(percent_done)}% Done', end='\r')

    if round(percent_done) == 100:
        print(f"\n\n{end}\n")


def start_bot(client):

    cogs = []

    all_categories = list(os.listdir("cogs"))
    for category in all_categories:
        for filename in os.listdir(f"cogs/{category}"):
            if filename.endswith(".py"):
                cogs.append(f"cogs.{category}.{filename[:-3]}")
            else:
                continue 
    
    try:
        print("\n")
        for cog, index in enumerate(cogs):
            client.cogs_list = cogs
            client.load_extension(cog)
            loading_bar(len(cogs), index, "Loading Cogs:", "Loaded All Cogs ✅")

        time.sleep(1)

        client.run(os.environ['TOKEN'])

    except Exception as e:
        print(f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")


def main():
    with open("config.json") as f:
        data = json.load(f)

    config = Config(data)

    client = WhyBot(config)

    start_bot(client)


if __name__ == '__main__':
    main()