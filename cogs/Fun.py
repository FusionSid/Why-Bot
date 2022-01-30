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
from utils.other import log
from utils.checks import plugin_enabled
from discord.ui import Button, View

dotenv.load_dotenv()

async def get_roast():
    with open('./database/roastlist.json') as f:
        data = json.load(f)
    return random.choice(data)

class MyView(View):
    def __init__(self):
        super().__init__(timeout=500)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Claim", custom_id="b1")
    async def button1(self, interaction, button):
        await interaction.response.send_message("https://imgur.com/NQinKJB", empherial=True)
        button.style = discord.ButtonStyle.red
        button.label = "Claimed"
        button.disabled=True
        await interaction.response.edit_message(view=self)

    
class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(plugin_enabled)
    async def nitro(self,ctx):
        em = discord.Embed(title="Claim Nitro")
        em.set_image(url="https://gudstory.s3.us-east-2.amazonaws.com/wp-content/uploads/2021/02/08150513/Discord-Nitro.png")
        await ctx.send(embed=em, view=MyView())

    @commands.command(aliases=['rockpaperscissors'], extras={"category":"Fun"}, usage="rps [rock/paper/scissors]", help="This command if for playing rock paper scissors with the bot.", description="Play a game of rock paper scissors against the bot")
    @commands.check(plugin_enabled)
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


    @commands.command(aliases=['roastme'], extras={"category":"Fun"}, usage="roast", help="The bot sends a roast into the chat", description="Bot roasts you")
    @commands.check(plugin_enabled)
    async def roast(self, ctx):
        await ctx.message.delete()
        roast = await get_roast()
        em = discord.Embed(title=roast)
        await ctx.send(embed=em)
    

    @commands.command(aliases=['sendmsg'], extras={"category":"Fun"}, usage="dm [@user] [message]", help="You can use this command to send a dm to a user. The bot will send the message to the user.", description="Bot sends a message on your behalf")
    @commands.check(plugin_enabled)
    async def dm(self, ctx, member: discord.Member, *, message):
        await ctx.message.delete()
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)
    

    @commands.command(aliases=['sr'], extras={"category":"Fun"}, usage="sendroast [@user]", help="The bot picks a random roast from a list and send it to a person of your choosing", description="The bots send a roast to someone on your behalf")
    @commands.check(plugin_enabled)
    async def sendroast(self, ctx, member: discord.Member):
        await ctx.message.delete()
        message = await get_roast()
        embeddm = discord.Embed(
            title=message, description="Imagine being roasted by a bot")
        await member.send(embed=embeddm)


    @commands.command(aliases=['8ball'], extras={"category":"Fun"}, name="8 ball", usage="8ball [question]", help="The bot asks the magical 8ball and gets you the result", description="Asks the 8ball a question")
    @commands.check(plugin_enabled)
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

    @commands.command(aliases=['em'], extras={"category":"Fun"}, usage="embed [t/d/td] [fields(optional)] [channel(optional)] [img(optional)]", help="This command is used to make an embeded message.\nThe bot will create a nice embed and then send it to the channel youre in or the channel you want.", description="Makes an embed")
    @commands.check(plugin_enabled)
    async def embed(self, ctx, fields: str, extra: int= None, channel: int = None,*, img=None):
        await ctx.message.delete()
        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author
        em = discord.Embed()
        if fields == "t":
            await ctx.send("Enter Title:", delete_after=2)
            title = await self.client.wait_for("message", check=wfcheck, timeout=300)
            await title.delete()
            em.title = title.content
        if fields == "d":
            await ctx.send("Enter Description:", delete_after=2)
            desc = await self.client.wait_for("message", check=wfcheck, timeout=300)
            await desc.delete()
            em.description = desc.content
        if fields == "td":
            await ctx.send("Enter Title:", delete_after=2)
            title = await self.client.wait_for("message", check=wfcheck, timeout=300)
            await title.delete()
            em.title = title.content

            await ctx.send("Enter Description:", delete_after=2)
            desc = await self.client.wait_for("message", check=wfcheck, timeout=300)
            await desc.delete()
            em.description = desc.content

        if extra == None:
            pass

        else:
            for i in range(extra):
                await ctx.send("Enter Name:", delete_after=2)
                name = await self.client.wait_for("message", check=wfcheck, timeout=300)
                await name.delete()

                await ctx.send("Enter Value:", delete_after=2)
                value = await self.client.wait_for("message", check=wfcheck, timeout=300)
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

    @commands.command(aliases=['noembed'], extras={"category":"Fun"}, usage="say [text]", help="The bot speaks text that you want", description="Bot sends text")
    @commands.check(plugin_enabled)
    async def say(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(text)

    # Polls

    @commands.command(aliases=['yahornah', 'yn'], extras={"category":"Fun"}, usage="yesorno [question]", help="This command makes a small poll which users can vote either yes, or no", description="Makes a Yah or Nah poll")
    @commands.check(plugin_enabled)
    async def yesorno(self, ctx, *, message):
        msg = await ctx.send(embed=discord.Embed(title="Yah or Nah?", description=message))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @commands.command(pass_context=True, aliases=['makepoll', 'question'], extras={"category":"Fun"}, usage="poll [time:seconds] '[title]' [each option followed by a space]", help="This command creates a poll which can have up to 10 options to vote to.\nThe poll will last for a certain amount of seconds that you choose, and after those seconds you will get the results.", description="Makes a poll")
    @commands.check(plugin_enabled)
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
        # await message.edit(embed=embed)
        await message.reply(embed=discord.Embed(title=f"Poll Results For {question}:", description=f"**Votes:**\n {results}"))


def setup(client):
    client.add_cog(Fun(client))
