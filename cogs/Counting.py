import discord
import discord
from discord.ext import commands
import json
from utils.checks import plugin_enabled
from utils.other import log
import numexpr as ne
import numpy


async def get_counting_channel(guild):
    with open("./database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == guild.id:
          if i['counting_channel'] == None:
              return None
          return int(i["counting_channel"])

# Counting


async def counting(msg, guild, channel, m):
    if "this" in msg:
      return
    try:
        msg = int(msg)
        calcm = False
    except:
        try:
          calc = ne.evaluate(msg)
          msg = int(calc)
          calcm = True
          with open("./database/db.json") as f:
            data = json.load(f)
          for i in data:
            if i['guild_id'] == guild.id:
              if i['settings']['autocalc'] == True:
                await m.reply(msg)
        except:
          return

    cc = await get_counting_channel(guild)

    if cc is None:
        return
    if channel.id == cc:
        with open("./database/counting.json") as f:
            data = json.load(f)
        with open('./database/db.json') as f:
            dataa = json.load(f)
        for i in dataa:
            if i['guild_id'] == guild.id:
                if i['lastcounter'] == None:
                    i['lastcounter'] = m.author.id
                    break
                elif i['lastcounter'] == m.author.id:
                    data[f"{guild.id}"] = 0
                    i['lastcounter'] = None
                    await m.add_reaction("❌")
                    em = discord.Embed(title=f"{m.author.name}, You ruined it!", description="Only one person at a time\nCount reset to zero")
                    with open("./database/counting.json", 'w') as f:
                        json.dump(data, f, indent=4)
                    with open("./database/db.json", 'w') as f:
                        json.dump(dataa, f, indent=4)
                    return await channel.send(embed=em)
                else:
                    i['lastcounter'] = m.author.id
                    break
                    
        if (data[f"{guild.id}"] + 1) == msg:
            data[f"{guild.id}"] += 1
            if calcm == True:
              #await m.reply(msg)
              pass
            else:
              pass
            await m.add_reaction("✅")
        else:
            await m.add_reaction("❌")
            em = discord.Embed(title=f"{m.author.name}, You ruined it!", description=f"You were supposed to type `{(data[f'{guild.id}']+1)}`\nCount reset to zero")
            i['lastcounter'] = None
            data[f"{guild.id}"] = 0
            await channel.send(embed=em)
        with open("./database/counting.json", 'w') as f:
            json.dump(data, f, indent=4)
        with open("./database/db.json", 'w') as f:
            json.dump(dataa, f, indent=4)


class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=['num'])
    @commands.check(plugin_enabled)
    async def numrn(self, ctx):
        guild = ctx.guild
        with open('./database/counting.json') as f:
            data = json.load(f)
        guildid = f'{guild.id}'
        numrn = data[guildid]
        await ctx.send(f"Current number is {numrn}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
          return
        with open("./database/db.json") as f:
          data = json.load(f)
        for i in data:
          if i["guild_id"] == message.guild.id:
            if i['settings']['plugins']['Counting'] == False:
              return
            else:
              pass

        channel = message.channel
        msg = message.content
        guild = message.guild

        await counting(msg, guild, channel, message)


def setup(client):
    client.add_cog(Counting(client))
