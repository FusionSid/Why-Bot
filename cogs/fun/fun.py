import discord
import asyncio
import pyfiglet
import json
import random
from discord.ext import commands
import asyncio
from discord.utils import get
import dotenv
from utils.checks import plugin_enabled
import datetime
from utils import post_get_json, kwarg_to_embed, is_it_me
from discord.ui import View

dotenv.load_dotenv()
languages = ['awk', 'bash', 'befunge93', 'brachylog', 'brainfuck', 'c', 'c++', 'cjam', 'clojure', 'cobol', 'coffeescript', 'cow', 'crystal', 'csharp', 'csharp.net', 'd', 'dart', 'dash', 'dragon', 'elixir', 'emacs', 'erlang', 'file', 'forte', 'fortran', 'freebasic', 'fsharp.net', 'fsi', 'go', 'golfscript', 'groovy', 'haskell', 'husk', 'iverilog', 'japt', 'java', 'javascript', 'jelly', 'julia', 'kotlin', 'lisp', 'llvm_ir', 'lolcode', 'lua', 'matl', 'nasm', 'nasm64', 'nim', 'ocaml', 'octave', 'osabie', 'paradoc', 'pascal', 'perl', 'php', 'ponylang', 'powershell', 'prolog', 'pure', 'pyth', 'python', 'python2', 'racket', 'raku', 'retina', 'rockstar', 'rscript', 'ruby', 'rust', 'scala', 'sqlite3', 'swift', 'typescript', 'basic', 'basic.net', 'vlang', 'vyxal', 'yeethon', 'zig,']

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


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="This command gives you free coins. Click claim.", extras={"category":"Fun"}, usage="claim", description="Free Coins")
    @commands.check(plugin_enabled)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def claim(self,ctx):
        em = discord.Embed(title="Claim 100k Why Coins", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em, view=MyView())
        
    @commands.command(help="This command gives you free coins. Click claim.", extras={"category":"Fun"}, usage="nitro", description="Free Coins")
    @commands.check(is_it_me)
    @commands.check(plugin_enabled)
    async def nitro(self,ctx):
        em = discord.Embed(title="Claim Free Nitro", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.set_image(url="https://gudstory.s3.us-east-2.amazonaws.com/wp-content/uploads/2021/02/08150513/Discord-Nitro.png")
        await ctx.send(embed=em, view=MyView())

    @commands.command()
    @commands.check(plugin_enabled)
    async def ascii(self, ctx, *, message):
            font = "big"
            message = pyfiglet.figlet_format(message, font=font)
            await ctx.send('```\n{}\n```'.format(message))

    

    @commands.command()
    @commands.check(plugin_enabled)
    async def fascii(self, ctx, font:str, *,message):
        if font not in ["1943____","3-d","3x5","4x4_offr","5slalineoblique","5x7","5x8","64f1____","6x10","6x9","a_zooloo","acrobatic","advenger","alligator","alligator2","alphabet","aquaplan","arrows","asc_____","ascii___","assalt_m","asslt__m","atc_____","atc_gran","avatar","b_m__200","banner","banner3","banner3-D","banner4","barbwire","basic","battle_s","battlesh","baz__bil","beer_pub","bell","big","bigchief","binary","block","brite","briteb","britebi","britei","broadway","bubble","bubble__","bubble_b","bulbhead","c1______","c2______","c_ascii_","c_consen","calgphy2","caligraphy","catwalk","caus_in_","char1___","char2___","char3___","char4___","charact1","charact2","charact3","charact4","charact5","charact6","characte","charset_","chartr","chartri","chunky","clb6x10","clb8x10","clb8x8","cli8x8","clr4x6","clr5x10","clr5x6","clr5x8","clr6x10","clr6x6","clr6x8","clr7x10","clr7x8","clr8x10","clr8x8","coil_cop","coinstak","colossal","com_sen_","computer","contessa","contrast","convoy__","cosmic","cosmike","cour","courb","courbi","couri","crawford","cricket","cursive","cyberlarge","cybermedium","cybersmall","d_dragon","dcs_bfmo","decimal","deep_str","defleppard","demo_1__","demo_2__","demo_m__","devilish","diamond","digital","doh","doom","dotmatrix","double","drpepper","druid___","dwhistled","e__fist_","ebbs_1__","ebbs_2__","eca_____","eftichess","eftifont","eftipiti","eftirobot","eftitalic","eftiwall","eftiwater","epic","etcrvs__","f15_____","faces_of","fair_mea","fairligh","fantasy_","fbr12___","fbr1____","fbr2____","fbr_stri","fbr_tilt","fender","finalass","fireing_","flyn_sh","fourtops","fp1_____","fp2_____","fraktur","funky_dr","future_1","future_2","future_3","future_4","future_5","future_6","future_7","future_8","fuzzy","gauntlet","ghost_bo","goofy","gothic","gothic__","graceful","gradient","graffiti","grand_pr","greek","green_be","hades___","heavy_me","helv","helvb","helvbi","helvi","heroboti","hex","high_noo","hills___","hollywood","home_pak","house_of","hypa_bal","hyper___","inc_raw_","invita","isometric1","isometric2","isometric3","isometric4","italic","italics_","ivrit","jazmine","jerusalem","joust___","katakana","kban","kgames_i","kik_star","krak_out","larry3d","lazy_jon","lcd","lean","letter_w","letters","letterw3","lexible_","linux","lockergnome","mad_nurs","madrid","magic_ma","marquee","master_o","maxfour","mayhem_d","mcg_____","mig_ally","mike","mini","mirror","mnemonic","modern__","morse","moscow","mshebrew210","nancyj","nancyj-fancy","nancyj-underlined","new_asci","nfi1____","nipples","notie_ca","npn_____","ntgreek","nvscript","o8","octal","odel_lak","ogre","ok_beer_","os2","outrun__","p_s_h_m_","p_skateb","pacos_pe","panther_","pawn_ins","pawp","peaks","pebbles","pepper","phonix__","platoon2","platoon_","pod_____","poison","puffy","pyramid","r2-d2___","rad_____","rad_phan","radical_","rainbow_","rally_s2","rally_sp","rampage_","rastan__","raw_recu","rci_____","rectangles","relief","relief2","rev","ripper!_","road_rai","rockbox_","rok_____","roman","roman___","rot13","rounded","rowancap","rozzo","runic","runyc","sans","sansb","sansbi","sansi","sblood","sbook","sbookb","sbookbi","sbooki","script","script__","serifcap","shadow","shimrod","short","skate_ro","skateord","skateroc","sketch_s","slant","slide","slscript","sm______","small","smisome1","smkeyboard","smscript","smshadow","smslant","smtengwar","space_op","spc_demo","speed","stacey","stampatello","standard","star_war","starwars","stealth_","stellar","stencil1","stencil2","stop","straight","street_s","subteran","super_te","t__of_ap","tanja","tav1____","taxi____","tec1____","tec_7000","tecrvs__","tengwar","term","thick","thin","threepoint","ti_pan__","ticks","ticksslant","tiles","times","timesofl","tinker-toy","tomahawk","tombstone","top_duck","trashman","trek","triad_st","ts1_____","tsalagi","tsm_____","tsn_base","tty","ttyb","tubular","twin_cob","twopoint","type_set","ucf_fan_","ugalympi","unarmed_","univers","usa_____","usa_pq__","usaflag","utopia","utopiab","utopiabi","utopiai","vortron_","war_of_w","wavy","weird","whimsy","xbrite","xbriteb","xbritebi","xbritei","xchartr","xchartri","xcour","xcourb","xcourbi","xcouri","xhelv","xhelvb","xhelvbi","xhelvi","xsans","xsansb","xsansbi","xsansi","xsbook","xsbookb","xsbookbi","xsbooki","xtimes","xtty","xttyb","yie-ar__","yie_ar_k","z-pilot_","zig_zag_","zone7___"]:
            return await ctx.send("Invalid Font")
        message = pyfiglet.figlet_format(message, font=font)
        await ctx.send('```\n{}\n```'.format(message))
        
    @commands.command(aliases=['rockpaperscissors'], extras={"category":"Fun"}, usage="rps [rock/paper/scissors]", help="This command if for playing rock paper scissors with the bot.", description="Play a game of rock paper scissors against the bot")
    @commands.check(plugin_enabled)
    async def rps(self, ctx, rps: str):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
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
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)
    

    @commands.command(aliases=['sendmsg'], extras={"category":"Fun"}, usage="dm [@user] [message]", help="You can use this command to send a dm to a user. The bot will send the message to the user.", description="Bot sends a message on your behalf")
    @commands.check(plugin_enabled)
    async def dm(self, ctx, member: discord.Member, *, message):
        await ctx.message.delete()
        embeddm = discord.Embed(title=message, color=ctx.author.color)
        embeddm.timestamp = datetime.datetime.utcnow()
        embeddm.set_footer(text=f"Message sent by: {ctx.author}")
        await member.send(embed=embeddm)
    

    @commands.command(aliases=['sr'], extras={"category":"Fun"}, usage="sendroast [@user]", help="The bot picks a random roast from a list and send it to a person of your choosing", description="The bots send a roast to someone on your behalf")
    @commands.check(plugin_enabled)
    async def sendroast(self, ctx, member: discord.Member):
        await ctx.message.delete()
        message = await get_roast()
        embeddm = discord.Embed(
            title=message, description="Imagine being roasted by a bot", color=ctx.author.color)
        embeddm.timestamp = datetime.datetime.utcnow()
        embeddm.set_footer(text=f"Message sent by: {ctx.author}")
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
        em = discord.Embed(title="__8 Ball__",description=f"{question}\nAnswer: {random.choice(_8ballans)}")
        em.timestamp = datetime.datetime.utcnow()                   
        await ctx.send(embed=em)

    @commands.command(aliases=['em'], extras={"category":"Fun"}, usage="embed --title test --desc test --channel 123456789 --color blue --timestamp yes --fields 2", help="This command is used to make an embeded message.\nThe bot will create a nice embed and then send it to the channel youre in or the channel you want.", description="Makes an embed")
    @commands.check(plugin_enabled)
    async def embed(self, ctx, *, kwargs):
        data = await kwarg_to_embed(self.client, ctx, kwargs)
        if data is None:
            return
        em = data[0]
        channel = data[1]

        await ctx.message.delete()
        await channel.send(embed=em)

    @commands.command(usage = "runcode [language] [code]", description = "Runs code", help = "This command is used to run code. It supports many languages.", extras={"category": "Fun"})
    @commands.check(plugin_enabled)
    async def runcode(self, ctx, lang:str, *, code):
        code = code.replace("`", "")
        data = {
            "language": lang,
            "source" : f"""{code}"""
        }
        url = "https://emkc.org/api/v1/piston/execute"

        data = await post_get_json(url, data)
        print(data)
        if data['ran'] == True:
            await ctx.send(f"```py\n{data['output']}```")
        if data['stderr'] != "":
            await ctx.send(f"```Errors\n{data['stderr']}```")

    @commands.command(aliases=['noembed'], extras={"category":"Fun"}, usage="say [text]", help="The bot speaks text that you want", description="Bot sends text")
    @commands.check(plugin_enabled)
    async def say(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(f"{text}\n\n|| On behalf of {ctx.author.name} ||")

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
        embed.timestamp = datetime.datetime.utcnow()
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

    
    @commands.command(usage = "screenshot [url]", description = "Screenshot a url", help = "This command finds a url and screenshots it", extras={"category": "Fun"})
    @commands.check(plugin_enabled)
    async def screenshot(self, ctx, *, url):
        if "http://" not in url or "https://" not in url:
            url = f"https://{url}"
        em = discord.Embed(
            title = f"Screenshot",
            description = f"[Link]({url.replace('https://image.thum.io/get/', '')})",
            color = ctx.author.color
        )
        em.set_image(url=f"https://image.thum.io/get/{url}")

        await ctx.send(embed=em)


    @commands.command(usage = "hack [@user]", description = "Hack someone", help = "This command totally 'hacks' someone :)", extras={"category": "Fun"})
    async def hack(self, ctx, member: discord.Member):

        email_ext = ["gmail.com","yahoo.com","hotmail.com","aol.com","hotmail.co.uk","hotmail.fr","msn.com","yahoo.fr","wanadoo.fr","orange.fr","comcast.net","yahoo.co.uk","yahoo.com.br","yahoo.co.in","live.com","rediffmail.com","free.fr","gmx.de","web.de","yandex.ru","ymail.com","libero.it","outlook.com","uol.com.br","bol.com.br","mail.ru","cox.net","hotmail.it","sbcglobal.net","sfr.fr","live.fr","verizon.net","live.co.uk",]
        most_used_words = ['TrASh','gEt gUd','waSsUp','noOb', "LmAo", "lol", "lMfao", "e", "seNd nUkeS", "f&Ck", "sH#t", "nub", "b1T#h"]
        passwords = ["123456","password","12345","123456789","password1","abc123","12345678","qwerty","111111","1234567","1234","iloveyou","sunshine","monkey","1234567890","123123","princess","baseball","dragon","football","shadow","michael","soccer","unknown","maggie","000000.","ashley","myspace1","purple","fuckyou","charlie","jordan","hunter","superman","tigger","michelle","buster","pepper","justin","andrew","harley","matthew","bailey","jennifer","samantha","ginger","anthony","qwerty123","qwerty1","peanut"]

        hack_message = await ctx.send(f"[▖] Hacking {member.name} now...")
        await asyncio.sleep(1.420)
        await hack_message.edit(content='[▘] Finding discord login... (2fa bypassed)')
        await asyncio.sleep(1.69)
        email = f"{member.name}.{random.randint(1, 100)}@{random.choice(email_ext)}"
        await hack_message.edit(content=f"[▝] `Email: {email}`\n    `Password: {random.choice(passwords)}`")
        await asyncio.sleep(1.420)
        await hack_message.edit(content='[▗] IP address: 127.0.0.1:50')
        await asyncio.sleep(1.69)
        await hack_message.edit(content=f'[▖] Most used words: {random.choice(most_used_words)}')
        await asyncio.sleep(1.420)
        await hack_message.edit(content=f"[▘] Injecting trojan virus into discriminator: {member.discriminator}")
        await asyncio.sleep(1.69)
        await hack_message.edit(content='[▝] Selling information to the government...')
        await asyncio.sleep(1.420)
        await hack_message.edit(content=f'[▗] Reporting account to discord for breaking TOS...')
        await asyncio.sleep(1.69)
        await hack_message.edit(content='[▖] Hacking medical records...')
        await asyncio.sleep(1.420)
        await hack_message.edit(content=f"Finished hacking {member.mention}")
        
        await ctx.send("The *totally* real and dangerous hack is complete!")
        # "[▖] [▘] [▝] [▗]"

def setup(client):
    client.add_cog(Fun(client))



