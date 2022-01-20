import json
from discord.channel import DMChannel
from discordLevelingSystem import DiscordLevelingSystem, RoleAward, LevelUpAnnouncement
import os
from os import listdir
from os.path import isfile, join
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from utils.keep_alive import keep_alive
import dotenv
from easy_pil import Editor, Canvas, Font, load_image, Text
from discord.ui import Button, View
from datetime import datetime
from utils import is_it_me

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

def log(log):
    now = datetime.now()
    timern = now.strftime("%d/%m/%Y %H:%M:%S")

    with open('other/log.txt', 'a') as f:
        f.write('\n')
        f.write(f"{timern} | {log}")

intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix,
                      intents=intents, help_command=None)


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


async def startguildsetup(id):
    file = {
        "guild_id": id,
        "prefix": "?",
        "counting_channel": None,
        "lastcounter":None,
        "log_channel": None,
        "welcome_channel": None,
        "warnings": {
        },
        "settings": {
        },
        "autorole": {
            "all": None,
            "bot": None
        }
    }
    with open("database/db.json") as f:
        data = json.load(f)

    data.append(file)
    with open("database/db.json", 'w') as f:
        json.dump(data, f, indent=4)
    newtickettemplate = {"ticket-counter": 0, "valid-roles": [],
                         "pinged-roles": [], "ticket-channel-ids": [], "verified-roles": []}
    with open(f"tickets/ticket{id}.json", 'w') as f:
        json.dump(newtickettemplate, f, indent=4)
    with open(f"database/counting.json") as f:
        data = json.load(f)
    data[f"{id}"] = 0
    with open(f"database/counting.json", 'w') as f:
        json.dump(data, f, indent=4)
# On Guild Join


@client.event
async def on_guild_join(guild):
    cha = client.get_channel(925513395883606129)
    await cha.send(embed=discord.Embed(title="Join", description=f"Joined: {guild.name}"))
    await update_activity()
    await startguildsetup(guild.id)
    embed = discord.Embed(color=discord.Color(value=0x36393e))
    embed.set_author(name="Here's some stuff to get you started:")
    embed.add_field(name="Default Prefix: `?`",
                    value="This can be changed later using `?setprefix`")
    embed.add_field(name="Channel Setting",
                    value="To set the counting, mod and welcome channel use `?set`")
    embed.add_field(
        name="Settings", value="You can use `?settings` to change some bot settings")
    embed.set_footer(
        text=f"Thank You - Why bot is now on {len(client.guilds)} servers!")
    try:
        await guild.system_channel.send(content="**Thanks for inviting me! :wave: **", embed=embed)
    except:
        pass
    
# Set Prefix


@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, pref: str):
    with open(f'database/db.json') as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == ctx.guild.id:
            i["prefix"] = pref
    with open(f'database/db.json', 'w') as f:
        json.dump(data, f)
    await ctx.send(embed=discord.Embed(title=f"Prefix has been set to `{pref}`"))


@client.event
async def on_guild_remove(guild):
    await update_activity()



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
            "user_id":user,
            "command_count" : 1,
            "settings":{},
            "on_pinged": {"title": None, "description":None, "color":None}
        }
        data.append(user_data)
    with open("database/userdb.json", 'w') as f:
        json.dump(data, f, indent=4)

# On Message
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # if bot - no

    if isinstance(message.channel, DMChannel):
        cha = await client.fetch_channel(926232260166975508)
        em = discord.Embed(title="New DM", description=f"From {message.author.name}")
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
      

@client.event
async def on_command_error(ctx, error):
    #cha = await client.fetch_channel(896932591620464690)
    #chaem = discord.Embed(title="ERROR", description=error)
    #chaem.add_field(name="Server:", value=f"{ctx.guild.id} ({ctx.guild.name})")
    #chaem.add_field(name="User:", value=f"{ctx.author.id} ({ctx.author.name})")
    # await cha.send(embed=chaem)
    log(f"ERROR: {error}")

    if isinstance(error, commands.CommandOnCooldown):
        async def better_time(cd:int):
          time = f"{cd}s"
          if cd > 60:
              minutes = cd - (cd % 60)
              seconds = cd - minutes
              minutes = int(minutes/ 60)
              time = f"{minutes}min {seconds}s"
              if minutes > 60:
                  hoursglad = minutes -(minutes % 60)
                  hours = int(hoursglad/ 60)
                  minutes = minutes - (hours*60)
                  time = f"{hours}h {minutes}min {seconds}s"
          return time
        cd = round(error.retry_after)
        if cd == 0:
            cd = 1
        retry_after = await better_time(cd)
        em = discord.Embed(
            title="Wow buddy, Slow it down\nThis command is on cooldown",
            description=f"Try again in **{retry_after}**",
        )
        await ctx.send(embed=em)

    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(
            title="Missing a requred value/arg",
            description="You haven't passed in all value/arg",
        )
        await ctx.send(embed=em)

    elif isinstance(error, commands.MissingPermissions):
        em = discord.Embed(
            title="Missing permissions",
            description="You don't have permissions to use this commands",
        )
        await ctx.send(embed=em)
      
# Start the bot


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
        print(f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")
        log(f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")


if __name__ == '__main__':
    start_bot(client)
