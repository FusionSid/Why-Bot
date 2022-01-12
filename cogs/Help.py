import discord
from discord.ext import commands
import json
from discord.ui import Button, View
from utils import Paginator

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, cmd = None):
        em = discord.Embed(title="Why Help")
        cats = ["economy", "fun", "reddit", "google", "minecraft", "moderation", "music", "slash", "text", "ticket", "utilities", "other"]
        if cmd == 'all':
            with open("./database/help.json") as f:
                data = json.load(f)
            economy = discord.Embed(title="Why Help `[Economy]`:", description="Use `?help [command]` for more info on command")
            fun = discord.Embed(title="Why Help: `[Fun]`", description="Use `?help [command]` for more info on command")
            reddit = discord.Embed(title="Why Help: `[Reddit]`", description="Use `?help [command]` for more info on command")
            google = discord.Embed(title="Why Help: `[Google]`", description="Use `?help [command]` for more info on command")
            minecraft = discord.Embed(title="Why Help: `[Minecraft]`", description="Use `?help [command]` for more info on command")
            moderation = discord.Embed(title="Why Help: `[Moderation]`", description="Use `?help [command]` for more info on command")
            music = discord.Embed(title="Why Help: `[Music]`", description="Use `?help [command]` for more info on command")
            text = discord.Embed(title="Why Help: `[Text]`", description="Use `?help [command]` for more info on command")
            ticket = discord.Embed(title="Why Help: `[Ticket]`", description="Use `?help [command]` for more info on command")
            utilities = discord.Embed(title="Why Help: `[Utilities]`", description="Use `?help [command]` for more info on command")
            other = discord.Embed(title="Why Help: `[Other]`", description="Use `?help [command]` for more info on command")
            for i in data:
                if i['category'] == "Economy":
                    economy.add_field(name=i["name"], value=i["description"], inline=False)

                if i['category'] == "Fun":
                    fun.add_field(name=i["name"], value=i["description"], inline=False)

                if i['category'] == "Reddit":
                    reddit.add_field(name=i["name"], value=i["description"], inline=False)

                if i['category'] == "Google":
                    google.add_field(name=i["name"], value=i["description"], inline=False)

                if i['category'] == "Minecraft":
                    minecraft.add_field(name=i["name"], value=i["description"], inline=False)

                if i['category'] == "Moderation":
                    moderation.add_field(name=i["name"], value=i["description"], inline=False)

                if i['category'] == "Music":
                    music.add_field(name=i["name"], value=i["description"], inline=False)

                if i['category'] == "Text":
                    text.add_field(name=i["name"], value=i["description"], inline=False)

                if i['category'] == "Ticket":
                    ticket.add_field(name=i["name"], value=i["description"], inline=False)

                if i['category'] == "Utilities":
                    utilities.add_field(name=i["name"], value=i["description"], inline=False)

                if i['category'] == "Other":
                    other.add_field(name=i["name"], value=i["description"], inline=False)

            em = discord.Embed(title="Why Help:", description="Use `?help [command]` for more info on command")
            ems = [economy, fun, reddit, google, minecraft, moderation, music, text, ticket, utilities, other]
            view = Paginator(ctx, ems)
            message = await ctx.send(embed=em, view=view)
            res = await view.wait()
            if res:
              for i in view.children:
                i.disabled = True
            return await message.edit(view=view)

        if cmd is None:
            em.add_field(inline=False,name="`?help [category]`", value="Lists all commands in that category")
            em.add_field(inline=False,name="`?help [command]`", value="Give information about a specific command")
            em.add_field(inline=False,name="Useful Commands:", value="`/set`, `?settings`, `?setprefix`, `?report`")
            em.add_field(inline=False,name="Why Support Server", value="https://discord.gg/8fJaesY8SR")
            em.add_field(inline=False,name="Contribute/Source Code", value="https://github.com/FusionSid/Why-Bot")
            em.add_field(inline=False,name="Dm Bot", value="You can always just dm the bot for help, suggestions, bugreports etc")
            em.set_footer(text="Defauly prefix is ? might be different for you")
            em.add_field(inline=False,name="Categories:", value="Economy, Fun, Reddit, Google, Minecraft, Moderation, Music. Slash, Text, Ticket, Utilities and Other")
            button = Button(style=discord.ButtonStyle.grey,label="Vote:", url="https://discordbotlist.com/bots/why")
            button2 = Button(style=discord.ButtonStyle.grey,label="Source:", url="https://github.com/FusionSid/Why-Bot")
            button3 = Button(style=discord.ButtonStyle.grey,label="Discord:", url="https://discord.gg/8fJaesY8SR")
            button4 = Button(style=discord.ButtonStyle.grey,label="Todo:", url="https://github.com/users/FusionSid/projects/1")
            button5 = Button(style=discord.ButtonStyle.grey,label="Website:", url="https://fusionsid.xyz/whybot")
            view= View(timeout=15)
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
        elif cmd.lower() in cats:
            for i in cats:
                if i.lower() == cmd.lower():
                    category = i.lower()
            # loop thru all commands and show all with this category
            with open('./database/help.json') as f:
                data = json.load(f)
            em = discord.Embed(title="Why Help:", description="Use `?help [command]` for more info on command")
            for i in data:
                if i['category'].lower() == category.lower():
                    em.add_field(inline=False,name=i["name"], value=i["description"])
            em.set_footer(text="Defauly prefix is ? might be different for you")
            await ctx.send(embed=em)
        else:
            # loop thru all command to find one that has the same name and show its info
            with open('./database/help.json') as f:
                data = json.load(f)
            em = discord.Embed(title="Why Help:", description="Use `?help [command]` for more info on command")
            found = False
            for i in data:
                if i["name"] == cmd.lower():
                    found = True
                    em.add_field(inline=False,name="Name: ", value=i["name"])
                    em.add_field(inline=False,name="Description: ", value=i["description"])
                    em.add_field(inline=False,name="Usage: ", value=i["usage"])
                    em.add_field(inline=False,name="Category: ", value=i["category"])
                    em.set_footer(text="Defauly prefix is ? might be different for you")

                    return await ctx.send(embed=em)
            em.add_field(name="Command/Category Not Found", value="Use `?help` to find help")
            await ctx.send(embed=em)

        
    @commands.command()
    async def add_help(self, ctx):
        dev_ids = [624076054969188363]

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        with open("./database/help.json") as f:
            data = json.load(f)
            
        if ctx.author.id in dev_ids:

            await ctx.send(embed=discord.Embed(title="Please enter the command name:"))
            name = await self.client.wait_for("message", check=check, timeout=300)
            name = str(name.content)

            for cmd in data:
                if cmd['name'] == name:
                    await ctx.send("This command already exists")
                    return

            await ctx.send(embed=discord.Embed(title="Please enter the description:"))
            desc = await self.client.wait_for("message", check=check, timeout=300)
            desc = str(desc.content)

            await ctx.send(embed=discord.Embed(title="Please enter the usage:"))
            use = await self.client.wait_for("message", check=check, timeout=300)
            use = str(use.content)

            await ctx.send(embed=discord.Embed(title="Please enter the category:"))
            cat = await self.client.wait_for("message", check=check, timeout=300)
            cat = str(cat.content)

            help_command = {
                "name": name,
                "description": desc,
                "usage": f"`{use}`",
                "category":cat
            }

            data.append(help_command)
            with open('./database/help.json', 'w') as f:
                json.dump(data, f, indent=4)
            
            await ctx.send(embed=discord.Embed(title=f"Command created successfully.", description="You can view it using `?help {name}`"))

        else:
            await ctx.send("You dont have permission to use this command")

def setup(client):
    client.add_cog(Help(client))