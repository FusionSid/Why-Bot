import discord
from discord.ext import commands
from discord.ui import Button, View

class Dropdown(discord.ui.Select):
    def __init__(self, client):
        self.client = client
        categories = ["Counting", "Fun", "Leveling", "Logs", "Minecraft", "Moderation", "Music", "Ping", "Search", 'Settings', "Text", "Ticket", "Utilities", "Voice", "Welcome", "Economy", "Games"]

        for category in categories:
            index = categories.index(category)
            categories[index] = discord.Embed(title=category, color=discord.Color.blue())

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
        emojis = ["🔢","😂","🏆","📝","🎮","🛠️","🎵","⚠️","🔎","⚙️","🔀","🎫","📱","🎤","👋","💵", "🕹️"]
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
        categories = ["Counting", "Fun", "Leveling", "Logs", "Minecraft", "Moderation", "Music", "Ping", "Search", 'Settings', "Text", "Ticket", "Utilities", "Voice", "Welcome", "Economy", "Games"]

        cat = self.values[0]

        for category in categories:
            index = categories.index(category)
            categories[index] = discord.Embed(title=category, color=discord.Color.blue())

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
                    em = discord.Embed(title="Logs", description=f"`help [command]` for more info on command", color=discord.Color.blue())
                    em.add_field(name="Use the /set command to set the mod/log channel", value="This category doesn't have any commands because it works on events.\nIf you use the `/set Mod/Log Channel #channel` command properly and set the right channel the bot will log things like Bans, Unbans, Messages being deleted/edited, Nick changes and more")
                    await interaction.response.edit_message(embed=em)

                elif cat.lower() == "welcome":
                    em = discord.Embed(title="Welcome", description=f"`help [command]` for more info on command", color=discord.Color.blue())
                    em.add_field(name="This system is used to send welcome messages to a user/into a channel when a member joins", value="Use the `/set Welcome Channel #channel` to set the welcome channel")
                    await interaction.response.edit_message(embed=em)

                elif cat.lower() == "economy":
                    em = discord.Embed(title="Economy", description=f"`help [command]` for more info on command", color=discord.Color.blue())
                    em.add_field(name="This plugin/category is still under construction", value="** **")
                    await interaction.response.edit_message(embed=em)

                if cat.lower() == category.title.lower():
                    await interaction.response.edit_message(embed=category)
                    
    async def interaction_check(self, interaction) -> bool:
      if interaction.user != self.ctx.author:
          await interaction.response.send_message("This isnt for you",ephemeral=True)
          return False
      else:
          return True

class HelpView(View):
    def __init__(self, client):
        super().__init__(timeout=30)

        button1 = Button(style=discord.ButtonStyle.grey, label="Vote:",url="https://discordbotlist.com/bots/why")
        button2 = Button(style=discord.ButtonStyle.grey, label="Source:",url="https://github.com/FusionSid/Why-Bot")
        button3 = Button(style=discord.ButtonStyle.grey,label="Discord:", url="https://discord.gg/ryEmgnpKND")
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
            em = discord.Embed(title="Logs", description=f"`{ctx.prefix}help [command]` for more info on command", color=ctx.author.color)
            em.add_field(name="Use the /set command to set the mod/log channel", value="This category doesn't have any commands because it works on events.\nIf you use the `/set Mod/Log Channel #channel` command properly and set the right channel the bot will log things like Bans, Unbans, Messages being deleted/edited, Nick changes and more")
            return await ctx.send(embed=em)

        elif cat.lower() == "welcome":
            em = discord.Embed(title="Welcome", description=f"`{ctx.prefix}help [command]` for more info on command", color=ctx.author.color)
            em.add_field(name="This system is used to send welcome messages to a user/into a channel when a member joins", value="Use the `/set Welcome Channel #channel` to set the welcome channel")
            em.add_field(name=f"Using `{ctx.prefix}welcome` without a subcommand will display the welcome image",value=f"Configure your welcome message:\n`{ctx.prefix}welcome textcolor`\n`{ctx.prefix}welcome image`\n`{ctx.prefix}welcome bgcolor`\n`{ctx.prefix}welcome text`")
            return await ctx.send(embed=em)

        elif cat.lower() == "economy":
            em = discord.Embed(title="Economy", description=f"`{ctx.prefix}help [command]` for more info on command", color=ctx.author.color)
            em.add_field(name="This plugin/category is still under construction", value="** **")
            return await ctx.send(embed=em)

        categories = ["Counting", "Fun", "Leveling", "Logs", "Minecraft", "Moderation", "Music", "Ping", "Search", 'Settings', "Text", "Ticket", "Utilities", "Voice", "Welcome", "Economy", "Games"]

        if cat is None:
            em = discord.Embed(title="Why Help", color=ctx.author.color)
            em.add_field(inline=False, name=f"Use `{ctx.prefix}help all`", value="For all commands")
            em.add_field(inline=False, name=f"`{ctx.prefix}help [command]`", value="Give information about a specific command")
            em.add_field(inline=False, name=f"`{ctx.prefix}help [category]`", value="Give information about a specific category")
            em.add_field(inline=False, name="Useful Commands:",value=f"`/set`, `{ctx.prefix}settings`, `{ctx.prefix}setprefix`, `{ctx.prefix}report`")
            em.add_field(inline=False, name="Why Support Server",value="[Link](https://discord.gg/ryEmgnpKND)")
            em.add_field(inline=False, name="Contribute/Source Code",value="[Link](https://github.com/FusionSid/Why-Bot)")
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
            categories[index] = discord.Embed(title=category, color=ctx.author.color)

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
                em = discord.Embed(title="Why Help", description=f"`{ctx.prefix}help [command]` for more info on command", color=ctx.author.color)
                em.add_field(name=f"Name", value=f"`{cmd.name}`", inline=False)
                if len(cmd.aliases) == 0:
                    em.add_field(name="Aliases:", value='None', inline=False)
                else:
                    em.add_field(name="Aliases:", value=', '.join(cmd.aliases), inline=False)
                em.add_field(name="Usage: ", value=f"`{ctx.prefix}{cmd.usage}`", inline=False)
                em.add_field(name="Description:", value=f"""```{cmd.help}```""", inline=False)
                return await ctx.send(embed=em)
        await ctx.send(embed=discord.Embed(title="Command/Category Not Found", color=ctx.author.color))


    @commands.command(aliases=['contribute', 'src'])
    async def source(self, ctx):
        link = "https://github.com/FusionSid/Why-Bot"

        button = Button(style=discord.ButtonStyle.grey, label="Code", url=link)
        view = View(timeout=30)

        view.add_item(button)

        await ctx.send(embed=discord.Embed(title="**Why Bot** Source Code:", color=ctx.author.color), view=view)


    @commands.command(aliases=["support", "discord_server", "server", "discord"])
    async def discordserver(self, ctx):
        link = "https://discord.gg/ryEmgnpKND"

        button = Button(style=discord.ButtonStyle.grey, label="Discord Server", url=link)
        view = View(timeout=30)

        view.add_item(button)

        await ctx.send(embed=discord.Embed(title="**Why Bot** Discord Server:", color=ctx.author.color), view=view)


def setup(client):
    client.add_cog(Help(client))
