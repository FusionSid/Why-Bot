import discord, os, math
from discord.ext import commands
from time import ctime
from os import listdir
from os.path import isfile, join

prefix = "?"
intents = discord.Intents.all()
client = commands.Bot(prefix, intents=intents, help_command=None)

# On Ready
async def update_activity():
  await client.change_presence(activity=discord.Game(f"?help | {len(client.guilds)} guilds!"))
  print("Updated presence")


@client.event
async def on_ready():
  print("=======================\nConnected\n=========")
  await update_activity()


# On Guild Join/Remove
@client.event
async def on_guild_join(guild):
  await update_activity()
  embed = discord.Embed(color=discord.Color(value=0x36393e))
  embed.set_author(name="Here's some stuff to get you started:")
  embed.add_field(name="Prefix", value="Default prefix:`?`, Can be changed later")
  embed.set_footer(text=f"Why bot is now on {len(client.guilds)} servers!")
  try:
    await guild.system_channel.send(content="**Hello! Thanks for inviting me! :wave: **", embed=embed)
    await guild.system_channel.send("Please run `?setup` to setup the bot")
  except:
    pass


@client.event
async def on_guild_remove():
  await update_activity()


# On Message
@client.event
async def on_message(message):
  if message.author == client.user:
        return
  channel = message.channel
  msg = message.content

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

  else:
    print("An error has occured:\n{}".format(error))
    em = discord.Embed(title="Unkown Error", description="Possible bug?\nUser ?report bug <bug> to report bug")
      
  await ctx.send(embed=em, delete_after=5)


# Start the bot
def start_bot(client):
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