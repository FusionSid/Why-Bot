import time as py_time
import asyncio
import datetime

import discord
from discord.utils import get
from discord.ext import commands


from utils import blacklisted

class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Makes a Yah or Nah poll")
    @commands.check(blacklisted)
    async def yesorno(self, ctx, *, message):
        msg = await ctx.send(embed=discord.Embed(title="Yah or Nah?", description=message, color=ctx.author.color))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')


    @commands.command()
    @commands.check(blacklisted)
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

        embed = discord.Embed(title=f"{ctx.author.name} asks: {question}", description=''.join(description), color=ctx.author.color)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Please don't vote twice")
        timern = py_time.time()
        t = int(timern) + time
        embed.add_field(name="Voting ends in:", value=f"<t:{t}:R>")
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
        results = "\n".join([f"{key} got {value}" for key, value in results.items()])
        results_message = await message.reply(embed=discord.Embed(title=f"Poll Results For {question}:", description=f"**Votes:**\n {results}", color=ctx.author.color))
        embed.set_footer(text="Voting is closed")
        embed.fields = []
        embed.add_field(name="Voting is now closed", value=f"[Vote Results]({results_message.jump_url})")
        return await message.edit(embed=embed)

def setup(client):
    client.add_cog(Poll(client))