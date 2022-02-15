import json

def is_it_me(ctx):
    return ctx.author.id == 624076054969188363

def notblacklisted(ctx):
    with open("./database/blacklisted.json") as f:
        data = json.load(f)
    if ctx.author.id not in data:
        return True

async def plugin_enabled(ctx):
    categories = ["Counting", "Fun", "Leveling", "Logs", "Minecraft", "Moderation", "Music", "Ping", "Search", 'Settings', "Text", "Ticket", "Utilities", "Voice", "Welcome", "Economy", "Games"]
    if ctx.cog is None:
        return True
    with open('./database/db.json') as f:
        data = json.load(f)
        settings = data[str(ctx.guild.id)]['settings']
    try:
      if settings["plugins"][ctx.cog.qualified_name] == False:
        await ctx.send("This command had been disabled", delete_after=5)
        return False
      else:
          return True
    except:
      return True
