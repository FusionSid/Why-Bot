import discord
import datetime
from discord.ext import commands
import json
from utils import Log, is_it_me
from utils import update_activity

log = Log()

async def startguildsetup(client, id):
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
    data = await client.get_db()
    
    if str(id) in data:
        pass
    else:
        data[str(id)] = file
        await client.update_db(data)

    newtickettemplate = {"ticket-counter": 0, "valid-roles": [],"pinged-roles": [], "ticket-channel-ids": [], "verified-roles": []}
    with open(f"./database/tickets/ticket{id}.json", 'w') as f:
        json.dump(newtickettemplate, f, indent=4)
    with open(f"./database/counting.json") as f:
        dataa = json.load(f)
    dataa[f"{id}"] = 0
    with open(f"./database/counting.json", 'w') as f:
        json.dump(dataa, f, indent=4)



class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        await update_activity(self.client)
        cha = self.client.get_channel(925513395883606129)
        em = discord.Embed(title="Leave", description=f"Left: {guild.name}", color=discord.Color.red())
        em.timestamp = datetime.datetime.utcnow()
        await cha.send(embed=em)
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        chaem = discord.Embed(title="Join", description=f"Joined: {guild.name}", color=discord.Color.green())
        chaem.timestamp = datetime.datetime.utcnow()
        cha = self.client.get_channel(925513395883606129)
        await cha.send(embed=chaem)
        await update_activity(self.client)
        await startguildsetup(self.client, guild.id)
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
        embed.timestamp = datetime.datetime.utcnow()

        await guild.system_channel.send(content="**Thanks for inviting me! :wave: **", embed=embed)


    @commands.command()
    @commands.check(is_it_me)
    async def update_all_non_db(self, ctx):
        for guild in self.client.guilds:
            id = guild.id
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
            data = await self.client.get_db()
            
            
            if str(id) in data:
                pass
            else:
                data[str(id)] = file
                await self.client.update_db(data)
            
            newtickettemplate = {"ticket-counter": 0, "valid-roles": [],"pinged-roles": [], "ticket-channel-ids": [], "verified-roles": []}
            with open(f"./database/tickets/ticket{id}.json", 'w') as f:
                json.dump(newtickettemplate, f, indent=4)
            with open(f"./database/counting.json") as f:
                dataa = json.load(f)
            dataa[f"{id}"] = 0
            with open(f"./database/counting.json", 'w') as f:
                json.dump(dataa, f, indent=4)

def setup(client):
    client.add_cog(Events(client))