import discord
import random
from discord.ext import commands
import json
from datetime import datetime
from utils import Log

log = Log("./database/log.txt", timestamp=True)

async def startguildsetup(id):
    file = {
        "guild_id": id,
        "prefix": "?",
        "counting_channel": None,
        "lastcounter": None,
        "log_channel": None,
        "welcome_channel": None,
        "announcement_channel" : None,
        "warnings": {
        },
        "settings": {
            "autocalc":True,
        "plugins": {
            "Counting": True,
            "Moderation": True,
            "Economy": True,
            "TextConvert": True,
            "Search": True,
            "Welcome": True,
            "Leveling": True,
            "Music": True,
            "Onping": True,
            "Ticket": True,
            "Minecraft": True,
            "Utilities": True,
            "Fun": True
        }
        },
        "autorole": {
            "all": None,
            "bot": None
        },
        "welcome" : {
            "bg_color" : None,
            "text_color" : None,
            "text_footer" : None,
            "bg_image" : None
        }
    }
    with open("database/db.json") as f:
        data = json.load(f)
    
    alr_in = False
    
    for i in data:
        if i["guild_id"] == id:
            alr_in = True
        else:
            alr_in = False
    
    if alr_in == False:
        data.append(file)
        with open("database/db.json", 'w') as f:
            json.dump(data, f, indent=4)
    newtickettemplate = {"ticket-counter": 0, "valid-roles": [],
                        "pinged-roles": [], "ticket-channel-ids": [], "verified-roles": []}
    with open(f"tickets/ticket{id}.json", 'w') as f:
        json.dump(newtickettemplate, f, indent=4)
    with open(f"database/counting.json") as f:
        data = json.load(f)
    data[f"{id}"] = 0
    with open(f"database/counting.json", 'w') as f:
        json.dump(data, f, indent=4)

async def update_activity(client):
    await client.change_presence(activity=discord.Game(f"On {len(client.guilds)} servers! | ?help"))
    print("Updated presence")

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        cha = self.client.get_channel(925513395883606129)
        await cha.send(embed=discord.Embed(title="Join", description=f"Joined: {guild.name}", color=discord.Color.green()))
        await update_activity(self.client)
        await startguildsetup(guild.id)
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name="Here's some stuff to get you started:")
        embed.add_field(name="Default Prefix: `?`",
                        value="This can be changed later using `?setprefix`")
        embed.add_field(name="Channel Setting",
                        value="To set the counting, mod and welcome channel use `/set`")
        embed.add_field(
            name="Settings", value="You can use `?settings` to change some bot settings")
        embed.set_footer(
            text=f"Thank You - Why bot is now on {len(self.client.guilds)} servers!")
        try:
            await guild.system_channel.send(content="**Thanks for inviting me! :wave: **", embed=embed)
        except Exception as e:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        await update_activity(self.client)
        cha = self.client.get_channel(925513395883606129)
        await cha.send(embed=discord.Embed(title="Leave", description=f"Left: {guild.name}", color=discord.Color.red()))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        log.log_error(error)

        if isinstance(error, commands.CommandOnCooldown):
            async def better_time(cd: int):
                time = f"{cd}s"
                if cd > 60:
                    minutes = cd - (cd % 60)
                    seconds = cd - minutes
                    minutes = int(minutes / 60)
                    time = f"{minutes}min {seconds}s"
                    if minutes > 60:
                        hoursglad = minutes - (minutes % 60)
                        hours = int(hoursglad / 60)
                        minutes = minutes - (hours*60)
                        time = f"{hours}h {minutes}min {seconds}s"
                return time
                
            cd = round(error.retry_after)
            if cd == 0:
                cd = 1
            retry_after = await better_time(cd)
            em = discord.Embed(
                title="Wow buddy, Slow it down\nThis command is on cooldown",
                description=f"Try again in **{retry_after}**",
                color = discord.Color.red()
            )
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                title="Missing a requred value/arg",
                description="You haven't passed in all value/arg",
                color = discord.Color.red()
            )
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(
                title="Missing permissions",
                description="You don't have permissions to use this commands",
                color = discord.Color.red()
            )
            await ctx.send(embed=em)

def setup(client):
    client.add_cog(Events(client))