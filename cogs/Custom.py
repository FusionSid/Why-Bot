import discord
from discord.commands.commands import command
from discord.ext import commands
import json

async def get_data(user_id):
    with open('./database/userdb.json') as f:
        data = json.load(f)
    for user in data:
        if user["user_id"] == user_id:
            return user
    return None

class Custom(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.group(aliases=["on_pinged", 'pinged'])
    async def onpinged(self, ctx):
        if ctx.invoked_subcommand is None:
            user = await get_data(ctx.author.id)
            if user == None:
                return
            on_pinged_message = user['on_pinged']
            em = discord.Embed()

            if on_pinged_message["title"] == None and on_pinged_message["description"] == None:
                return await ctx.send(embed=discord.Embed(title="You have no on pinged message set.",description=f"Use `{ctx.prefix}onpinged set` to set one"))

            if on_pinged_message["title"] == None:
                pass
            else:
                em.title=on_pinged_message["title"]

            if on_pinged_message["description"] == None:
                pass
            else:
                em.description=on_pinged_message["description"]

            if on_pinged_message["color"] == None:
                pass
            else:
                em.color=on_pinged_message["color"]

            await ctx.send(embed=em)


    @onpinged.command()
    async def set(self, ctx):
        user = await get_data(ctx.author.id)
        if user == None:
            return
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        colors = {
            "red":0xFF0000,
            "orange":0xFFA500,
            "yellow":0xFFFF00,
            "green":0x00FF00,
            "blue":0x0000FF,
            "purple":0x800080,
            "pink":0xFFC0CB,
            "white":0xFFFFFF,
            "black":0x000000,
        }
        await ctx.send("Type the title for the embed (or type none if you dont want one)")
        title = await self.client.wait_for("message", check=check, timeout=300)
        title = title.content
        if title.lower() == 'none':
            title = None

        await ctx.send("Type the description for the embed (or type none if you dont want one)")
        description = await self.client.wait_for("message", check=check, timeout=300)
        description = description.content
        if description.lower() == 'none':
            description = None

        await ctx.send("Choose color from this list:\n[red, orange, yellow, green. blue, purple, pink, white, black]\nEnter the color you want (or type none if you want the default:)")
        color = await self.client.wait_for("message", check=check, timeout=300)
        color = color.content
        color = color.lower()

        if color.lower() in colors.keys():
            color = colors[color]
        else:
            color = None
        
        with open('./database/userdb.json') as f:
            data = json.load(f)

        for i in data:
            if i['user_id'] == ctx.author.id:
                i['on_pinged']['title'] = title
                i['on_pinged']['description'] = description
                i['on_pinged']['color'] = color
    
        with open("./database/userdb.json", 'w') as f:
            json.dump(data, f, indent=4)
        

    @onpinged.command()
    async def clear(self, ctx):
        with open("./database/userdb.json") as f:
            data = json.load(f)
        for i in data:
            if i["user_id"] == ctx.author.id:
                i["on_pinged"]["title"] = None
                i["on_pinged"]["description"] = None
                i["on_pinged"]["color"] = None
        with open("./database/userdb.json", 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.send("On Pinged Reset")


    @commands.Cog.listener()
    async def on_message(self, message):
        with open("./database/userdb.json") as f:
            data = json.load(f)
        for i in data:
            if message.reference is None:
              return
            if f"<@!{i['user_id']}>" in message.content:
                em = discord.Embed()
                em.title = i["on_pinged"]["title"]
                em.description= i["on_pinged"]["description"]
                if i["on_pinged"]["color"] == None:
                  pass
                else:
                  em.color = i["on_pinged"]["color"]
                try:
                  return await message.reply(embed=em)
                except:
                  return await message.channel.send(embed=em)
            if f"<@{i['user_id']}>" in message.content:
                em = discord.Embed()
                em.title = i["on_pinged"]["title"]
                em.description= i["on_pinged"]["description"]
                if i["on_pinged"]["color"] == None:
                  pass
                else:
                  em.color = i["on_pinged"]["color"]
                try:
                  return await message.reply(embed=em)
                except:
                  return await message.channel.send(embed=em)

def setup(client):
    client.add_cog(Custom(client))