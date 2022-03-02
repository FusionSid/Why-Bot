import discord
from utils.checks import plugin_enabled
from discord.ext import commands
import datetime


class Onping(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.group(aliases=["on_pinged", 'pinged', 'onping'], help="This command is used to set the Onping message when you get pinged\nYou can use: onpinged set - to set your onpinged message\nYou can use: onpinged clear to clear your onping message\nYou can use this command without a subcommand and it will display the message", extras={"category": "Onping"}, usage="onpinged [set/clear(optional)]", description="Sets your Onpinged message")
    @commands.check(plugin_enabled)
    async def onpinged(self, ctx):
        if ctx.invoked_subcommand is None:
            user = await self.client.get_user_db()
            user = user[str(ctx.author.id)]

            on_pinged_message = user['on_pinged']
            em = discord.Embed()
            em.timestamp = datetime.datetime.utcnow()

            if on_pinged_message["title"] == None and on_pinged_message["description"] == None:
                return await ctx.send(embed=discord.Embed(title="You have no on pinged message set.", description=f"Use `{ctx.prefix}onpinged set` to set one"))

            if on_pinged_message["title"] == None:
                pass
            else:
                em.title = on_pinged_message["title"]

            if on_pinged_message["description"] == None:
                pass
            else:
                em.description = on_pinged_message["description"]

            if on_pinged_message["color"] == None:
                pass
            else:
                em.color = on_pinged_message["color"]

            await ctx.send(embed=em)


    @onpinged.command()
    @commands.check(plugin_enabled)
    async def set(self, ctx):

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        colors = {
        "none": None,
        "blue": 0x3498db,
        "blurple": 0x5865f2,
        "brand_green": 0x57f287,
        "brand_red": 0xed4245,
        "dark_blue": 0x206694,
        "dark_gold": 0xc27c0e,
        "dark_gray": 0x607d8b,
        "dark_green": 0x1f8b4c,
        "dark_grey": 0x607d8b,
        "dark_magenta": 0xad1457,
        "dark_orange": 0xa84300,
        "dark_purple": 0x71368a,
        "dark_red": 0x992d22,
        "dark_teal": 0x11806a,
        "dark_theme": 0x36393f,
        "darker_gray": 0x546e7a,
        "darker_grey": 0x546e7a,
        "fuchsia": 0xeb459e,
        "gold": 0xf1c40f,
        "green": 0x2ecc71,
        "greyple": 0x99aab5,
        "light_gray": 0x979c9f,
        "light_grey": 0x979c9f,
        "lighter_gray": 0x95a5a6,
        "lighter_grey": 0x95a5a6,
        "magenta": 0xe91e63,
        "nitro_pink": 0xf47fff,
        "og_blurple": 0x7289da,
        "orange": 0xe67e22,
        "purple": 0x9b59b6,
        "random": 0x00d1ff,
        "red": 0xe74c3c,
        "teal": 0x1abc9
        }

        await ctx.send("Type the title for the embed (or type none if you dont want one)")
        title = await self.client.wait_for("message", check=check, timeout=300)
        title = title.content
        if title.lower() == 'none':
            title = None

        await ctx.send("Type the description for the embed (or type none if you dont want one)")
        description = await self.client.wait_for("message", check=check, timeout=300)
        description = description.content
        if description.lower() == 'none':
            description = None

        await ctx.send("Choose color from this list:\nEnter the color you want (or type none if you want the default:)")
        color = await self.client.wait_for("message", check=check, timeout=300)
        color = color.content
        color = color.lower()

        if color.lower() in colors.keys():
            color = colors[color]
        else:
            color = None

        data = await self.client.get_user_db()

        data[str(ctx.author.id)]['on_pinged']['title'] = title
        data[str(ctx.author.id)]['on_pinged']['description'] = description
        data[str(ctx.author.id)]['on_pinged']['color'] = color

        await self.client.update_user_db(data)


    @onpinged.command(aliases=['reset'])
    @commands.check(plugin_enabled)
    async def clear(self, ctx):
        data = await self.client.get_user_db()
        data[str(ctx.author.id)]["on_pinged"]["title"] = None
        data[str(ctx.author.id)]["on_pinged"]["description"] = None
        data[str(ctx.author.id)]["on_pinged"]["color"] = None
        await self.client.update_user_db(data)
        await ctx.send(embed=discord.Embed(title="On-Ping", description="RESET", color=ctx.author.color))


    @onpinged.command()
    @commands.check(plugin_enabled)
    async def toggle(self, ctx):
        data = await self.client.get_user_db()
        if data[str(ctx.author.id)]["on_pinged_toggled"] == True:
            data[str(ctx.author.id)]["on_pinged_toggled"] = False
            await ctx.send(embed=discord.Embed(title="On-Ping", description="Toggled Off", color=ctx.author.color))

        elif data[str(ctx.author.id)]["on_pinged_toggled"] == False:
            data[str(ctx.author.id)]["on_pinged_toggled"] = True
            await ctx.send(embed=discord.Embed(title="On-Ping", description="Toggled On", color=ctx.author.color))

        await self.client.update_user_db(data)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.author.bot:
            return

        data = await self.client.get_db()
        if data[str(message.guild.id)]['settings']['plugins']['Onping'] == False:
            return

        user_data = await self.client.get_user_db()

        for key, value in user_data.items():
            if message.reference != None:
                return

            em = discord.Embed()
            em.timestamp = datetime.datetime.utcnow()
            em.title = value["on_pinged"]["title"]
            em.description = value["on_pinged"]["description"]

            if em.title and em.description is None:
                    return
            if value["on_pinged"]["color"] == None:
                pass
            else:
                em.color = value["on_pinged"]["color"]
                
            if f"<@!{value['user_id']}>" in message.content or f"<@{value['user_id']}>" in message.content:
                if value['user_id'] == message.author.id:
                    return
                try:
                    return await message.reply(embed=em)
                except Exception as err:
                    print(err)


def setup(client):
    client.add_cog(Onping(client))
