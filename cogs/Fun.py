import discord
import json
import os
import random
from discord.ext import commands
import asyncio


roastlistpy = [
    "I'd like to roast you, but it looks like God already did.",
    "You look like someone set your face on fire and then put it out with a hammer.",
    "The only thing attracted to you is gravity",
    "You’re not good looking enough to be a model, but you’re not smart enough to be anything else",
    "If you’d like to know what sexual position produces the ugliest babies, you should ask your mother.",
    "Can you speak a little louder? I can’t hear you over the sound of how stupid you are.",
    "Why are you even talking to me? So your self esteem can match your IQ?",
    "I’m not insulting you, I’m describing you.",
    "If you hide your big nose and shut your big mouth, people will think you are attractive and well-spoken.",
    "I guess God’s just making anybody these days.",
    "You're so ugly, when your mom dropped you off at school she got a fine for littering.",
    "Some babies were dropped on their heads but you were clearly thrown at a wall.",
    "They say opposites attract. If that's so, you will meet someone who is good-looking, intelligent, and cultured.",
    "I didn’t hear you. I’m busy ignoring an annoying person.",
    "I don't know what your problem is, but I'll bet it's hard to pronounce.",
    "Please excuse me while I transfer you to someone who speaks Fucktard.",
    "It must take a lot of flexibility to fit your foot in your mouth and your head up your ass at the same time.",
    "I don’t have the time nor the crayons to explain things to you",
    "I’d love to keep chatting with you, but I’d rather have AIDS",
    "I bet you swim with a t shirt on",
    "You have all the charm and charisma of a burning orphanage",
    "Your face is so oily that I’m surprised America hasn’t invaded yet.",
    "If you were any dumber, someone would need to water you twice a week",
    "If you were on fire and I had a cup of my own piss, I’d drink it",
    "Do you still love nature, despite what it did to you?",
    "The thing I dislike most about your face is that I can see it.",
    "If B.S. was music, you’d be an orchestra.",
    "You look like a before picture.",
    "I’ve heard farts more intelligent than you.",
    "You have a perfect face for radio.",
    "They say that a million monkeys on a million typewriters will eventually produce the collected works of Shakespeare. If that theory is correct, I believe you will one day say something intelligent.",
    "If you want to lose ten pounds of ugly fat, may I suggest you start with cutting off your head.",
    "You look like somebody stepped on a goldfish.",
    "I thought the trash got picked up last night, what are you still doing here?",
    "Looking the way you do must save a lot of money on halloween.",
    "I’d love to continue talking with you but my favorite commercial is on tv",
    "I'd love to keep chatting with you, but right now I have to do literally anything else.",
    "Did you get a bowl of soup with that haircut?",
    "If you don’t like what I say about you, it would be a good idea to improve yourself.",
    "Does being that ugly require a license?",
    "You could throw a rock at the ground and miss",
    "There’s no one in this world like you. Or at least I hope so.",
    "You look like a man, and you need to lose some weight.",
    "Did you cancel your barbecue?  Because your grill is messed up",
    "Some people make millions.  You make memes.",
    "Did you forget to wipe or is that your natural scent?",
    "I missed you this week, but my aim is improving.",
    "I'm surprised you've made it this far without being eaten.",
    "Your body looks like your head is inflating a water balloon.",
    "Your mother was a hamster.",
    "How do you make an idiot wait?",
    "If balls were dynamite, you wouldn't have enough to kill a fish.",
    "I'd like to roast you, but I'm too busy judging your choices.",
    "You are the worst part of everybody's day.",
    "If your face were scrambled it would improve your looks.",
    "I hope you don't feel the way you look.",
    "In the book of Who's Who, you are listed as What's That?",
    "It's surprising to me that a pig's bladder on a stick has gotten so far in life.",
    "Sorry.  I'm on the toilet and I can only deal with one shit at a time.",
    "If you fell into a river it would be unfortunate, but if anyone pulled you out it would be a disaster.",
    "You are the discount version of whatever celebrity you look like.",
    "When you go to the dentist, he needs anaesthetic.",
    "You suck dick for bus fare and then walk home.",
    "The fact that you are still alive is evidence that natural disasters are poorly distributed.",
    "You are so dumb you can't fart and chew gum at the same time.",
    "I was going to give you a nasty look, but I see you already have one.",
    "Me think'st thou are a general offence and every man should beat thee.",
    "I don't try to explain myself to idiots like you.  I'm not the Fucktard Whisperer.",
    "Your mom circulates like a public key, servicing more requests than HTTP.",
    "Your mom is so fat and dumb, the only reason she opened her email is because she heard it contained spam.",
    "Your mom is so fat, she has to iron her pants in the driveway.",
    "Your face invites a slap.",
    "The only way you could get laid is if you crawled up a chicken's ass and waited."
]


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rps(self, ctx, rps:str):
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


    @commands.command()
    async def roast(self, ctx):
        roast = random.choice(roastlistpy)
        em = discord.Embed(title=roast)
        await ctx.send(embed=em)


    @commands.command()
    async def dm(self, ctx, member: discord.Member, *, message):
        await ctx.channel.purge(limit=1)
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)


    @commands.command()
    async def sendroast(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        message = random.choice(roastlistpy)
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


    @commands.command()
    async def embed(self, ctx, fields:str, extra:int, img:str=None, channel:int=None):
        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author
        em = discord.Embed()
        if fields == "t":
            await ctx.send("Enter Title:", delete_after=5)
            title = await self.client.wait_for("message", check=wfcheck)
            em.title = title.content
        if fields == "d":
            await ctx.send("Enter Description:", delete_after=5)
            desc = await self.client.wait_for("message", check=wfcheck)
            em.description = desc.content
        if fields == "td":
            await ctx.send("Enter Title:", delete_after=5)
            title = await self.client.wait_for("message", check=wfcheck)
            em.title = title.content

            await ctx.send("Enter Description:", delete_after=5)
            desc = await self.client.wait_for("message", check=wfcheck)
            em.description = desc.content

        if extra == 0:
            pass

        else:
            for i in range(extra):
                await ctx.send("Enter Name:", delete_after=5)
                name = await self.client.wait_for("message", check=wfcheck)

                await ctx.send("Enter Value:", delete_after=5)
                value = await self.client.wait_for("message", check=wfcheck)
                
                em.add_field(name=name.content, value=value.content)
        
        if img == None:
            await ctx.send(embed=em)
            return
        if img.lower() == 'none':
            pass  
        else:
          em.set_image(url=img)
          await ctx.send(embed=em)
          return
        if channel == None:
          return
        else:
          cha = await self.client.fetch_channel(channel)
          await cha.send(embed=em)


    @commands.command()
    async def say(self, ctx, *, text):
      await ctx.send(text)
  

    @commands.command()
    async def numrn(self, ctx):
        guild = ctx.guild
        cd = os.getcwd()
        os.chdir("/home/runner/Why-Bot/")
        with open ('counting.json') as f:
            data = json.load(f)
        guildid = f'{guild.id}'
        numrn = data[guildid]
        await ctx.send(f"Current number is {numrn}")

    @commands.command()
    async def yesorno(self, ctx, *, message):
      msg = await ctx.send(embed=discord.Embed(title="Yah or Nah?", description=message))
      await msg.add_reaction('👍')
      await msg.add_reaction('👎')


    @commands.command(pass_context=True)
    async def quickpoll(self, ctx, question, *options: str):
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await self.bot.add_reaction(react_message, reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await self.bot.edit_message(react_message, embed=embed)


    @commands.command(pass_context=True)
    async def tally(self, ctx, id):
        poll_message = await self.bot.get_message(ctx.message.channel, id)
        if not poll_message.embeds:
            return
        embed = poll_message.embeds[0]
        if poll_message.author != ctx.message.server.me:
            return
        if not embed['footer']['text'].startswith('Poll ID:'):
            return
        unformatted_options = [x.strip() for x in embed['description'].split('\n')]
        opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
            else {x[:1]: x[2:] for x in unformatted_options}
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [ctx.message.server.me.id]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactors = await self.bot.get_reaction_users(reaction)
                for reactor in reactors:
                    if reactor.id not in voters:
                        tally[reaction.emoji] += 1
                        voters.append(reactor.id)

        output = 'Results of the poll for "{}":\n'.format(embed['title']) + \
                 '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
        await self.bot.say(output)
    
def setup(client):
    client.add_cog(Fun(client))


