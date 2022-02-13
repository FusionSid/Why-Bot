import discord
import json
import os
import random
from discord.ext import commands
import asyncio
from discord.utils import get
import dotenv
from utils.checks import plugin_enabled
import datetime
import shlex
from discord.ui import View

dotenv.load_dotenv()

async def get_roast():
    with open('./database/roastlist.json') as f:
        data = json.load(f)
    return random.choice(data)

class MyView(View):
    def __init__(self):
        super().__init__(timeout=500)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Claim", custom_id="b1")
    async def button1(self, button, interaction):
        button.style = discord.ButtonStyle.red
        button.label = "Claimed"
        button.disabled=True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("https://imgur.com/NQinKJB",ephemeral=True)
        with open("./database/other.json") as f:
            data = json.load(f)
        data["claimrickroll"] += 1
        count = data["claimrickroll"]
        await interaction.followup.send(f"You were the {count} person to get rick rolled",ephemeral=True)
        with open("./database/other.json", 'w') as f:
            json.dump(data, f, indent=4)

def is_it_me(ctx):
    return ctx.author.id == 624076054969188363

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="This command gives you free coins. Click claim.", extras={"category":"Fun"}, usage="claim", description="Free Coins")
    @commands.check(plugin_enabled)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def claim(self,ctx):
        em = discord.Embed(title="Claim 100k Why Coins", color=ctx.author.color)
        await ctx.send(embed=em, view=MyView())
        
    @commands.command()
    @commands.check(is_it_me)
    @commands.check(plugin_enabled)
    async def nitro(self,ctx):
        em = discord.Embed(title="Claim Free Nitro", color=ctx.author.color)
        em.set_image(url="https://gudstory.s3.us-east-2.amazonaws.com/wp-content/uploads/2021/02/08150513/Discord-Nitro.png")
        await ctx.send(embed=em, view=MyView())
        
    @commands.command(aliases=['rockpaperscissors'], extras={"category":"Fun"}, usage="rps [rock/paper/scissors]", help="This command if for playing rock paper scissors with the bot.", description="Play a game of rock paper scissors against the bot")
    @commands.check(plugin_enabled)
    async def rps(self, ctx, rps: str):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors", color=ctx.author.color)
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
        em = discord.Embed(title=roast, color=ctx.author.color)
        await ctx.send(embed=em)
    

    @commands.command(aliases=['sendmsg'], extras={"category":"Fun"}, usage="dm [@user] [message]", help="You can use this command to send a dm to a user. The bot will send the message to the user.", description="Bot sends a message on your behalf")
    @commands.check(plugin_enabled)
    async def dm(self, ctx, member: discord.Member, *, message):
        await ctx.message.delete()
        embeddm = discord.Embed(title=message, color=ctx.author.color)
        await member.send(embed=embeddm)
    

    @commands.command(aliases=['sr'], extras={"category":"Fun"}, usage="sendroast [@user]", help="The bot picks a random roast from a list and send it to a person of your choosing", description="The bots send a roast to someone on your behalf")
    @commands.check(plugin_enabled)
    async def sendroast(self, ctx, member: discord.Member):
        await ctx.message.delete()
        message = await get_roast()
        embeddm = discord.Embed(
            title=message, description="Imagine being roasted by a bot", color=ctx.author.color)
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

    @commands.command(aliases=['em'], extras={"category":"Fun"}, usage="embed --title test --desc test --channel 123456789 --color blue --timestamp yes --fields 2", help="This command is used to make an embeded message.\nThe bot will create a nice embed and then send it to the channel youre in or the channel you want.", description="Makes an embed")
    @commands.check(plugin_enabled)
    async def embed(self, ctx, *, kwargs):
        colors = {
            "none" : None,
            "blue": discord.Color.blue(),
            "blurple": discord.Color.blurple(),
            "brand_green": discord.Color.brand_green(),
            "brand_red": discord.Color.brand_red(),
            "dark_blue": discord.Color.dark_blue(),
            "dark_gold": discord.Color.dark_gold(),
            "dark_gray": discord.Color.dark_gray(),
            "dark_green": discord.Color.dark_green(),
            "dark_grey": discord.Color.dark_grey(),
            "dark_magenta": discord.Color.dark_magenta(),
            "dark_orange": discord.Color.dark_orange(),
            "dark_purple": discord.Color.dark_purple(),
            "dark_red": discord.Color.dark_red(),
            "dark_teal": discord.Color.dark_teal(),
            "dark_theme": discord.Color.dark_theme(),
            "darker_gray": discord.Color.darker_gray(),
            "darker_grey": discord.Color.darker_grey(),
            "fuchsia": discord.Color.fuchsia(),
            "gold": discord.Color.gold(),
            "green": discord.Color.green(),
            "greyple": discord.Color.greyple(),
            "light_gray": discord.Color.light_gray(),
            "light_grey": discord.Color.light_grey(),
            "lighter_gray": discord.Color.lighter_gray(),
            "lighter_grey": discord.Color.lighter_grey(),
            "magenta": discord.Color.magenta(),
            "nitro_pink": discord.Color.nitro_pink(),
            "og_blurple": discord.Color.og_blurple(),
            "orange": discord.Color.orange(),
            "purple": discord.Color.purple(),
            "random": discord.Color.random(),
            "red": discord.Color.red(),
            "teal": discord.Color.teal(),
        }

        colorlist = []
        for c in colors:
            colorlist.append(c)
            
        def wait_for_check(m):
            return m.author == ctx.author and m.channel == ctx.message.channel

        em = discord.Embed()

        kwargs = shlex.split(kwargs)
        args = {}

        for index in range(len(kwargs)):
            if index % 2 == 0:
                args[kwargs[index].lstrip("--")] = kwargs[index+1]
            index += 0

        channel = ctx.message.channel

        for key, value in args.items():
            print(len(args))
            if key.lower() == "title":
                em.title = value
            elif key.lower() == "description" or key.lower() == "desc":
                em.description = value
            elif key.lower() == "channel":
                channel = await self.client.fetch_channel(int(value))
            elif key.lower() == "img" or key.lower() == "image":
                em.set_image(url=value)
            elif key.lower() == "color" or key.lower() == "colour":
                if value.lower() == "list" or value.lower() == "help":
                    return await ctx.send(", ".join(colorlist))
                if value.lower() not in colorlist:
                    await ctx.send("Color not found", delete_after=2)
                    em.color = ctx.author.color
                else:
                    em.color = colors[value.lower()]
            elif key.lower() == "fields":
                vint = False
                try:
                    int(value) 
                    vint= True
                except:
                    vint = False
                
                if vint is True:
                    for i in range(int(value)):
                        entername = await ctx.send("Enter Name:")
                        name = await self.client.wait_for("message", check=wait_for_check, timeout=300)
                        await name.delete()

                        entervalue = await ctx.send("Enter Value:")
                        value = await self.client.wait_for("message", check=wait_for_check, timeout=300)
                        await entername.delete()
                        await entervalue.delete()
                        await value.delete()

                        em.add_field(name=name.content, value=value.content)
            elif key.lower() in ["timestamp", "time"] and value.lower() in ["true", "yes"]:
                em.timestamp = datetime.datetime.now()
            else:
                pass

        await channel.send(embed=em)

    @commands.command(aliases=['noembed'], extras={"category":"Fun"}, usage="say [text]", help="The bot speaks text that you want", description="Bot sends text")
    @commands.check(plugin_enabled)
    async def say(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(text)

    @commands.command()
    @commands.check(plugin_enabled)
    async def whypp(self, ctx):
        await ctx.send(
"""
**|   WHY PP   |**
**         **<:why:932912321544728576> 
        <:why:932912321544728576> 
        <:why:932912321544728576> 
        <:why:932912321544728576> 
        <:why:932912321544728576> 
<:why:932912321544728576> **       **  <:why:932912321544728576>
"""
        )

    # Polls

    @commands.command(aliases=['yahornah', 'yn'], extras={"category":"Fun"}, usage="yesorno [question]", help="This command makes a small poll which users can vote either yes, or no", description="Makes a Yah or Nah poll")
    @commands.check(plugin_enabled)
    async def yesorno(self, ctx, *, message):
        msg = await ctx.send(embed=discord.Embed(title="Yah or Nah?", description=message, color=ctx.author.color))
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
        embed = discord.Embed(title=question, description=''.join(description), color=ctx.author.color)
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
        await message.reply(embed=discord.Embed(title=f"Poll Results For {question}:", description=f"**Votes:**\n {results}", color=ctx.author.color))

    @commands.command(extras={"category":"Fun"}, usage="reactemoji [message_id] [word]", help="This command reacts a word to a message. If the word has more then one letter thats the same it wont work", description="React a word to a message")
    @commands.check(plugin_enabled)
    async def reactemoji(self, ctx,msg:int, *, text):
        text = text.lower()
        alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        emojis = ["🇦", "🇧", "🇨", "🇩" ,"🇪", "🇫" ,"🇬", "🇭" ,"🇮", "🇯", "🇰", "🇱", "🇲", "🇳" ,"🇴" ,"🇵" ,"🇶", "🇷" ,"🇸", "🇹" ,"🇺", "🇻", "🇼", "🇽", "🇾", "🇿"]
        
        emojis = dict(zip(alpha, emojis))
        message = await ctx.message.channel.fetch_message(msg)
        for i in text:
            try:
                emoji = emojis[i]
                await message.add_reaction(emoji)
            except Exception as e:
                print(e)

def setup(client):
    client.add_cog(Fun(client))
