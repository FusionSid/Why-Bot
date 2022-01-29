import discord
import json
from utils.checks import plugin_enabled
import os
import time
from utils.other import log
import platform
from discord import role
from discord.ext import commands
import psutil
import qrcode
from simpcalc import simpcalc
from discord.ui import Button, View

class InteractiveView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=100)
        self.expr = ""
        self.calc = simpcalc.Calculate() # if you are using the above function, no need to declare this!

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
        except: # if you are function only, change this to BadArgument
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

    @commands.command()
    @commands.check(plugin_enabled)
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=10)
        await ctx.send(link)

    @commands.command(aliases=['bot'])
    @commands.check(plugin_enabled)
    async def botinvite(self, ctx):
        await ctx.send(embed=discord.Embed(title="Invite **Why?** to your server:", description="https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"))

    @commands.command()
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
        em.add_field(name="Created Account:", value=f"<t:{int(time.mktime(member.created_at.timetuple()))}>", inline=False)
        em.add_field(name="Joined Server:", value=f"<t:{int(time.mktime(member.joined_at.timetuple()))}>", inline=False)
        em.add_field(name="Highest Role:", value=member.top_role.mention, inline=False)
        if len(roles) > 15:
          em.add_field(name="Roles:", value=f"{len(roles)}", inline=False)
        else:
          em.add_field(name=f"Roles ({len(roles)}):", value=" ".join(role.mention for role in roles), inline=False)
        await ctx.send(embed=em)

    @commands.command(aliases=['sug'])
    @commands.check(plugin_enabled)
    async def suggest(self, ctx, *, suggestion):
        sid = await self.client.fetch_channel(925157029092413460)
        await sid.send(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.send("Thank you for you suggestion!")

    @commands.command()
    @commands.check(plugin_enabled)
    async def ping(self, ctx):
        await ctx.send(f"Pong! jk\n{round(self.client.latency * 1000)}ms")

    @commands.command()
    @commands.check(plugin_enabled)
    async def serverinfo(self, ctx):
        em = discord.Embed(title="Server Info:", description=f"For: {ctx.guild.name}", color=ctx.author.color)
        em.set_thumbnail(url=ctx.guild.icon.url)
        em.set_author(name=f"Guild Owner: {ctx.guild.owner.name}", icon_url=ctx.guild.owner.avatar.url)
        em.add_field(name="Member Count:", value=ctx.guild.member_count) 
        em.add_field(name="Created: ", value=f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}>")
        em.add_field(name="ID:", value=ctx.guild.id)
        await ctx.send(embed=em)
    
    @commands.command()
    @commands.check(plugin_enabled)
    async def botinfo(self, ctx):
        with open("./database/userdb.json") as f:
          data = json.load(f)
        active = len(data)
        em = discord.Embed(title = 'Why Bot', description = 'Just Why?')
        em.add_field(inline = False,name="Server Count", value=f"{len(self.client.guilds)}")
        mlist = []
        for i in list(self.client.get_all_members()):
            mlist.append(i.name)
        em.add_field(inline = False,name="User Count", value=len(mlist))
        em.add_field(inline = False,name="Active User Count", value=active)
        em.add_field(inline = False,name="Ping", value=f"{round(self.client.latency * 1000)}ms")
        em.set_footer(text="Mostly made by FusionSid#3645")
        em.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
        em.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
        em.add_field(name = 'Available Memory', value = f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%', inline = False)
        em.add_field(inline = False,name="Python version", value= f"{platform.python_version()}")
        em.add_field(inline = False,name="Running on", value=f"{platform.system()} {platform.release()}")
        em.add_field(name="Python code", value=f"{get_lines()} of code")
        await ctx.send(embed = em)

    @commands.command(aliases=['qr'])
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


    @commands.command(aliases=['calc', 'calculator'])
    @commands.check(plugin_enabled)
    async def calculate(self, ctx):
        view = InteractiveView()
        message = await ctx.send("```\n```", view=view)
        res = await view.wait()
        if res:
          for i in view.children:
            i.disabled = True
        return await message.edit(view=view)

    @commands.command()
    @commands.check(plugin_enabled)
    async def vote(self, ctx):
        button = Button(style=discord.ButtonStyle.grey,label="Vote link:", url="https://discordbotlist.com/bots/why")
        view= View(timeout=15)
        view.add_item(button)
        await ctx.send(embed=discord.Embed(title="Vote for Why Bot here:"), view=view)
    @commands.command()
    async def cuse(self, ctx, member:discord.Member=None):
        if member is None:
          member = ctx.author
        with open('./database/userdb.json') as f:
          data = json.load(f)
          for i in data:
            if i["user_id"] == member.id:
                cuse = i["command_count"]
        await ctx.send(f"You have used Why Bot {cuse} times")        
        
        
def setup(client):
    client.add_cog(Utilities(client))
