import discord
from discord.commands import slash_command
from discord.ext import commands
from discord import Option
import json

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, cmd = None):
        em = discord.Embed(title="Why Help")
        cats = ["economy", "fun", "reddit", "google", "minecraft", "moderation", "music", "slash", "text", "ticket", "utilities", "other"]
        if cmd is None:
            em.add_field(inline=True,name="`?help [category]`", value="Lists all commands in that category")
            em.add_field(inline=True,name="`?help [command]`", value="Give information about a specific command")
            em.add_field(inline=True,name="Useful Commands:", value="`/set`, `?settings`, `?setprefix`")
            em.add_field(inline=True,name="Why Support Server", value="https://discord.gg/8fJaesY8SR")
            em.set_footer(text="Defauly prefix is ? might be different for you")
            em.add_field(inline=True,name="Categories:", value="Economy, Fun, Reddit, Google, Minecraft, Moderation, Music. Slash, Text, Ticket, Utilities and Other")
            return await ctx.send(embed=em)
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
                    em.add_field(inline=True,name=i["name"], value=i["description"])
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
                    em.add_field(inline=True,name="Name: ", value=i["name"])
                    em.add_field(inline=True,name="Description: ", value=i["description"])
                    em.add_field(inline=True,name="Usage: ", value=i["usage"])
                    em.add_field(inline=True,name="Category: ", value=i["category"])
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
            
            await ctx.send(embed=discord.Embed(title=f"Command created successfully.", description="You can view it using `.help {name}`"))

        else:
            await ctx.send("You dont have permission to use this command")

def setup(client):
    client.add_cog(Help(client))