import math
from backup import backup
import json
import sys
import sqlite3
from discord.channel import DMChannel
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
from easy_pil import Editor, Canvas, Font, load_image, Text
import requests

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

async def memberjoin(member):
    # Custom Image
    background = Editor(Canvas((900, 270), "#23272a"))

    # For profile to use users profile picture load it from url using the load_image/load_image_async function
    profile_image = load_image(str(member.avatar.url))
    profile = Editor(profile_image).resize((200, 200)).circle_image()

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

    background.save(f"tempstorage/welcome{member.id}.png")

    try:
        await member.send(file=discord.File(f"tempstorage/welcome{member.id}.png"))  # Welcome message
    except:
        print('f')
    with open(f"database/db.json") as f:
        # Open setup file and check if there is a welcome channel
        data = json.load(f)
    for i in data:
        if i["guild_id"] == member.guild.id:
            cha = i["welcome_channel"]
    if cha == None:
        await member.guild.system_channel.send(file=discord.File(f"welcome{member.id}.png"))
    else:
        channel = await client.fetch_channel(int(cha))
        # Send welcome message in server welcome channel
        await channel.send(file=discord.File(f"tempstorage/welcome{member.id}.png"))
    os.remove(f"tempstorage/welcome{member.id}.png")

async def mj(member):
    with open("database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == member.guild.id:
            channel = i["welcome_channel"]
            if channel == None:
                channel = member.guild.system_channel
    channel = await client.fetch_channel(channel)
    r = requests.get(
        url='https://api.xzusfin.repl.co/card?',
        params={
            'avatar': str(member.avatar.url),
            'middle': 'welcome',
            'name': str(member.name),
            'bottom': str('on ' + member.guild.name),
            'text': '#CCCCCC',
            'avatarborder': '#CCCCCC',
            'avatarbackground': '#CCCCCC',
            'background': 'https://c4.wallpaperflare.com/wallpaper/969/697/87/square-shapes-black-dark-wallpaper-preview.jpg'  # or image url
        }
    )
    em = discord.Embed()
    em.set_image(url=r.url)
    await channel.send(embed=em)


@client.event
async def on_member_join(member):
    await memberjoin(member)
    

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

@client.command(aliases=['lvl'])
async def rank(ctx, member:discord.Member=None):
    if member == None:
      data = await lvl.get_data_for(ctx.author)
    else:
      data = await lvl.get_data_for(member)

    LEVELS_AND_XP = {
        '0': 0,'1': 100,'2': 255,'3': 475,
        '4': 770,'5': 1150,'6': 1625,'7': 2205,'8': 2900,'9': 3720,'10': 4675,'11': 5775,'12': 7030,
        '13': 8450,'14': 10045,'15': 11825,'16': 13800,'17': 15980,'18': 18375,'19': 20995,'20': 23850,
        '21': 26950,'22': 30305,'23': 33925,'24': 37820,'25': 42000,'26': 46475,'27': 51255,'28': 56350,
        '29': 61770,'30': 67525,'31': 73625,'32': 80080,'33': 86900,'34': 94095,'35': 101675,'36': 109650,
        '37': 118030,'38': 126825,'39': 136045,'40': 145700,'41': 155800,'42': 166355,'43': 177375,'44': 188870,
        '45': 200850,'46': 213325,'47': 226305,'48': 239800,'49': 253820,'50': 268375,'51': 283475,'52': 299130,
        '53': 315350,'54': 332145,'55': 349525,'56': 367500,'57': 386080,'58': 405275,'59': 425095,'60': 445550,
        '61': 466650,'62': 488405,'63': 510825,'64': 533920,'65': 557700,'66': 582175,'67': 607355,'68': 633250,
        '69': 659870,'70': 687225,'71': 715325,'72': 744180,'73': 773800,'74': 804195,'75': 835375,'76': 867350,
        '77': 900130,'78': 933725,'79': 968145,'80': 1003400,'81': 1039500,'82': 1076455,'83': 1114275,'84': 1152970,
        '85': 1192550,'86': 1233025,'87': 1274405,'88': 1316700,'89': 1359920,'90': 1404075,'91': 1449175,'92': 1495230,
        '93': 1542250,'94': 1590245,'95': 1639225,'96': 1689200,'97': 1740180,'98': 1792175,'99': 1845195,'100': 1899250
    }

    if member == None:
      member = ctx.author
    else:
      pass
    arank = data.xp
    brank = LEVELS_AND_XP[f"{data.level+1}"]
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
    profile_image = load_image(str(member.avatar.url))
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
    background.save(f"tempstorage/rank{member.id}.png")
    await ctx.send(file=discord.File(f"tempstorage/rank{member.id}.png"))
    os.remove(f"tempstorage/rank{member.id}.png")


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
async def addxp(ctx, member:discord.Member, amount:int):
    await ctx.message.delete()
    await lvl.add_xp(member=member, amount=amount)


@client.command()
@commands.check(is_it_me)
async def removexp(ctx, member:discord.Member, amount:int):
    await ctx.message.delete()
    await lvl.remove_xp(member=member, amount=amount)


@client.command()
@commands.check(is_it_me)
async def setlvl(ctx, member:discord.Member, level:int):
    await ctx.message.delete()
    await lvl.set_level(member=member, level=level)

@client.command()
async def givexp(ctx, member:discord.Member, amount:int):
    await lvl.remove_xp(member=ctx.author, amount=amount)
    await lvl.add_xp(member=member, amount=amount)
    await ctx.send(f"Gave {amount} xp to {member.name}, Removed {amount} xp from {ctx.author.name}")


# Get the counting channel


async def get_counting_channel(guild):
    with open("database/db.json") as f:
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
        with open("database/counting.json") as f:
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

    # Check if counting channel
    await counting(msg, guild, channel, message)

    await lvl.award_xp(amount=[15, 25], message=message)

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

@client.event
async def on_command_error(ctx, error):
    cha = await client.fetch_channel(896932591620464690)
    chaem = discord.Embed(title="ERROR", description=error)
    chaem.add_field(name="Server:", value=f"{ctx.guild.id} ({ctx.guild.name})")
    chaem.add_field(name="User:", value=f"{ctx.author.id} ({ctx.author.name})")
    await cha.send(embed=chaem)

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
    # backup()
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
