import json

async def blacklisted(ctx):
    author_id = ctx.author.id

    with open("./database/blacklisted.json") as f:
        data = json.load(f)

    if author_id in data:
        await ctx.send("You have been blacklisted from using this bot")
        return False
    return True