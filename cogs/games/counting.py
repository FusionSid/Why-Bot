import discord
import discord
from discord.ext import commands
import json
import datetime
from utils.checks import plugin_enabled
import numexpr as ne


async def get_counting_channel(guild):
    with open("./database/db.json") as f:
        data = json.load(f)
    if data[str(guild.id)]['counting_channel'] == None:
        return None
    return int(data[str(guild.id)]["counting_channel"])

# Counting


async def counting(msg, guild, channel, m):
    for i in ['this', 'that', 'is', 'not', "false", ]:
        if i in msg.lower():
            return
    try:
        msg = int(msg)
        calcm = False
    except:
        try:
            calc = ne.evaluate(msg)
            _msg = msg
            msg = int(calc)
            calcm = True
            with open("./database/db.json") as f:
                data = json.load(f)
            if data[str(guild.id)]['settings']['autocalc'] == True:
                with open("./database/goose_mode.json") as f:
                    goose_data = json.load(f)
                if str(guild.id) in goose_data and msg == 19 and "9" in str(_msg) and "10" in str(_msg) and "+" in str(_msg):
                    if goose_data[str(guild.id)]:
                        await m.reply("21")
                    else:
                        await m.reply(msg)
                else:
                    await m.reply(msg)
        except Exception:
            return
    with open("./database/db.json") as f:
        data = json.load(f)
    if data[str(m.guild.id)]['settings']['plugins']['Counting'] == False:
        return
    cc = await get_counting_channel(guild)

    if cc is None:
        return
    if channel.id == cc:
        with open("./database/counting.json") as f:
            data = json.load(f)
        with open('./database/db.json') as f:
            data2 = json.load(f)

        if data2[str(guild.id)]['lastcounter'] == None:
            data2[str(guild.id)]['lastcounter'] = m.author.id
        elif data2[str(guild.id)]['lastcounter'] == m.author.id:
            data[f"{guild.id}"] = 0
            data2[str(guild.id)]['lastcounter'] = None
            await m.add_reaction("❌")
            em = discord.Embed(title=f"{m.author.name}, You ruined it!",
                               description="Only one person at a time\nCount reset to zero", color=discord.Color.blue())
            em.timestamp = datetime.datetime.utcnow()
            with open("./database/counting.json", 'w') as f:
                json.dump(data, f, indent=4)
            with open("./database/db.json", 'w') as f:
                json.dump(data2, f, indent=4)
            return await channel.send(embed=em)
        else:
            data2[str(guild.id)]['lastcounter'] = m.author.id

        if (data[f"{guild.id}"] + 1) == msg:
            data[f"{guild.id}"] += 1
            if calcm == True:
                # await m.reply(msg)
                pass
            else:
                pass
            await m.add_reaction("✅")
        else:
            await m.add_reaction("❌")
            em = discord.Embed(title=f"{m.author.name}, You ruined it!", description=f"You were supposed to type `{(data[f'{guild.id}']+1)}`\nCount reset to zero", color=discord.Color.blue())
            em.timestamp = datetime.datetime.utcnow()
            data2[f"{guild.id}"]['lastcounter'] = None
            data[f"{guild.id}"] = 0
            await channel.send(embed=em)
        with open("./database/counting.json", 'w') as f:
            json.dump(data, f, indent=4)
        with open("./database/db.json", 'w') as f:
            json.dump(data2, f, indent=4)


class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['num', 'nrn'], extras={"category": "Counting"}, usage="numrn", help="This command shows the current number for the Counting game.\nYou can use /set Counting Channel [#channel] to set the counting channel.\nThis commamd is very useful if somebody deletes/edited their message and you dont know whats the next number", description="Current number for the counting game")
    @commands.check(plugin_enabled)
    async def numrn(self, ctx):
        guild = ctx.guild
        with open('./database/counting.json') as f:
            data = json.load(f)
        guildid = f'{guild.id}'
        numrn = data[guildid]
        em = discord.Embed(
            title=f"Current number is {numrn}", description=f"So the next number to count is: {numrn+1}", color=discord.Color.green())
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.author.bot:
            return

        channel = message.channel
        msg = message.content
        guild = message.guild

        await counting(msg, guild, channel, message)


def setup(client):
    client.add_cog(Counting(client))
