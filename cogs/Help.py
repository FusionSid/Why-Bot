import discord
from discord.ext import commands
import json
from discord.ui import Button, View
from utils import Paginator, is_it_me
from utils.other import log

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, cmd=None):
        cats = ["Counting","Economy", "Fun", "Minecraft", "Moderation", "Music", "Ping", "Search", "Text", "Ticket", "Utilities"]
        if cmd == None:
            em = discord.Embed(title="Why Help")
            em.add_field(
                inline=False, name=f"Use `{ctx.prefix}help all`", value="For all commands")
            em.add_field(
                inline=False, name=f"`{ctx.prefix}help [command]`", value="Give information about a specific command")
            em.add_field(
                inline=False, name=f"`{ctx.prefix}help [category]`", value="Give information about a specific category")
            em.add_field(inline=False, name="Useful Commands:",
                         value=f"`/set`, `{ctx.prefix}settings`, `{ctx.prefix}setprefix`, `{ctx.prefix}report`")
            em.add_field(inline=False, name="Why Support Server",
                         value="https://discord.gg/8fJaesY8SR")
            em.add_field(inline=False, name="Contribute/Source Code",
                         value="https://github.com/FusionSid/Why-Bot")
            em.add_field(inline=False, name="Dm Bot",
                         value="You can always just dm the bot for help, suggestions, bugreports etc")
            em.add_field(inline=False, name="Categories", value="Counting,Economy, Fun, Minecraft, Moderation, Music, Ping, Search, Text, Ticket, Utilities")
            em.set_footer(
                text="Default prefix is ? might be different for you")
            button = Button(style=discord.ButtonStyle.grey, label="Vote:",
                            url="https://discordbotlist.com/bots/why")
            button2 = Button(style=discord.ButtonStyle.grey, label="Source:",
                             url="https://github.com/FusionSid/Why-Bot")
            button3 = Button(style=discord.ButtonStyle.grey,
                             label="Discord:", url="https://discord.gg/8fJaesY8SR")
            button4 = Button(style=discord.ButtonStyle.grey, label="Todo:",
                             url="https://github.com/users/FusionSid/projects/1")
            button5 = Button(style=discord.ButtonStyle.grey,
                             label="Website:", url="https://fusionsid.xyz/whybot")
            view = View(timeout=15)
            view.add_item(button)
            view.add_item(button2)
            view.add_item(button3)
            view.add_item(button4)
            view.add_item(button5)
            message = await ctx.send(embed=em, view=view)
            res = await view.wait()
            if res:
                for i in view.children:
                    i.disabled = True
            return await message.edit(view=view)
        if cmd.lower() == "all":
            counting = discord.Embed(title="Why Help `[Counting]`:", description="Use `?help [command]` for more info on command")
            economy = discord.Embed(title="Why Help: `[Economy]`", description="Use `?help [command]` for more info on command")
            fun = discord.Embed(title="Why Help: `[Fun]`", description="Use `?help [command]` for more info on command")
            minecraft = discord.Embed(title="Why Help: `[Minecraft]`", description="Use `?help [command]` for more info on command")
            moderation = discord.Embed(title="Why Help: `[Moderation]`", description="Use `?help [command]` for more info on command")
            music = discord.Embed(title="Why Help: `[Music]`", description="Use `?help [command]` for more info on command")
            ping = discord.Embed(title="Why Help: `[Ping]`", description="Use `?help [command]` for more info on command")
            search = discord.Embed(title="Why Help: `[Search]`", description="Use `?help [command]` for more info on command")
            text = discord.Embed(title="Why Help: `[Text]`", description="Use `?help [command]` for more info on command")
            ticket = discord.Embed(title="Why Help: `[Ticket]`", description="Use `?help [command]` for more info on command")
            utilites = discord.Embed(title="Why Help: `[Utilites]`", description="Use `?help [command]` for more info on command")
            with open("./database/help.json") as f:
                data = json.load(f)
            for key, value in data.items():
                if key == "Counting":
                    for i in value:
                        counting.add_field(name=i["name"], value=i["description"], inline=False)
                if key == "Economy":
                    for i in value:
                        economy.add_field(name=i["name"], value=i["description"], inline=False)
                if key == "Fun":
                    for i in value:
                        fun.add_field(name=i["name"], value=i["description"], inline=False)
                if key == "Minecraft":
                    for i in value:
                        minecraft.add_field(name=i["name"], value=i["description"], inline=False)
                if key == "Moderation":
                    for i in value:
                        moderation.add_field(name=i["name"], value=i["description"], inline=False)
                if key == "Music":
                    for i in value:
                        music.add_field(name=i["name"], value=i["description"], inline=False)
                if key == "Ping":
                    for i in value:
                        ping.add_field(name=i["name"], value=i["description"], inline=False)
                if key == "Search":
                    for i in value:
                        search.add_field(name=i["name"], value=i["description"], inline=False)
                if key == "Text":
                    for i in value:
                        text.add_field(name=i["name"], value=i["description"], inline=False)
                if key == "Ticket":
                    for i in value:
                       ticket.add_field(name=i["name"], value=i["description"], inline=False)
                if key == "Utilities":
                    for i in value:
                        utilites.add_field(name=i["name"], value=i["description"], inline=False)
            em = discord.Embed(title="Why Help", description="Use the buttons to look through all the commands\nUse `?help [command]` for more info on command")
            ems = [counting, economy, fun, minecraft, moderation, music, ping, search, text, ticket, utilites]
            view = Paginator(ctx, ems)
            message = await ctx.send(embed=em, view=view)
            res = await view.wait()
            if res:
                for i in view.children:
                    i.disabled = True
            return await message.edit(view=view)
        elif cmd in cats:
          with open("./database/help.json") as f:
            data = json.load(f)
          stuff = data[cmd]
          e = discord.Embed(title="Why Help", description=f"Use {ctx.prefix}help [command] for more info on a specific command")
          for i in stuff:
            e.add_field(name=i['name'], value=i['description'])
          await ctx.send(embed=e)
        else:
            with open('./database/help.json') as f:
                data = json.load(f)
            em = discord.Embed(title="Why Help:", description="Use `?help [command]` for more info on command")
            for key, value in data.items():
                for i in value:
                    if i["name"] == cmd.lower():
                        em.add_field(inline=False, name="Name: ", value=i["name"])
                        em.add_field(inline=False, name="Description: ",
                                    value=i["description"])
                        usage = ctx.prefix+i["usage"]
                        em.add_field(inline=False, name="Usage: ", value=usage)
                        em.add_field(inline=False, name="Category: ",
                                    value=i["category"])
                        return await ctx.send(embed=em)

            em.add_field(name="Command Not Found", value=f"Use `{ctx.prefix}help` to find help")
            await ctx.send(embed=em)

    @commands.command()
    @commands.check(is_it_me)
    async def add_help(self, ctx):
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        with open("./database/help.json") as f:
            data = json.load(f)

        await ctx.send(embed=discord.Embed(title="Please enter the command name:"))
        name = await self.client.wait_for("message", check=check, timeout=300)
        name = str(name.content)

        await ctx.send(embed=discord.Embed(title="Please enter the description:"))
        desc = await self.client.wait_for("message", check=check, timeout=300)
        desc = str(desc.content)

        await ctx.send(embed=discord.Embed(title="Please enter the usage:"))
        use = await self.client.wait_for("message", check=check, timeout=300)
        use = str(use.content)

        cats = {"1": "Counting", "2": "Economy", "3": "Fun", "4": "Minecraft", "5":"Moderation","6": "Music",
                "7": "Ping", "8": "Search", "9": "Text", "10": "Ticket", "11": "Utilities"}
        await ctx.send(embed=discord.Embed(title="Please enter the number of the category:", description=cats))
        cat = await self.client.wait_for("message", check=check, timeout=300)
        cat = str(cat.content)
        cat = cats[cat]

        help_command = {
            "name": name,
            "description": desc,
            "usage": f"{use}",
            "category":cat
        }

        data[cat].append(help_command)
        with open('./database/help.json', 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(embed=discord.Embed(title="Command created successfully.", description=f"You can view it using `{ctx.prefix}help {name}`"))

    @commands.command()
    async def testhelp(self, ctx):
        counting = discord.Embed(title="Why Help `[Counting]`:", description="Use `?help [command]` for more info on command")
        fun = discord.Embed(title="Why Help: `[Fun]`", description="Use `?help [command]` for more info on command")
        leveling = discord.Embed(title="Why Help: `[Leveling]`", description="Use `?help [command]` for more info on command")
        logs = discord.Embed(title="Why Help: `[Logs]`", description="Use `?help [command]` for more info on command")
        minecraft = discord.Embed(title="Why Help: `[Minecraft]`", description="Use `?help [command]` for more info on command")
        moderation = discord.Embed(title="Why Help: `[Moderation]`", description="Use `?help [command]` for more info on command")
        music = discord.Embed(title="Why Help: `[Music]`", description="Use `?help [command]` for more info on command")
        ping = discord.Embed(title="Why Help: `[Ping]`", description="Use `?help [command]` for more info on command")
        search = discord.Embed(title="Why Help: `[Search]`", description="Use `?help [command]` for more info on command")
        settings = discord.Embed(title="Why Help: `[Settings]`", description="Use `?help [command]` for more info on command")
        text = discord.Embed(title="Why Help: `[Text]`", description="Use `?help [command]` for more info on command")
        ticket = discord.Embed(title="Why Help: `[Ticket]`", description="Use `?help [command]` for more info on command")
        utilities = discord.Embed(title="Why Help: `[Utilites]`", description="Use `?help [command]` for more info on command")
        voice = discord.Embed(title="Why Help: `[Voice]`", description="Use `?help [command]` for more info on command")
        welcome = discord.Embed(title="Why Help: `[Welcome]`", description="Use `?help [command]` for more info on command")
        economy = discord.Embed(title="Why Help: `[Economy]`", description="Use `?help [command]` for more info on command")

        embeds = [counting, fun, leveling, logs, minecraft, moderation, music, ping, search, settings, text, ticket, utilities, voice, welcome, economy]
        emojis = ["🔢","😂","🏆","📝","🎮","🛠️","🎵","⚠️","🔎","⚙️","🔀","🎫","🎤","👋","💵"]
        view = None # DropdownView(embeds=embeds, emojis=emojis)
        
        message = await ctx.send("e", view=view)

def setup(client):
    client.add_cog(Help(client))
