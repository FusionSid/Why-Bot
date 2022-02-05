import discord
import json
from utils.checks import plugin_enabled
import os
import time
import platform
from discord import role
from discord.ext import commands
import psutil
import qrcode
from simpcalc import simpcalc
from discord.ui import Button, View
import numexpr as ne
import random, operator


class InteractiveView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=100)
        self.expr = ""
        self.ctx = ctx
        # if you are using the above function, no need to declare this!
        self.calc = simpcalc.Calculate()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="1", row=0)
    async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "1"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="2", row=0)
    async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "2"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="3", row=0)
    async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "3"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="+", row=0)
    async def plus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "+"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="4", row=1)
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "4"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="5", row=1)
    async def five(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "5"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="6", row=1)
    async def six(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "6"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="/", row=1)
    async def divide(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "/"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "7"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "8"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "9"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="*", row=2)
    async def multiply(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "*"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "."
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "0"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="=", row=3)
    async def equal(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            self.expr = await self.calc.calculate(self.expr)
        except:  # if you are function only, change this to BadArgument
            return await interaction.response.send_message("Um, looks like you provided a wrong expression....")
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="-", row=3)
    async def minus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "-"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="(", row=4)
    async def left_bracket(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "("
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label=")", row=4)
    async def right_bracket(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += ")"
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.red, label="C", row=4)
    async def clear(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = ""
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.red, label="<==", row=4)
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = self.expr[:-1]
        await interaction.message.edit(content=f"```\n{self.expr}\n```")

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("This isnt for you", ephemeral=True)
            return False
        else:
            return True


def get_lines():
    lines = 0
    files = []
    for i in os.listdir():
        if i.endswith(".py"):
            files.append(i)
    for i in os.listdir("cogs/"):
        if i.endswith(".py"):
            files.append(f"cogs/{i}")
    for i in os.listdir("utils/"):
        if i.endswith(".py"):
            files.append(f"utils/{i}")
    for i in files:
        count = 0
        with open(i, 'r') as f:
            for line in f:
                count += 1
        lines += count
    return lines


class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(extras={"category": "Utilities"}, usage="invite", help="This command creates a quick invite for your server", description="Creates a 10 day invite for your discord server.")
    @commands.check(plugin_enabled)
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=10)
        await ctx.send(link)

    @commands.command(aliases=['bot'], extras={"category": "Utilities"}, usage="botinvite", help="Creates an invite link so you can invite Why to your server", description="Invite why to your server")
    @commands.check(plugin_enabled)
    async def botinvite(self, ctx):
        await ctx.send(embed=discord.Embed(title="Invite **Why?** to your server:", description="https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"))

    @commands.command(extras={"category": "Utilities"}, usage="info [@user]", help="This command shows a message with info on a user.", description="Returns info on a user")
    @commands.check(plugin_enabled)
    async def info(self, ctx, member: discord.Member = None):
        if member == None:
            return await ctx.send(f"{ctx.prefix}info person <@person>\nYou didnt @ the member")
        roles = [role for role in member.roles]
        em = discord.Embed(title="Person Info",
                           description=f"For: {member.name}")
        if str(member.status) == "online":
            status = "🟢 Online"
        elif str(member.status) == "offline":
            status = "🔴 Offline"
        elif str(member.status) == "dnd":
            status = '⛔ Do not disturb'
        elif str(member.status) == "invisible":
            status = "🔴 Invisible"
        elif str(member.status) == "idle":
            status = "🌙 Idle"
        elif str(member.status) == "streaming":
            status = "📷 Streaming"
        else:
            status = member.status
        em.add_field(name="Status:", value=status, inline=False)

        em.add_field(name="ID:", value=member.id, inline=False)
        em.set_thumbnail(url=member.avatar.url)
        em.add_field(name="Created Account:",
                     value=f"<t:{int(time.mktime(member.created_at.timetuple()))}>", inline=False)
        em.add_field(name="Joined Server:",
                     value=f"<t:{int(time.mktime(member.joined_at.timetuple()))}>", inline=False)
        em.add_field(name="Highest Role:",
                     value=member.top_role.mention, inline=False)

        with open("./database/db.json") as f:
            data = json.load(f)
        for i in data:
            if i['guild_id'] == ctx.guild.id:
                warnings = i['warnings']
        if str(member.id) not in warnings:
            em.add_field(name="Warnings", value="This user has no warnings")
        else:
            em.add_field(name="Warnings", value=len(warnings[str(member.id)]))
        if len(roles) > 15:
            em.add_field(name="Roles:", value=f"{len(roles)}", inline=False)
        else:
            em.add_field(name=f"Roles ({len(roles)}):", value=" ".join(
                role.mention for role in roles), inline=False)
        await ctx.send(embed=em)

    @commands.command(aliases=['sug'], extras={"category": "Utilities"}, usage="suggest [suggestion]", help="This command is used to suggest new features/commands to us", description="Suggest something for Why")
    @commands.check(plugin_enabled)
    async def suggest(self, ctx, *, suggestion):
        sid = await self.client.fetch_channel(925157029092413460)
        await sid.send(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.send("Thank you for you suggestion!")

    @commands.command(extras={"category": "Utilities"}, usage="ping", help="Shows the bots ping", description="Shows bot ping")
    @commands.check(plugin_enabled)
    async def ping(self, ctx):
        await ctx.send(f"Pong! jk\n{round(self.client.latency * 1000)}ms")

    @commands.command(extras={"category": "Utilities"}, usage="serverinfo", help="Returns info on this server.", description="shows server info")
    @commands.check(plugin_enabled)
    async def serverinfo(self, ctx):
        em = discord.Embed(
            title="Server Info:", description=f"For: {ctx.guild.name}", color=ctx.author.color)
        em.set_thumbnail(url=ctx.guild.icon.url)
        em.set_author(
            name=f"Guild Owner: {ctx.guild.owner.name}", icon_url=ctx.guild.owner.avatar.url)
        em.add_field(
            name="Channels:", value=f"**Text:** {len(ctx.guild.text_channels)}\n**Voice:** {len(ctx.guild.voice_channels)}")
        em.add_field(name="Roles:", value=len(ctx.guild.roles))
        bots = 0
        members = 0
        for i in ctx.guild.members:
            if i.bot:
                bots += 1
            else:
                members += 1
        em.add_field(
            name="Members:", value=f"**Total:** {ctx.guild.member_count}\n**Humans:** {members}\n**Bots:** {bots}")
        em.add_field(
            name="Created: ", value=f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}>")
        em.add_field(name="ID:", value=ctx.guild.id)
        await ctx.send(embed=em)

    @commands.command(extras={"category": "Utilities"}, usage="botinfo", help="This command shows info on the bot", description="Info about Why bot")
    @commands.check(plugin_enabled)
    async def botinfo(self, ctx):
        with open("./database/userdb.json") as f:
            data = json.load(f)
        active = len(data)
        em = discord.Embed(title='Why Bot', description='Just Why?')
        em.add_field(inline=False, name="Server Count",
                     value=f"{len(self.client.guilds)}")
        mlist = []
        for i in list(self.client.get_all_members()):
            mlist.append(i.name)
        em.add_field(inline=False, name="User Count", value=len(mlist))
        em.add_field(inline=False, name="Command Count",
                     value=f"{len(self.client.commands)} commands")
        em.add_field(inline=False, name="Active User Count", value=active)
        em.add_field(inline=False, name="Ping",
                     value=f"{round(self.client.latency * 1000)}ms")
        em.set_footer(text="Mostly made by FusionSid#3645")
        em.add_field(name='CPU Usage',
                     value=f'{psutil.cpu_percent()}%', inline=False)
        em.add_field(name='Memory Usage',
                     value=f'{psutil.virtual_memory().percent}% of ({round((psutil.virtual_memory().total/1073741824), 2)}GB)', inline=False)
        em.add_field(name='Available Memory',
                     value=f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%', inline=False)
        em.add_field(inline=False, name="Python version",
                     value=f"{platform.python_version()}")
        em.add_field(inline=False, name="Running on",
                     value=f"{platform.system()} {platform.release()}")
        em.add_field(name="Python code", value=f"{get_lines()} of code")
        await ctx.send(embed=em)

    @commands.command(aliases=['qr'], extras={"category": "Utilities"}, usage="qrcode [url]", help="This command takes in a url and makes a qrcode.", description="Creates a qrcode")
    @commands.check(plugin_enabled)
    async def qrcode(self, ctx, *, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(url))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",
                            back_color="white").convert('RGB')
        img.save('./tempstorage/qrcode.png')
        await ctx.send(file=discord.File('./tempstorage/qrcode.png'))

    @commands.command(aliases=['calculator'], extras={"category": "Utilities"}, usage="calculator", help="This command shows an interactive button calculator", description="Interactive button calculator")
    @commands.check(plugin_enabled)
    async def calculate(self, ctx):
        view = InteractiveView(ctx)
        message = await ctx.send("```\n```", view=view)
        res = await view.wait()
        if res:
            for i in view.children:
                i.disabled = True
        return await message.edit(view=view)

    @commands.command(extras={"category": "Utilities"}, usage="calc [query]", help="This command returns a calculated result. It supports binary, and bit shifts and squareroots", description="Calculates your query")
    @commands.check(plugin_enabled)
    async def calc(self, ctx, *, query):
        try:
            calc = ne.evaluate(query)
            msg = int(calc)
            await ctx.send(msg)
        except Exception as e:
            await ctx.send(f"Calculation Error\n{e}")

    @commands.command(extras={"category": "Utilities"}, usage="vote", help="This command allows you to vote for Why bot", description="Vote for why bot")
    @commands.check(plugin_enabled)
    async def vote(self, ctx):
        button = Button(style=discord.ButtonStyle.grey, label="Vote link:",
                        url="https://discordbotlist.com/bots/why")
        view = View(timeout=15)
        view.add_item(button)
        await ctx.send(embed=discord.Embed(title="Vote for Why Bot here:"), view=view)

    @commands.command(extras={"category": "Utilities"}, usage="cuse [@user(optional)]", help="Shows how many times you have used Why bot", description="How many times have you used Why?")
    async def cuse(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open('./database/userdb.json') as f:
            data = json.load(f)
            for i in data:
                if i["user_id"] == member.id:
                    cuse = i["command_count"]
        await ctx.send(embed=discord.Embed(title=f"You have used Why Bot {cuse} times"))

    @commands.command(no_pm=True, help="This command is used to check whos playing a certain game/activity", extras={"category":"Utilities"}, usage="whosplaying [game/activity]", description="Check whosplaying activity")
    async def whosplaying(self, ctx, *, game):
        if len(game) <= 1:
            await ctx.send("```The game should be at least 2 characters long...```", delete_after=5.0)
            return

        guild = ctx.message.guild
        members = guild.members
        playing_game = ""
        count_playing = 0

        for member in members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if game.lower() in member.activity.name.lower():
                count_playing += 1
                if count_playing <= 15:
                    emote = random.choice(
                        [":trident:", ":high_brightness:", ":low_brightness:", ":beginner:", ":diamond_shape_with_a_dot_inside:"])
                    playing_game += f"{emote} {member.name} ({member.activity.name})\n"

        if playing_game == "":
            await ctx.send("```Search results:\nNo users are currently playing that game.```")
        else:
            msg = playing_game
            if count_playing > 15:
                showing = "(Showing 15/{})".format(count_playing)
            else:
                showing = "({})".format(count_playing)

            em = discord.Embed(
                description=msg, colour=discord.Colour(value=0x36393e))
            await ctx.send(embed=em)


    @commands.command(no_pm=True, help="This command is used to show the most played games right now", extras={"category":"Utilities"}, usage="currentgames", description="Show current games being played")
    async def currentgames(self, ctx):
        """Shows the most played games right now"""
        guild = ctx.message.guild
        members = guild.members

        freq_list = {}
        for member in members:
            if not member:
                continue
            if not member.activity or not member.activity.name:
                continue
            if member.bot:
                continue
            if member.activity.name not in freq_list:
                freq_list[member.activity.name] = 0
            freq_list[member.activity.name] += 1

        sorted_list = sorted(freq_list.items(),
                             key=operator.itemgetter(1),
                             reverse=True)

        if not freq_list:
            await ctx.send("```Search results:\nNo users are currently playing any games. Odd...```")
        else:
            # Create display and embed
            msg = ""
            max_games = min(len(sorted_list), 10)

            em = discord.Embed(
                description=msg, colour=discord.Colour(value=0x36393e))
            for i in range(max_games):
                game, freq = sorted_list[i]
                if int(freq_list[game]) < 2:
                    amount = "1 person"
                else:
                    amount = f"{int(freq_list[game])} people"
                em.add_field(name=game, value=amount)
            em.set_thumbnail(url=guild.icon.url)
            em.set_footer(
                text=f"Do {ctx.prefix}whosplaying <game> to see whos playing a specific game")
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(Utilities(client))
