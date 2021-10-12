import discord, os, math
from discord.ext import commands
from time import ctime
from keep_alive import keep_alive
from os import listdir
from os.path import isfile, join
import json

def get_prefix(client, message):
  cd = os.getcwd()
  os.chdir(f"{cd}/Setup")
  with open(f"{message.guild.id}.json") as f:
    data = json.load(f)
  prefix = data[3]["prefix"]
  os.chdir(cd)
  return prefix

intents = discord.Intents.all()
client = commands.Bot(prefix = get_prefix(), intents=intents, help_command=None)

# On Ready
async def update_activity():
  await client.change_presence(activity=discord.Game(f"?help | {len(client.guilds)} guilds!"))
  print("Updated presence")


@client.event
async def on_ready():
  print("=======================\nConnected\n=========")
  await update_activity()


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
  os.chdir(cd)

# On Guild Join/Remove
@client.event
async def on_guild_join(guild):
  await update_activity()
  await startguildsetup(guild.id)
  embed = discord.Embed(color=discord.Color(value=0x36393e))
  embed.set_author(name="Here's some stuff to get you started:")
  embed.add_field(name="Default Prefix:", value="```?```, Can be changed later")
  embed.set_footer(text=f"Why bot is now on {len(client.guilds)} servers!")
  try:
    await guild.system_channel.send(content="**Hello! Thanks for inviting me! :wave: **", embed=embed)
    await guild.system_channel.send("PLEASE run ```?setup``` to setup the bot")
  except:
    pass


@client.event
async def on_guild_remove(guild):
  await update_activity()


def notblacklisted(ctx):
  with open("blacklisted.json") as f:
    blacklisted = json.load(f)
  for user in blacklisted:
    if ctx.author.id == user:
      return False
  return True


@client.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
  def wfcheck(m):
    return m.channel == ctx.channel and m.author == ctx.author
  await ctx.send("To setup bot you will need to copy the id's of channels.\nPlease turn on developer mode to be able to copy channel id's")
  cd = os.getcwd()
  os.chdir("{}/Setup".format(cd))
  with open(f'{ctx.guild.id}.json') as f:
      data = json.load(f)
  os.chdir(cd)

  await ctx.send("Please enter the id for the moderator/staff channel.\nThis channel will be used for logging mod commands done by the bot.\nAlso members can report messages and they will be sent to this channel for review\nType None if you dont/want one")
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

  await ctx.send("Please enter the id for the counting channel\nThis is for the counting game.\nType None if you dont/want one")
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

  await ctx.send("Please enter the id for the welcome channel\nThis is where the bot will welcome new users\nType None if you dont/want one")
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
      json.dump(data, f)

  os.chdir(cd)
  
  
# On Message
@client.event
async def on_message(message):
  if message.author == client.user:
        return
  channel = message.channel
  msg = message.content
  guild = message.guild

  bl = notblacklisted(message)
  if bl == True:
    await client.process_commands(message)
  if bl == False:
    await channel.send("You have been blacklisted from using this bot")

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

  else:
    print("An error has occured:\n{}".format(error))
    em = discord.Embed(title="Unkown Error", description="Possible bug?\nUser ?report bug <bug> to report bug")
      
  await ctx.send(embed=em, delete_after=5)


# Start the bot
def start_bot(client):
  keep_alive()
  client.remove_command("help")
  lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
  no_py = [s.replace('.py', '') for s in lst]
  startup_extensions = ["cogs." + no_py for no_py in no_py]
  try:
    for cogs in startup_extensions:
      client.load_extension(cogs)
      print(f"Loaded {cogs}")

    print("\nAll Cogs Loaded\n===============\nLogging into Discord...")
    client.run(os.environ['TOKEN'])

  except Exception as e:
    print(f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")


if __name__ == '__main__':
  start_bot(client)
