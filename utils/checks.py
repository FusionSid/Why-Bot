import json

def is_it_me(ctx):
    return ctx.author.id == 624076054969188363

def notblacklisted(ctx):
    with open("./database/blacklisted.json") as f:
        data = json.load(f)
    if ctx.author.id not in data:
        return True
