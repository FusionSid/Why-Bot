import discord
from discord.ext import commands
import json
from discord.ui import Button, View
from utils import Paginator, is_it_me
from utils.other import log

class Dropdown(discord.ui.Select):
    def __init__(self, client):
        self.client = client
        categories = ["Counting", "Fun", "Leveling", "Logs", "Minecraft", "Moderation", "Music", "Ping", "Search", 'Settings', "Text", "Ticket", "Utilities", "Voice", "Welcome", "Economy"]

        for category in categories:
            index = categories.index(category)
            categories[index] = discord.Embed(title=category)

        for cmd in client.commands:
            try:
                if cmd.extras is None:
                    pass
                else:
                    for category in categories:
                        if cmd.extras['category'].lower() == category.title.lower():
                            index = categories.index(category)
                            categories[index].add_field(name=cmd.name, value=cmd.description, inline=False)
            except:
                pass
        
        options = []
        emojis = ["🔢","😂","🏆","📝","🎮","🛠️","🎵","⚠️","🔎","⚙️","🔀","🎫","📱","🎤","👋","💵"]
        for i in categories:
            index = categories.index(i)
            options.append(discord.SelectOption(emoji=emojis[index],label=i.title, description=f"Get help with the {i.title} commands"))


        super().__init__(
            placeholder="Choose the category you want help with...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        categories = ["Counting", "Fun", "Leveling", "Logs", "Minecraft", "Moderation", "Music", "Ping", "Search", 'Settings', "Text", "Ticket", "Utilities", "Voice", "Welcome", "Economy"]

        cat = self.values[0]

        for category in categories:
            index = categories.index(category)
            categories[index] = discord.Embed(title=category)

        for cmd in self.client.commands:
            try:
                if cmd.extras is None:
                    pass
                else:
                    for category in categories:
                        if cmd.extras['category'].lower() == category.title.lower():
                            index = categories.index(category)
                            categories[index].add_field(name=cmd.name, value=cmd.description, inline=False)
            except:
                pass
    
        for category in categories:
                if cat.lower() == "logs":
                    em = discord.Embed(title="Logs", description=f"`help [command]` for more info on command")
                    em.add_field(name="Use the /set command to set the mod/log channel", value="This category doesn't have any commands because it works on events.\nIf you use the `/set Mod/Log Channel #channel` command properly and set the right channel the bot will log things like Bans, Unbans, Messages being deleted/edited, Nick changes and more")
                    await interaction.response.edit_message(embed=em)

                elif cat.lower() == "welcome":
                    em = discord.Embed(title="Welcome", description=f"`help [command]` for more info on command")
                    em.add_field(name="This system is used to send welcome messages to a user/into a channel when a member joins", value="Use the `/set Welcome Channel #channel` to set the welcome channel")
                    await interaction.response.edit_message(embed=em)

                elif cat.lower() == "economy":
                    em = discord.Embed(title="Economy", description=f"`help [command]` for more info on command")
                    em.add_field(name="This plugin/category is still under construction", value="** **")
                    await interaction.response.edit_message(embed=em)

                if cat.lower() == category.title.lower():
                    await interaction.response.edit_message(embed=category)

class HelpView(View):
    def __init__(self, client):
        super().__init__(timeout=30)

        button1 = Button(style=discord.ButtonStyle.grey, label="Vote:",url="https://discordbotlist.com/bots/why")
        button2 = Button(style=discord.ButtonStyle.grey, label="Source:",url="https://github.com/FusionSid/Why-Bot")
        button3 = Button(style=discord.ButtonStyle.grey,label="Discord:", url="https://discord.gg/8fJaesY8SR")
        button4 = Button(style=discord.ButtonStyle.grey, label="Todo:",url="https://github.com/users/FusionSid/projects/1")
        button5 = Button(style=discord.ButtonStyle.grey,label="Website:", url="https://fusionsid.xyz/whybot")

        self.add_item(button1)
        self.add_item(button2)
        self.add_item(button3)
        self.add_item(button4)
        self.add_item(button5)

        self.add_item(Dropdown(client))


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, cat=None):
        
        if cat is None:
            pass
        
        elif cat.lower() == "logs":
            em = discord.Embed(title="Logs", description=f"`{ctx.prefix}help [command]` for more info on command")
            em.add_field(name="Use the /set command to set the mod/log channel", value="This category doesn't have any commands because it works on events.\nIf you use the `/set Mod/Log Channel #channel` command properly and set the right channel the bot will log things like Bans, Unbans, Messages being deleted/edited, Nick changes and more")
            return await ctx.send(embed=em)

        elif cat.lower() == "welcome":
            em = discord.Embed(title="Welcome", description=f"`{ctx.prefix}help [command]` for more info on command")
            em.add_field(name="This system is used to send welcome messages to a user/into a channel when a member joins", value="Use the `/set Welcome Channel #channel` to set the welcome channel")
            return await ctx.send(embed=em)

        elif cat.lower() == "economy":
            em = discord.Embed(title="Economy", description=f"`{ctx.prefix}help [command]` for more info on command")
            em.add_field(name="This plugin/category is still under construction", value="** **")
            return await ctx.send(embed=em)

        categories = ["Counting", "Fun", "Leveling", "Logs", "Minecraft", "Moderation", "Music", "Ping", "Search", 'Settings', "Text", "Ticket", "Utilities", "Voice", "Welcome", "Economy"]

        if cat is None:
            em = discord.Embed(title="Why Help")
            em.add_field(inline=False, name=f"Use `{ctx.prefix}help all`", value="For all commands")
            em.add_field(inline=False, name=f"`{ctx.prefix}help [command]`", value="Give information about a specific command")
            em.add_field(inline=False, name=f"`{ctx.prefix}help [category]`", value="Give information about a specific category")
            em.add_field(inline=False, name="Useful Commands:",value=f"`/set`, `{ctx.prefix}settings`, `{ctx.prefix}setprefix`, `{ctx.prefix}report`")
            em.add_field(inline=False, name="Why Support Server",value="https://discord.gg/8fJaesY8SR")
            em.add_field(inline=False, name="Contribute/Source Code",value="https://github.com/FusionSid/Why-Bot")
            em.add_field(inline=False, name="Dm Bot",value="You can always just dm the bot for help, suggestions, bugreports etc")
            em.add_field(inline=False, name="Categories", value=', '.join(categories))
            
            view= HelpView(self.client)
            message = await ctx.send(embed=em, view=view)
            res = await view.wait()
            if res:
                for i in view.children:
                    i.disabled = True
            return await message.edit(view=view)

        for category in categories:
            index = categories.index(category)
            categories[index] = discord.Embed(title=category)

        for cmd in self.client.commands:
            try:
                if cmd.extras is None:
                    pass
                else:
                    for category in categories:
                        if cmd.extras['category'].lower() == category.title.lower():
                            index = categories.index(category)
                            categories[index].add_field(name=cmd.name, value=cmd.description, inline=False)
            except:
                pass
    
        for category in categories:
            if cat.lower() == category.title.lower():
                return await ctx.send(embed=category)
                
        for cmd in self.client.commands:
            if cmd.name.lower() == cat.lower():
                em = discord.Embed(title="Why Help", description=f"`{ctx.prefix}help [command]` for more info on command")
                em.add_field(name=f"Name", value=f"`{cmd.name}`", inline=False)
                em.add_field(name="Aliases:", value=', '.join(cmd.aliases), inline=False)
                em.add_field(name="Usage: ", value=f"`{ctx.prefix}{cmd.usage}`", inline=False)
                em.add_field(name="Description:", value=f"""```{cmd.help}```""", inline=False)
                return await ctx.send(embed=em)

def setup(client):
    client.add_cog(Help(client))
