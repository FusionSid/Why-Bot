import discord
from discord_slash.utils.manage_commands import create_option
import sqlite3
import os
import math
from discord.ext import commands
from keep_alive import keep_alive
from os import listdir
from os.path import isfile, join
import json
from discord_slash import SlashCommand
from discord.ext import commands
from discordLevelingSystem import DiscordLevelingSystem, RoleAward, LevelUpAnnouncement
from easy_pil import Editor, Canvas, Font, load_image, Text
import sys

# Get prefix

def get_prefix(client, message):
    try:
      cd = "/home/runner/Why-Bot"
      os.chdir(f"{cd}/Setup")
      with open(f"{message.guild.id}.json") as f:  # open prefix file
          data = json.load(f)
      prefix = data[3]["prefix"]
      os.chdir(cd)
      return prefix
    except:
      return "?"


intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix,
                      intents=intents, help_command=None)
slash = SlashCommand(client, sync_commands=True)


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
    # Custom Image
    background = Editor(Canvas((900, 270), "#23272a"))

    # For profile to use users profile picture load it from url using the load_image/load_image_async function
    profile_image = load_image(str(member.avatar_url))
    profile = Editor(profile_image).resize((150, 150)).circle_image()

    # Fonts to use with different size
    poppins_big = Font.poppins(variant="bold", size=50)
    poppins_mediam = Font.poppins(variant="bold", size=40)
    poppins_regular = Font.poppins(variant="regular", size=30)
    poppins_thin = Font.poppins(variant="light", size=18)

    card_left_shape = [(0, 0), (0, 270), (330, 270), (260, 0)]

    background.polygon(card_left_shape, "#2C2F33")
    background.paste(profile, (40, 35))
    background.text((600, 20), "WELCOME", font=poppins_big, color="white", align="center")
    background.text(
        (600, 70), f"{member.name}", font=poppins_regular, color="white", align="center"
    )
    background.text(
        (600, 120), "THANKS FOR JOINING", font=poppins_mediam, color="white", align="center"
    )
    background.text(
        (600, 160), f"{member.guild.name}", font=poppins_regular, color="white", align="center"
    )
    background.text(
        (620, 245),
        "THANK YOU FOR JOINING. HOPE YOU WILL ENJOY YOUR STAY",
        font=poppins_thin,
        color="white",
        align="center",
    )

    background.save(f"welcome{member.id}.png")

    try:
        await member.send(file=discord.File(f"welcome{member.id}.png"))  # Welcome message
    except:
        print('f')
    cd = "/home/runner/Why-Bot"
    os.chdir(f"{cd}/Setup/")
    with open(f"{member.guild.id}.json") as f:
        # Open setup file and check if there is a welcome channel
        data = json.load(f)
    os.chdir(cd)
    cha = data[2]["welcome_channel"]
    if cha == None:
        await member.guild.system_channel.send(file=discord.File(f"welcome{member.id}.png"))
    else:
        channel = await client.fetch_channel(int(cha))
        # Send welcome message in server welcome channel
        await channel.send(file=discord.File(f"welcome{member.id}.png"))
    os.remove(f"welcome{member.id}.png")

        
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
    cd = "/home/runner/Why-Bot"
    os.chdir("/home/runner/Why-Bot/Setup")
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
    os.chdir("/home/runner/Why-Bot/MainDB")
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
    os.chdir("/home/runner/Why-Bot/EncryptDB")
    conn = sqlite3.connect(f"{id}.db")
    c = conn.cursor()
    os.chdir(cd)


# On Guild Join
@client.event
async def on_guild_join(guild):
    cha = client.get_channel(896932591620464690)
    await cha.send(embed=discord.Embed(title="Join", description=f"Joined: {guild.name}"))
    await update_activity()
    await startguildsetup(guild.id)
    embed = discord.Embed(color=discord.Color(value=0x36393e))
    embed.set_author(name="Here's some stuff to get you started:")
    embed.add_field(name="Default Prefix:",
                    value="`?` This caan be changed later using `?setprefix`")
    embed.set_footer(text=f"Thank You - Why bot is now on {len(client.guilds)} servers!")
    embed.add_field(name="Please run `?setup`", description="To setup the bot")
    try:
        await guild.system_channel.send(content="**Hello! Thanks for inviting me! :wave: **", embed=embed)
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
    cd = "/home/runner/Why-Bot"
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
            data[0]["mod_channel"] = mod
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
            data[1]["counting_channel"] = counting
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
            data[2]["welcome_channel"] = welcome
        except:
            await ctx.send("Invalid Input")
            
    cd = "/home/runner/Why-Bot"
    os.chdir("{}/Setup".format(cd))
    with open(f'{ctx.guild.id}.json', 'w') as f:
        json.dump(data, f)  # Update setup file

    os.chdir(cd)
    await ctx.send("Setup Complete!\nRemember you can use ?setprefix to change the prefix")


# Set Prefix
@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, pref: str):
    cd = "/home/runner/Why-Bot"
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
  try:
    cd = "/home/runner/Why-Bot"

    os.chdir(f"{cd}/Setup")

    with open(f"{guild.id}.json") as f:
        data = json.load(f)  # open setup file and find channel

    os.chdir(cd)

    cc = data[1]["counting_channel"]
    if cc == None:
        return False
    else:
        return cc
  except:
    pass


# Counting
async def counting(msg, guild, channel):
    try:
        msg = int(msg)
    except:
        return
    cc = await get_counting_channel(guild)
    if cc == False:
        print("Not channel")
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
async def notblacklisted(ctx):
    with open("blacklisted.json") as f:
        blacklisted = json.load(f)  # Check if blacklisted
    for user in blacklisted:
        if ctx.author.id == user:
            return False
    return True  # If notblacklisted return true else return false


# Leveling

yes_guild = 893653614990606346
the_darth_gang = 1

my_awards = {
    yes_guild : [
        RoleAward(role_id=893681219269705728, level_requirement=1, role_name='Ur Cool')
    ]
}

lvlembed = discord.Embed()
lvlembed.set_author(name=LevelUpAnnouncement.Member.name, icon_url=LevelUpAnnouncement.Member.avatar_url)
lvlembed.description = f'Congrats {LevelUpAnnouncement.Member.mention}! You are now level {LevelUpAnnouncement.LEVEL} 😎'

announcement = LevelUpAnnouncement(lvlembed)

lvl = DiscordLevelingSystem(rate=1, per=10.0, level_up_announcement=announcement, awards=my_awards)
lvl.connect_to_database_file('/home/runner/Why-Bot/DiscordLevelingSystem.db')


@client.command(aliases=['lvl'])
async def rank(ctx, member:discord.Member=None):
    if member == None:
      data = await lvl.get_data_for(ctx.author)
    else:
      data = await lvl.get_data_for(member)

    LEVELS_AND_XP = {
        '0': 0,
        '1': 100,
        '2': 255,
        '3': 475,
        '4': 770,
        '5': 1150,
        '6': 1625,
        '7': 2205,
        '8': 2900,
        '9': 3720,
        '10': 4675,
        '11': 5775,
        '12': 7030,
        '13': 8450,
        '14': 10045,
        '15': 11825,
        '16': 13800,
        '17': 15980,
        '18': 18375,
        '19': 20995,
        '20': 23850,
        '21': 26950,
        '22': 30305,
        '23': 33925,
        '24': 37820,
        '25': 42000,
        '26': 46475,
        '27': 51255,
        '28': 56350,
        '29': 61770,
        '30': 67525,
        '31': 73625,
        '32': 80080,
        '33': 86900,
        '34': 94095,
        '35': 101675,
        '36': 109650,
        '37': 118030,
        '38': 126825,
        '39': 136045,
        '40': 145700,
        '41': 155800,
        '42': 166355,
        '43': 177375,
        '44': 188870,
        '45': 200850,
        '46': 213325,
        '47': 226305,
        '48': 239800,
        '49': 253820,
        '50': 268375,
        '51': 283475,
        '52': 299130,
        '53': 315350,
        '54': 332145,
        '55': 349525,
        '56': 367500,
        '57': 386080,
        '58': 405275,
        '59': 425095,
        '60': 445550,
        '61': 466650,
        '62': 488405,
        '63': 510825,
        '64': 533920,
        '65': 557700,
        '66': 582175,
        '67': 607355,
        '68': 633250,
        '69': 659870,
        '70': 687225,
        '71': 715325,
        '72': 744180,
        '73': 773800,
        '74': 804195,
        '75': 835375,
        '76': 867350,
        '77': 900130,
        '78': 933725,
        '79': 968145,
        '80': 1003400,
        '81': 1039500,
        '82': 1076455,
        '83': 1114275,
        '84': 1152970,
        '85': 1192550,
        '86': 1233025,
        '87': 1274405,
        '88': 1316700,
        '89': 1359920,
        '90': 1404075,
        '91': 1449175,
        '92': 1495230,
        '93': 1542250,
        '94': 1590245,
        '95': 1639225,
        '96': 1689200,
        '97': 1740180,
        '98': 1792175,
        '99': 1845195,
        '100': 1899250
    }
    if member == None:
      member = ctx.author
    else:
      pass
    arank = data.xp
    brank = LEVELS_AND_XP[f"{data.level+1}"] - LEVELS_AND_XP[f"{data.level}"]
    frac = arank/brank
    percentage = "{:.0%}".format(frac)
    percentage = int(percentage[:-1])

    user_data = {  # Most likely coming from database or calculation
    "name": f"{member.name}",  # The user's name
    "xp": arank,
    "level": data.level,
    "next_level_xp": brank,
    "percentage": percentage,
    "rank": data.rank
    }

    background = Editor(Canvas((934, 282), "#23272a"))
    profile_image = load_image(str(member.avatar_url))
    profile = Editor(profile_image).resize((150, 150)).circle_image()


    poppins = Font.poppins(size=30)

    background.rectangle((20, 20), 894, 242, "#2a2e35")
    background.paste(profile, (50, 50))
    background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
    background.bar(
        (260, 180),
        max_width=630,
        height=40,
        percentage=user_data["percentage"],
        fill="#00fa81",
        radius=20,
    )
    background.text((270, 120), user_data["name"], font=poppins, color="#00fa81")
    background.text(
        (870, 125),
        f"{user_data['xp']} / {user_data['next_level_xp']}",
        font=poppins,
        color="#00fa81",
        align="right",
    )

    rank_level_texts = [
        Text("Rank ", color="#00fa81", font=poppins),
        Text(f"{user_data['rank']}", color="#1EAAFF", font=poppins),
        Text("   Level ", color="#00fa81", font=poppins),
        Text(f"{user_data['level']}", color="#1EAAFF", font=poppins),
    ]

    background.multicolor_text((850, 30), texts=rank_level_texts, align="right")

    # send
    background.save(f"rank{member.id}.png")
    await ctx.send(file=discord.File(f"rank{member.id}.png"))
    os.remove(f"rank{member.id}.png")


@client.command()
async def leaderboard(ctx):
    data = await lvl.each_member_data(ctx.guild, sort_by='rank')
    em = discord.Embed(title="Leaderboard")
    n = 0
    for i in data:
      em.add_field(name=f'{i.rank}: {i.name}', value=f'Level: {i.level}, Total XP: {i.total_xp}', inline=False)
      n += 1
      if n == 10:
        break 
    await ctx.send(embed=em)


def is_it_me(ctx):
    return ctx.author.id == 624076054969188363


@client.command()
@commands.check(is_it_me)
async def axp(ctx, member:discord.Member, amount:int):
    await lvl.add_xp(member=member, amount=amount)


@client.command()
@commands.check(is_it_me)
async def rxp(ctx, member:discord.Member, amount:int):
    await lvl.remove_xp(member=member, amount=amount)


@client.command()
@commands.check(is_it_me)
async def slvl(ctx, member:discord.Member, level:int):
    await lvl.set_level(member=member, level=level)

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
        bl = await notblacklisted(message)
        if bl == True:
            await client.process_commands(message)
    except:
        await client.process_commands(message)


# Errors


@client.event
async def on_command_error(ctx, error):
    cha = client.get_channel(896932591620464690)
    await cha.send(embed=discord.Embed(title="ERROR", description=error))

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
