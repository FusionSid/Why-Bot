import discord
import json
from utils.checks import plugin_enabled
from discord.ext import commands
import qrcode
from simpcalc import simpcalc
from discord.ui import Button, View
import numexpr as ne


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
        await ctx.send(embed=discord.Embed(title="Invite **Why?** to your server:", description="[Why Invite Link](https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands)", color=ctx.author.color))

   
    @commands.command(usage = "avatar [member]", description = "User avatar", help = "Gets a members avatar and shows it", extras={"category": "Utilities"})
    @commands.check(plugin_enabled)
    async def avatar(self, ctx, member:discord.Member=None):
        if member is None:
            member = ctx.author
        em = discord.Embed(title=f"{member.name}'s Avatar:")
        em.set_image(url=member.avatar.url)
        await ctx.send(embed=em)


    @commands.command(aliases=['sug'], extras={"category": "Utilities"}, usage="suggest [suggestion]", help="This command is used to suggest new features/commands to us", description="Suggest something for Why")
    @commands.check(plugin_enabled)
    async def suggest(self, ctx, *, suggestion):
        sid = await self.client.fetch_channel(925157029092413460)
        em = discord.Embed(
            title= "Suggestion:",
            description=f"By: {ctx.author.name}\n\n{suggestion}",
            color=discord.Color.random()
        )
        await sid.send(embed=em, content=ctx.author.id)
        await ctx.send("Thank you for you suggestion!")

    

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
        await ctx.send(embed=discord.Embed(title="Vote for Why Bot here:", color=ctx.author.color), view=view)

    @commands.command(extras={"category": "Utilities"}, usage="cuse [@user(optional)]", help="Shows how many times you have used Why bot", description="How many times have you used Why?")
    @commands.check(plugin_enabled)
    async def cuse(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open('./database/userdb.json') as f:
            data = json.load(f)
        cuse = data[str(member.id)]["command_count"]
        await ctx.send(embed=discord.Embed(title=f"You have used Why Bot {cuse} times", color=ctx.author.color))

    

def setup(client):
    client.add_cog(Utilities(client))
