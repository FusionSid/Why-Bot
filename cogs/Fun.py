import discord
import json
import os
import random
from discord.ext import commands
import asyncio
from discord.utils import get
import dotenv
from discord import Option
from discord.commands import slash_command
import requests

dotenv.load_dotenv()

async def get_roast():
    with open('./database/roastlist.json') as f:
        data = json.load(f)
    return random.choice(data)

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rockpaperscissors'])
    async def rps(self, ctx, rps: str):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors")
        rps = rps.lower()
        if rps == 'rock':
            if cpu_choice == 'rock':
                em.description = "It's a tie!"
            elif cpu_choice == 'scissors':
                em.description = "You win!"
            elif cpu_choice == 'paper':
                em.description = "You lose!"

        elif rps == 'paper':
            if cpu_choice == 'paper':
                em.description = "It's a tie!"
            elif cpu_choice == 'rock':
                em.description = "You win!"
            elif cpu_choice == 'scissors':
                em.description = "You lose!"

        elif rps == 'scissors':
            if cpu_choice == 'scissors':
                em.description = "It's a tie!"
            elif cpu_choice == 'paper':
                em.description = "You win!"
            elif cpu_choice == 'rock':
                em.description = "You lose!"

        else:
            em.description = "Invalid Input"

        em.add_field(name="Your Choice", value=rps)
        em.add_field(name="Bot Choice", value=cpu_choice)
        await ctx.send(embed=em)


    @commands.command(aliases=['roastme'])
    async def roast(self, ctx):
        await ctx.message.delete()
        roast = await get_roast()
        em = discord.Embed(title=roast)
        await ctx.send(embed=em)
    

    @commands.command(aliases=['sendmsg'])
    async def dm(self, ctx, member: discord.Member, *, message):
        await ctx.message.delete()
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)
    

    @commands.command(aliases=['sr'])
    async def sendroast(self, ctx, member: discord.Member):
        await ctx.message.delete()
        message = await get_roast()
        embeddm = discord.Embed(
            title=message, description="Imagine being roasted by a bot")
        await member.send(embed=embeddm)


    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        _8ballans = [
            "As I see it, yes",
            "It is certain",
            "It is decidedly so",
            "Most likely",
            "Outlook good",
            "Signs point to yes",
            "Without a doubt",
            "Yes",
            "Yes - definitely",
            "You may rely on it",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
        ]
        em = discord.Embed(title="__8 Ball__",
                           description=f"{question}\nAnswer: {random.choice(_8ballans)}")
        await ctx.send(embed=em)

    @commands.command(aliases=['em'])
    async def embed(self, ctx, fields: str, extra: int= None, channel: int = None,*, img=None):
        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author
        em = discord.Embed()
        if fields == "t":
            await ctx.send("Enter Title:", delete_after=2)
            title = await self.client.wait_for("message", check=wfcheck)
            await title.delete()
            em.title = title.content
        if fields == "d":
            await ctx.send("Enter Description:", delete_after=2)
            desc = await self.client.wait_for("message", check=wfcheck)
            await desc.delete()
            em.description = desc.content
        if fields == "td":
            await ctx.send("Enter Title:", delete_after=2)
            title = await self.client.wait_for("message", check=wfcheck)
            await title.delete()
            em.title = title.content

            await ctx.send("Enter Description:", delete_after=2)
            desc = await self.client.wait_for("message", check=wfcheck)
            await desc.delete()
            em.description = desc.content

        if extra == None:
            pass

        else:
            for i in range(extra):
                await ctx.send("Enter Name:", delete_after=2)
                name = await self.client.wait_for("message", check=wfcheck)
                await name.delete()

                await ctx.send("Enter Value:", delete_after=2)
                value = await self.client.wait_for("message", check=wfcheck)
                await value.delete()

                em.add_field(name=name.content, value=value.content)

        if img == None:
          pass
        else:
          try:
            em.set_image(url=img)
          except:
            await ctx.send("Invalid Image Url", delete_after=2)

        if channel == 0:
          channel = None
        if channel == None:
            await ctx.send(embed=em)
        else:
            cha = await self.client.fetch_channel(channel)
            await cha.send(embed=em)

    @commands.command(aliases=['noembed'])
    async def say(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(text)
    
   

    @commands.command(aliases=['num'])
    async def numrn(self, ctx):
        guild = ctx.guild
        with open('./database/counting.json') as f:
            data = json.load(f)
        guildid = f'{guild.id}'
        numrn = data[guildid]
        await ctx.send(f"Current number is {numrn}")

    @commands.command(aliases=['yahornah', 'yn'])
    async def yesorno(self, ctx, *, message):
        msg = await ctx.send(embed=discord.Embed(title="Yah or Nah?", description=message))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @commands.command(pass_context=True, aliases=['makepoll', 'question'])
    async def poll(self, ctx, time: int, question, *options: str):
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣',
                         '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        reacting = []
        for x, option in enumerate(options):
            description += '\n{} = {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description))
        embed.set_footer(text="Please don't vote twice")
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
            reacting.append(reaction)
        await asyncio.sleep(time)
        message = await ctx.channel.fetch_message(react_message.id)
        results = {}
        for i in reacting:
            reaction = get(message.reactions, emoji=i)
            count = reaction.count-1
            results[i] = f"{count} votes"
        results = f'{results}'
        results = results.replace("{", "")
        results = results.replace("}", "")
        results = results.replace("'", "")
        results = results.replace(",", "\n")
        results = results.replace(":", " got")
        embed.description = f"{embed.description}\n** **"
        embed.add_field(name=f"Results:", value=f"** **\n {results}")
        embed.set_footer(text="Voting is closed")
        await message.edit(embed=embed)
        await ctx.send(embed=discord.Embed(title=f"Poll Results For {question}:", description=f"Votes:\n {results}"))


def setup(client):
    client.add_cog(Fun(client))
