import math
import json
import sys
import sqlite3
from discord.utils import valid_icon_size
from discordLevelingSystem import DiscordLevelingSystem, RoleAward, LevelUpAnnouncement
import os
from os import listdir
from os.path import isfile, join
import discord
from discord.ext import commands
from discord import Option
from discord.ui import Button, View
from keep_alive import keep_alive
import dotenv

dotenv.load_dotenv()


async def get_prefix(client, message):
    with open('database/db.json') as f:
        data = json.load(f)
    for i in data:
        if i['guild_id'] == message.guild.id:
            return i['prefix']
    return "?"

intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)


async def update_activity():
    await client.change_presence(activity=discord.Game(f"On {len(client.guilds)} guilds! | ?help"))
    print("Updated presence")


# On ready
@client.event
async def on_ready():
    print("=======================\nConnected\n=========")
    await update_activity()
    channel = client.get_channel(896932591620464690)
    await channel.send("Online")


async def startguildsetup(id):
    file = {
        "guild_id": id,
        "prefix": "?",
        "counting_channel": None,
        "log_channel": None,
        "welcome_channel": None,
        "warnings": {
        },
        "settings": {  
        }
    }
    with open("database/db.json") as f:
        data = json.load(f)

    data.append(file)
    with open("database/db.json", 'w') as f:
        json.dump(data, f, indent=4)
    newtickettemplate = {"ticket-counter": 0, "valid-roles": [], "pinged-roles": [], "ticket-channel-ids": [], "verified-roles": []}
    with open(f"./tickets/{id}.json", 'w') as f:
        json.dump(newtickettemplate, f, indent=4)

# On Guild Join
@client.event
async def on_guild_join(guild):
    cha = client.get_channel(896932591620464690)
    await cha.send(embed=discord.Embed(title="Join", description=f"Joined: {guild.name}"))
    await update_activity()
    await startguildsetup(guild.id)
    embed = discord.Embed(color=discord.Color(value=0x36393e))
    embed.set_author(name="Here's some stuff to get you started:")
    embed.add_field(name="Default Prefix: `?`", value="This can be changed later using `?setprefix`")
    embed.add_field(name="Channel Setting", value="To set the counting, mod and welcome channel use `?set`")
    embed.add_field(name="Settings", value="You can use `?settings` to change some bot settings")
    embed.set_footer(text=f"Thank You - Why bot is now on {len(client.guilds)} servers!")
    try:
        await guild.system_channel.send(content="**Thanks for inviting me! :wave: **", embed=embed)
    except:
        pass

@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    with open("database/react.json") as f:
        data = json.load(f)
        for x in data:
            if x['emoji'] == payload.emoji.name and x["message_id"] == payload.message_id:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])
                await payload.member.add_roles(role)
            else:
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

# Leveling
lvlembed = discord.Embed()
lvlembed.set_author(name=LevelUpAnnouncement.Member.name,
                    icon_url=LevelUpAnnouncement.Member.avatar_url)
lvlembed.description = f'Congrats {LevelUpAnnouncement.Member.mention}! You are now level {LevelUpAnnouncement.LEVEL} 😎'

announcement = LevelUpAnnouncement(lvlembed)

lvl = DiscordLevelingSystem(
    rate=1, per=10.0, level_up_announcement=announcement)
lvl.connect_to_database_file('database/DiscordLevelingSystem.db')

# Get the counting channel
async def get_counting_channel(guild):
    with open("database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == guild.id:
            return int(i["counting_channel"])
    return None

# Counting
async def counting(msg, guild, channel):
    try:
        msg = int(msg)
    except:
        return
    cc = await get_counting_channel(guild)
    if cc is None:
        return
    if channel.id == cc:
        with open("database/counting.json") as f:
            data = json.load(f)
        dataid = f'{guild.id}'
        if (data[dataid] + 1) == msg:
            data[dataid] += 1
        else:
            data[dataid] = 0
            em = discord.Embed(title="You ruined it!", description="Count reset to zero")
            await channel.send(embed = em)
        with open("counting.json", 'w') as f:
            json.dump(data, f, indent=4)


# Blacklist system
async def notblacklisted(message):
    with open("blacklisted.json") as f:
        blacklisted = json.load(f)  # Check if blacklisted
    for user in blacklisted:
        if message.author.id == user:
            return False
    return True  # If notblacklisted return true else return false


# On Message
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # if bot - no

    # Fome variables that come in useful later
    channel = message.channel
    msg = message.content
    guild = message.guild

    # Check if counting channel
    await counting(msg, guild, channel)

    await lvl.award_xp(amount=[15,25], message=message)

    # if blacklisted dont let them use bot
    try:
        notbl = await notblacklisted(message)
        if notbl == True:
            await client.process_commands(message)
    except:
        await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    cha = client.get_channel(896932591620464690)
    await cha.send(embed=discord.Embed(title="ERROR", description=error))

    if isinstance(error, commands.CommandOnCooldown):

        async def better_time(cd: int):
            time = f"{cd}s"
            if cd > 60:
                minutes = cd - (cd % 60)
                seconds = cd - minutes
                minutes = int(minutes / 60)
                time = f"{minutes}min {seconds}s"
            if minutes > 60:
                hoursglad = minutes - (minutes % 60)
                hours = int(hoursglad / 60)
                minutes = minutes - (hours * 60)
                time = f"{hours}h {minutes}min {seconds}s"
            return time

        retry_after = await better_time(int(math.ceil(error.retry_after)))
        em = discord.Embed(
            title="Wow buddy, Slow it down\nThis command is on cooldown",
            description=f"Try again in {retry_after}seconds.",
        )

    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(
            title="Missing a requred value/arg",
            description="You haven't passed in all value/arg",
        )

    elif isinstance(error, commands.MissingPermissions):
        em = discord.Embed(
            title="Missing permissions",
            description="You don't have permissions to use this commands",
        )


@client.command()
async def setupallserversjustincase(ctx):
    servers = list(client.guilds)
    for i in servers:
        print(i)
        await startguildsetup(i.id)

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
        client.run(os.environ['TOKEN'])

    except Exception as e:
        print(
            f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")



if __name__ == '__main__':
    start_bot(client)
