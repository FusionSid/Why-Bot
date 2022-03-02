import discord
import json
from discord.ext import commands
from utils import Paginator
import datetime

async def enabled_cogs(client, ctx):
    data = await client.get_db()
    plugins = data[str(ctx.guild.id)]['settings']['plugins']
    em = discord.Embed(
        title="Plugins:", description="These are all the plugins that have been enabled on your server", color=ctx.author.color)
    em.timestamp = datetime.datetime.utcnow()
    for key, value in plugins.items():
        if value == True:
            emoji = "Enabled ✅"
        else:
            emoji = "Disabled ❌"
        em.add_field(name=key, value=emoji)
    em.set_footer(text=f"Use {ctx.prefix}plugins to toggle plugins")
    return em


async def get_channels(self, ctx):
    data = await self.client.get_db()
    em = discord.Embed(title="Channels", color=ctx.author.color)
    em.timestamp = datetime.datetime.utcnow()
    em.set_footer(text="Use /set to set these")
    if data[str(ctx.guild.id)]['counting_channel'] == None:
        counting = "Not Set"
    else:
        channel = await self.client.fetch_channel(data[str(ctx.guild.id)]['counting_channel'])
        counting = channel
    if data[str(ctx.guild.id)]['welcome_channel'] == None:
        welcome = "Not Set"
    else:
        channel = await self.client.fetch_channel(data[str(ctx.guild.id)]['welcome_channel'])
        welcome = channel
    if data[str(ctx.guild.id)]['log_channel'] == None:
        log = "Not Set"
    else:
        channel = await self.client.fetch_channel(data[str(ctx.guild.id)]['log_channel'])
        log = channel
    em.add_field(name="Counting:", value=counting)
    em.add_field(name="Welcome:", value=welcome)
    em.add_field(name="Log:", value=log)
    return em


async def autorole(self, ctx):
    data = await self.client.get_db()
    em = discord.Embed(title="Autorole", color=ctx.author.color)
    em.timestamp = datetime.datetime.utcnow()
    em.set_footer(text="Use ?autorole  [all/bot] [@roles (you can do more than one)] to set the autorole")
    autorole = data[str(ctx.guild.id)]['autorole']
    all_roles = []
    bot_roles = []
    if len(autorole['all']) == 0:
        em.add_field(name="All", value="Not set")
    else:
        for role in autorole['all']:
            role = ctx.guild.get_role(role)
            all_roles.append(role)
        em.add_field(name="All", value=f"{[role.mention for role in all_roles]}")

    if len(autorole['bot']) == 0:
        em.add_field(name="Bot", value="Not set")
    else:
        for role in autorole['bot']:
            role = ctx.guild.get_role(role)
            all_roles.append(role)
        em.add_field(name="Bot", value=f"{[role.mention for role in all_roles]}")
    return em


async def welcome_text(self, ctx):
    data = await self.client.get_db()
    em = discord.Embed(title="Welcome Text", color=ctx.author.color)
    em.timestamp = datetime.datetime.utcnow()
    em.set_footer(text="Use ?welcome text [text] to set the text")
    wt = data[str(ctx.guild.id)]['welcome']['text_footer']
    em.add_field(name="Text:", value=wt)
    return em


async def autocalc(self, ctx):
    data = await self.client.get_db()

    autocalc = data[str(ctx.guild.id)]['settings']['autocalc']
    if autocalc == True:
        status = "Enabled ✅"
    if autocalc == False:
        status = "Disabled ❌"

    em = discord.Embed(title='Auto Calculator',description=status, color=ctx.author.color)
    em.timestamp = datetime.datetime.utcnow()

    return em


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="This command is used to show the settings for you discord server. You can use this command to quickly check all the current settings to know if you want to change it", extras={"category": "Settings"}, usage="settings", description="Shows the servers Why Bot settings")
    async def settings(self, ctx):
        plugins = await enabled_cogs(self.client, ctx)

        em = discord.Embed(
            title="Settings", description="Use the arrows to look throught the settings", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()

        prefix = discord.Embed(title= "Prefix", description=f"The prefix is `{ctx.prefix}`", color=ctx.author.color)
        prefix.timestamp = datetime.datetime.utcnow()
        prefix.set_footer(
            text=f"You can use {ctx.prefix}setprefix [prefix] to set the prefix")

        channels = await get_channels(self, ctx)
        autoroles = await autorole(self, ctx)
        welcometext = await welcome_text(self, ctx)
        auto_calc = await autocalc(self, ctx)

        ems = [em, plugins, prefix, channels,
            autoroles, auto_calc, welcometext]
        view = Paginator(ctx=ctx, ems=ems)

        message = await ctx.send(embed=em, view=view)
        res = await view.wait()
        if res:
            for i in view.children:
                i.disabled = True
        return await message.edit(view=view)

    @commands.group(help="This command is used to enable/disable plugins for your server. You can stop certain categories from working on this server\nThe plugin name is case sensitive", extras={"category": "Settings"}, usage="plugins [enable/disable] [plugin name]", description="Enable/Disable Plugins for Why bot")
    async def plugins(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Plugins", description=f"Use `{ctx.prefix}plugins [enable/disable] [plugin name]`", color=ctx.author.color)
            em.timestamp = datetime.datetime.utcnow()
            em.add_field(
                name="Plugin List:", value="Counting\nModeration\nEconomy\nTextConvert\nSearch\nWelcome\nLeveling\nMusic\nOnping\nTicket\nMinecraft\nUtilities\nLogging")
            em.set_footer(
                text="This command is case sensitive so please use capital letters")
            await ctx.send(embed=em)

    @plugins.group()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx, plugin: str):
        plist = ["Counting", "Moderation","Economy","TextConvert","Search","Welcome","Leveling","Music","Onping","Ticket","Minecraft","Utilities", "Fun", "Logging"]
        if plugin not in plist:
            return await ctx.send(f"Plugin not found, use `{ctx.prefix}plugins` for a list of them")
        data = await self.client.get_db()
        data[str(ctx.guild.id)]['settings']['plugins'][plugin] = True

        await self.client.update_db(data)

        await ctx.send(f"{plugin} has been enabled")

    @plugins.group()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, plugin: str):
        plist = ["Counting", "Moderation","Economy","TextConvert","Search","Welcome","Leveling","Music","Onping","Ticket","Minecraft","Utilities", "Fun", "Logging"]
        if plugin not in plist:
            return await ctx.send(f"Plugin not found, use `{ctx.prefix}plugins` for a list of them")
        data = await self.client.get_db()
        data[str(ctx.guild.id)]['settings']['plugins'][plugin] = False

        await self.client.update_db(data)

        await ctx.send(f"{plugin} has been disabled")

    @commands.command(usage = "goose_mode", description = "This command toggles goose_mode", help = "This command toggles goose mode which changed autocalc to 9 + 10 = 19 (which is wrong) to the correct answer 21 - Named after my friend who requested this", extras={"category": "Settings"})
    @commands.has_permissions(administrator=True)
    async def goose_mode(self, ctx):
        with open("./database/goose_mode.json") as f:
            data = json.load(f)
        if str(ctx.guild.id) not in data:
            data[str(ctx.guild.id)] = False
            await ctx.send("goose mode off")

        elif data[str(ctx.guild.id)] == False:
            data[str(ctx.guild.id)] = True
            await ctx.send("goose mode on")

        elif data[str(ctx.guild.id)] == True:
            data[str(ctx.guild.id)] = False
            await ctx.send("goose mode off")
        
        with open("./database/goose_mode.json", "w") as f:
            json.dump(data, f, indent=4)



    @commands.command(help="This command is used to set the prefix for the server. Default prefix is ?", extras={"category": "Settings"}, usage="setprefix [prefix]", description="Sets the server prefix")
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, pref: str):
        data = await self.client.get_db()
        data[str(ctx.guild.id)]["prefix"] = pref
        await self.client.update_db(data)
        await ctx.send(embed=discord.Embed(title=f"Prefix has been set to `{pref}`", color=ctx.author.color))

    @commands.command(help="This command turns on autocalc for the server.\nAuto calc basicaly autocalculates any thing you type. For example in chat you type\n1 + 1\nin chat, The bot will reply 2", extras={"category": "Settings"}, usage="autocalc [True/false]", description="Toggles autocalc for this server")
    @commands.has_permissions(administrator=True)
    async def autocalc(self, ctx, ena):
        data = await self.client.get_db()
        if ena.lower() == "true":
            status = "Enabled ✅"
            data[str(ctx.guild.id)]["settings"]['autocalc'] = True
        elif ena.lower() == "false":
            data[str(ctx.guild.id)]["settings"]['autocalc'] = False
            status = "Disabled ❌"
        else:
            await ctx.send("Invalid option. Only `true` or `false`")
        await self.client.update_db(data)
        await ctx.send(embed=discord.Embed(title=f"Autocalc is {status}", color=ctx.author.color))


def setup(client):
    client.add_cog(Settings(client))
