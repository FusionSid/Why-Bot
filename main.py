import discord
import sqlite3
import os
import math
from discord.ext import commands
from keep_alive import keep_alive
from os import listdir
from os.path import isfile, join
import json
from discord_slash import SlashCommand, SlashContext


# Get prefix
def get_prefix(client, message):
    cd = "/home/runner/Why-Bot"
    os.chdir(f"{cd}/Setup")
    with open(f"{message.guild.id}.json") as f:  # open prefix file
        data = json.load(f)
    prefix = data[3]["prefix"]
    os.chdir(cd)
    return prefix


intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)
slash = Slash(client)


# Update bot activity to show guilds and help command
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


async def memberjoin(member):
    em = discord.Embed(
        title="Welcome", description=f"Hello there :wave: {member.name} welcome to {member.guild.name}\nHope you have fun on this server :)", color=discord.Color(value=0x36393e))
    try:
        await member.send(embed=em)  # Welcome message
    except:
        print('f')
    cd = os.getcwd()
    os.chdir(f"{cd}/Setup")
    with open(f"{member.guild.id}.json") as f:
        # Open setup file and check if there is a welcome channel
        data = json.load(f)
    cha = data[2]["welcome_channel"]
    if cha == None:
        await member.guild.system_channel.send(embed=em)
    else:
        channel = await client.fetch_channel(int(cha))
        # Send welcome message in server welcome channel
        await channel.send(embed=em)


# On member join
@client.event
async def on_member_join(member):
    await memberjoin(member)


# On reaction
@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    with open("react.json") as f:
        data = json.load(f)
        for x in data:
            if x['emoji'] == payload.emoji.name and x["message_id"] == payload.message_id:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])
                await payload.member.add_roles(role)
            else:
                pass


# On voice channel join
@client.event
async def on_voice_state_update(member, before, after):
    os.chdir("/home/runner/Why-Bot")
    if member.bot:
        return
    if not before.channel and not after.channel:
        pass
    if before.channel and after.channel:
        pass
    if after.channel is not None:
        # Custom vc templates
        if after.channel.name == "Custom VC":
            name = f"{member.name}'s VC"
            guild = after.channel.guild
            channel = await guild.create_voice_channel(name)
            with open('customchannel.json') as f:
                data = json.load(f)
            data.append(channel.id)
            with open('customchannel.json', 'w') as f:
                json.dump(data, f)
            if channel is not None:
                await member.move_to(channel)  # move person to channel

    if before.channel is not None:
        with open('customchannel.json') as f:
            channels = json.load(f)
        if before.channel.id in channels:  # If the member just created a custom channel and left it - DELETE THAT SHIT
            for i in channels:
                if i == before.channel.id:
                    cha = i
                    if len(before.channel.members) == 0:
                        await before.channel.delete()
                    channels.remove(i)
                    break
            with open('customchannel.json', 'w') as f:
                json.dump(channels, f)


# Setup for guild
async def startguildsetup(id):
    cd = os.getcwd()
    os.chdir("{}/Setup".format(cd))
    file = [
        {"mod_channel": None},
        {"counting_channel": None},
        {"welcome_channel": None},
        {"prefix": "?"}
    ]
    with open(f'{id}.json', 'w') as f:
        json.dump(file, f)
    os.chdir(cd)  # Create blank setup file
    with open("counting.json") as f:
        data = json.load(f)
    data[id] = 0  # Set counting to 0
    with open("counting.json", 'w') as f:
        json.dump(data, f)
    os.chdir(f"{cd}/MainDB")
    conn = sqlite3.connect(f"warn{id}.db")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS Warnings (id INTEGER, reason TEXT, time TEXT)")
    # c.execute() create level table
    newtickettemplate = {"ticket-counter": 0, "valid-roles": [],
                         "pinged-roles": [], "ticket-channel-ids": [], "verified-roles": []}
    with open(f"ticket{id}.json", 'w') as f:
        json.dump(newtickettemplate, f)
    os.chdir(cd)
    os.chdir(f"{cd}/EncryptDB")
    conn = sqlite3.connect(f"{id}.db")
    c = conn.cursor()
    os.chdir(cd)


# On Guild Join
@client.event
async def on_guild_join(guild):
    cha = client.get_channel(896932591620464690)
    await cha.send(f"Joined: {guild.name}")
    await update_activity()
    await startguildsetup(guild.id)
    embed = discord.Embed(color=discord.Color(value=0x36393e))
    embed.set_author(name="Here's some stuff to get you started:")
    embed.add_field(name="Default Prefix:",
                    value="```?```, Can be changed later")
    embed.set_footer(text=f"Why bot is now on {len(client.guilds)} servers!")
    try:
        await guild.system_channel.send(content="**Hello! Thanks for inviting me! :wave: **", embed=embed)
        await guild.system_channel.send("PLEASE run ```?setup``` to setup the bot")
    except:
        pass


# On remove - Update to show -1 guilds
@client.event
async def on_guild_remove(guild):
    await update_activity()


# Setup command
@client.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    def wfcheck(m):
        return m.channel == ctx.channel and m.author == ctx.author

    # Tell em what the need
    await ctx.send(embed=discord.Embed(title="To setup the bot you will need to copy the id's of some channels.", description="Please turn on developer mode to be able to copy channel id's"))
    cd = os.getcwd()
    os.chdir("{}/Setup".format(cd))
    with open(f'{ctx.guild.id}.json') as f:
        data = json.load(f)
    os.chdir(cd)

    # ask for mod channel
    await ctx.send(embed=discord.Embed(title="Please enter the id for the mod/staff channel.", description="All mod commands done by the bot will be logged here. Also reports will be sent to this channel.\nAlso members can report messages and they will be sent to this channel for review\nType None if you dont/want one"))
    mod = await client.wait_for("message", check=wfcheck)
    mod = mod.content
    mod = str(mod)
    if mod.lower == "none":
        pass
    else:
        try:
            mod = int(mod)
        except:
            await ctx.send("Invalid Input")

    # ask for count channel
    await ctx.send(embed=discord.Embed(title="Please enter the id for the counting channel", description="This is for the counting game.\nType None if you dont/want one"))
    counting = await client.wait_for("message", check=wfcheck)
    counting = counting.content
    counting = str(counting)
    if counting.lower == "none":
        pass
    else:
        try:
            counting = int(counting)
        except:
            await ctx.send("Invalid Input")

    # Ask for welcome channel
    await ctx.send(embed=discord.Embed(title="Please enter the id for the welcome channel", description="This is where the bot will welcome new users\nType None if you dont/want one"))
    welcome = await client.wait_for("message", check=wfcheck)
    welcome = welcome.content
    welcome = str(welcome)
    if welcome.lower == "none":
        pass
    else:
        try:
            welcome = int(welcome)
        except:
            await ctx.send("Invalid Input")

    data[0]["mod_channel"] = mod
    data[1]["counting_channel"] = counting
    data[2]["welcome_channel"] = welcome

    os.chdir("{}/Setup".format(cd))
    with open(f'{ctx.guild.id}.json', 'w') as f:
        json.dump(data, f)  # Update setup file

    os.chdir(cd)


# Set Prefix
@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, pref: str):
    cd = os.getcwd()
    os.chdir("{}/Setup".format(cd))
    with open(f'{ctx.guild.id}.json') as f:
        data = json.load(f)
    data[3]["prefix"] = pref
    with open(f'{ctx.guild.id}.json', 'w') as f:
        json.dump(data, f)
    await ctx.send(f"Prefix is now `{pref}`")
    os.chdir(cd)


# Get the counting channel
async def get_counting_channel(guild):
    cd = os.getcwd()

    os.chdir(f"{cd}/Setup")

    with open(f"{guild.id}.json") as f:
        data = json.load(f)  # open setup file and find channel

    os.chdir(cd)

    cc = data[1]["counting_channel"]
    if cc == None:
        return False
    else:
        return cc


# Counting
async def counting(msg, guild, channel):
    try:
        msg = int(msg)
    except:
        return
    cc = await get_counting_channel(guild)
    if cc == False:
        return
    if channel.id == cc:
        with open("counting.json") as f:
            data = json.load(f)
        dataid = f'{guild.id}'
        if (data[dataid] + 1) == msg:
            data[dataid] += 1
        else:
            data[dataid] = 0
            await channel.send("You ruined it, count reset to zero")
        with open("counting.json", 'w') as f:
            json.dump(data, f)


# Blacklist system
def notblacklisted(ctx):
    with open("blacklisted.json") as f:
        blacklisted = json.load(f)  # Check if blacklisted
    for user in blacklisted:
        if ctx.author.id == user:
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

    # if blacklisted dont let them use bot
    try:
        bl = notblacklisted(message)
        if bl == True:
            await client.process_commands(message)
    except:
        await client.process_commands(message)


# Errors
@client.event
async def on_command_error(ctx, error):
    cha = client.get_channel(896932591620464690)
    await cha.send(error)

    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(
            title="Wow buddy, Slow it down\nThis command is on cooldown",
            description=f"Try again in {math.ceil(error.retry_after)}seconds.",
        )

    elif isinstance(error, commands.CommandNotFound):
        em = discord.Embed(
            title="Command not found",
            description="This command either doesn't exist, or you typed it wrong.",
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

    else:
        print("An error has occured:\n{}".format(error))
        em = discord.Embed(
            title="Error", description="Possible bug?\n?report bug <bug>")
        em.add_field(name="Error", value=error)

    await ctx.send(embed=em, delete_after=6)


# Start the bot
def start_bot(client):
    keep_alive()  # start website and if im using replit which i might it will let the bot stay alive
    client.remove_command("help")
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
