import json
import datetime
import discord

def is_it_me(ctx):
    return ctx.author.id == 624076054969188363

def notblacklisted(ctx):
    with open("./database/blacklisted.json") as f:
        data = json.load(f)
    if ctx.author.id not in data:
        return True

async def plugin_enabled(ctx):
    with open("./database/db.json") as f:
        data = json.load(f)

    data = data[str(ctx.guild.id)]
    
    try:
        category = ctx.command.extras['category']
    except Exception:
        return True

    if data["settings"]['plugins'][category]:
        return True
    
    em = discord.Embed(title="This command has been disabled for your server", description=f"Ask the admins to do `?plugins enable {category}`", color=ctx.author.color)
    em.timestamp = datetime.datetime.now()

    await ctx.send(embed=em)
    return False