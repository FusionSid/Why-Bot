import discord
import json
import os
import random
from discord.ext import commands

CD = '/home/runner/Why-Bot/cogs/'
DBPATH = '/home/runner/Why-Bot/MainDB/' #leveling{ctx.guild.id]

async def update_data(data, member):
    if not member.id in data:
        data[member.id] = []
        data[member.id]['exp'] = 0
        data[member.id]['level'] = 0
        data[member.id]['guild'] = member.guild.id


async def add_exp(data, member, exp):
    data[member.id]['exp'] += exp


async def level_up(data, member, channel):
    exp = data[member.id]['exp']
    lvl_start = data[member.id]['level']
    lvl_end = int(exp ** (1/4))

    if lvl_start < lvl_end:
        await channel.send(f'{member.mention} has leveled up to {lvl_end}')
    data[member.id]['level'] = lvl_end


class Leveling(commands.Cog):

    @commands.Cog.listener()
    async def on_member_join(self, member):
        os.chdir(DBPATH)
        with open('leveling.json', 'r') as f:
            data = json.load(f)
        os.chdir(CD)

        await update_data(data, member)

        os.chdir(DBPATH)
        with open('leveling.json', 'w') as f:
            json.dump(data, f)
        os.chdir(CD)


    @commands.Cog.listener()
    async def on_message(self, message):
        os.chdir(DBPATH)
        with open('leveling.json', 'r') as f:
            data = json.load(f)
        os.chdir(CD)

        await update_data(data, message.author.id)

        exp = random.randint(25, 75)
        await add_exp(data, message.author, exp)

        await level_up(data, message.author, message.channel)
        
        os.chdir(DBPATH)
        with open('leveling.json', 'w') as f:
            json.dump(data, f)
        os.chdir(CD)

    @commands.command()
    async def rank(self, ctx, member:discord.Member=None):
        name = member.name
        if member == None:
            memberid = ctx.author.id
        else:
            memberid = member.id
        
        os.chdir(DBPATH)
        with open('leveling.json', 'r') as f:
            data = json.load(f)
        os.chdir(CD)

        return

