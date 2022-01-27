import json

def is_it_me(ctx):
    return ctx.author.id == 624076054969188363

def notblacklisted(ctx):
    with open("./database/blacklisted.json") as f:
        data = json.load(f)
    if ctx.author.id not in data:
        return True

async def plugin_enabled(ctx):
    if ctx.cog is None:
        return True
    with open('./database/db.json') as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == ctx.guild.id:
            settings = i['settings']
    try:
      if settings["plugins"][ctx.cog.qualified_name] == False:
        await ctx.send("This command had been disabled", delete_after=5)
        return False
      else:
          return True
    except:
      return True
