import discord
import random
import os
import json
from discord.ext import commands
import datetime
import dotenv
from utils.checks import plugin_enabled
import aiohttp
import aiofiles
from mcstatus import MinecraftServer, MinecraftBedrockServer

dotenv.load_dotenv()

api_key = os.environ['HYPIXEL']


async def get_uuid(user):
    url = f'https://api.mojang.com/users/profiles/minecraft/{user}?'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            uuid =  await response.json()
    uuid = uuid['id']
    return uuid


async def get_user_uuid(ctx):
    with open('./database/igns.json', 'r') as f:
        users = json.load(f)

        for user in users:
            if user["id"] == ctx.author.id:
                uuid = user["uuid"]
                return uuid
    await ctx.send("You havent set your ign yet. Use setign to set it")


async def get_hydata(uuid):
    url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
    return await response.json()


class Minecraft(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['uuid'], extras={"category":"Minecraft"}, usage="getuuid [ign(optional)]", help="This command will return your minecraft ign.\nIf you have used setign before then you wont have to specify the user.", description="Returns your minecraft ign")
    @commands.check(plugin_enabled)
    async def getuuid(self, ctx, player=None):
        if player == None:
            uuid = await get_user_uuid(ctx)
        else:
            uuid = await get_uuid(str(player))
        await ctx.send(embed=discord.Embed(title="Your uuid:", description=f'{uuid}', color=ctx.author.color))

    # Register IGN

    @commands.command(aliases=['ign'], extras={"category":"Minecraft"}, usage="setign", help="This command sets your minecraft ign.\nIf you use this command you wont have to specify the ign in other mincraft commands", description="Sets you minecraft ign")
    @commands.check(plugin_enabled)
    async def setign(self, ctx):
        client = self.client
        confirm = False

        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author

        with open('./database/igns.json', 'r') as f:
            users = json.load(f)

            for user in users:
                if user["id"] == ctx.author.id:
                    await ctx.send("You've already set you ign, Would you like to change it?\ny/n")
                    confirm = await client.wait_for("message", check=wfcheck, timeout=300)
                    confirm = confirm.content
                    if confirm.lower() == "y":
                        await ctx.send("Enter your Minecraft ign:")
                        ign = await client.wait_for("message", check=wfcheck, timeout=300)
                        ign = str(ign.content)
                        uuid = await get_uuid(ign)
                        user["uuid"] = uuid
                        with open('./database/igns.json', 'w') as f:
                            json.dump(users, f, indent=4)
                        return
                    else:
                        return
        await ctx.send("Enter your Minecraft ign:")
        ign = await client.wait_for("message", check=wfcheck, timeout=300)
        ign = str(ign.content)
        uuid = await get_uuid(ign)
        user = {"id": ctx.author.id, "uuid": uuid}
        with open('./database/igns.json') as f:
            users = json.load(f)
            users.append(user)
        with open('./database/igns.json', 'w') as f:
            json.dump(users, f, indent=4)

    # Hypixel image

    @commands.command(aliases=['hypixel'], extras={"category":"Minecraft"}, usage="hystats [ign(optional)]", help="This command shows the hypixel stats for a Hypixel user.\nYou can specify an ign or if youve used setign befre you wont have to", description="Shows a nice pic of your hypixel stats")
    @commands.check(plugin_enabled)
    async def hystats(self, ctx, player=None):
        if player == None:
            uuid = await get_user_uuid(ctx)
        else:
            uuid = await get_uuid(str(player))

        url = "https://hypixel.paniek.de/signature/{}/general-tooltip".format(
            uuid)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open('./tempstorage/hypixel_pic.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        await ctx.send(file=discord.File('./tempstorage/hypixel_pic.png'))
        os.remove('./tempstorage/hypixel_pic.png')


    @commands.command(aliases=['bw', 'bedwars'], extras={"category":"Minecraft"}, usage="bwstats [ign(optional)", help="This command shows the hypixel bedwars stats for a Hypixel user.\nYou can specify an ign or if youve used setign befre you wont have to", description="Shows your bedwars stats")
    @commands.check(plugin_enabled)
    async def bwstats(self, ctx, player=None):
        if player == None:
            uuid = await get_user_uuid(ctx)
        else:
            uuid = await get_uuid(str(player))
        response = await get_hydata(uuid)

        player = response["player"]
        stats = player["stats"]
        player_name = player["displayname"]

        # Stats
        bw_stats = stats["Bedwars"]

        # Bedwars
        bw_level = player["achievements"]["bedwars_level"]
        bw_wins = bw_stats["wins_bedwars"]
        bw_losses = bw_stats["losses_bedwars"]
        bw_winstreak = bw_stats["winstreak"]
        bw_coins = bw_stats["coins"]
        bw_gold = bw_stats["gold_resources_collected_bedwars"]
        bw_iron = bw_stats["iron_resources_collected_bedwars"]
        bw_dias = bw_stats["diamond_resources_collected_bedwars"]
        bw_ems = bw_stats["emerald_resources_collected_bedwars"]
        bw_resources = bw_stats["resources_collected_bedwars"]
        bw_kills = bw_stats["kills_bedwars"]
        bw_deaths = bw_stats["deaths_bedwars"]
        bw_beds = bw_stats["beds_broken_bedwars"]
        bw_finals = bw_stats["final_kills_bedwars"]

        if "monthlyPackageRank" in player:
            rank = "MVP++"
            full_ign = "{} {}".format(rank, player_name)
        elif "newPackageRank" in player:
            rank = player["newPackageRank"]
            if "_PLUS" in rank:
                rank = rank.replace("_PLUS", '+')
            full_ign = "{} {}".format(rank, player_name)
        else:
            rank = None
            full_ign = player_name

        em = discord.Embed(title="Bedwars Stats:",
                           description="For {}".format(full_ign), color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        stats_values = [bw_level, bw_wins, bw_losses, bw_winstreak, bw_coins, bw_gold,
                        bw_iron, bw_dias, bw_ems, bw_resources, bw_kills, bw_deaths, bw_beds, bw_finals]
        stat_keys = ["Bedwars Level", "Wins", "Losses", "Current Winstreak", "Coins",
                     "Gold Collected", "Iron Collected", "Diamonds Collected", "Emeralds Collected", "Overall Resources", "Kills", "Deaths", "Beds Broken", "Final Kills"]

        dictionary = dict(zip(stat_keys, stats_values))

        for i in stat_keys:
            key = i
            value_ = dictionary[key]
            em.add_field(name=key, value=value_)
        await ctx.send(embed=em)


    @commands.command(help="Gets the status of a minecraft server", usage="mcstatus [bedrock/java] [server_ip]", description="Gets mc status", extras={"category" : "Search"})
    async def mcstatus(self, ctx, type_:str, server_ip:str):
        if type_.lower() == "bedrock":
            server = MinecraftBedrockServer.lookup(server_ip)

            status = server.status()

            em = discord.Embed(
                title = "Minecraft Server Status:",
                description = f"Looking for a bedrock server: {server_ip}",
                color = discord.Color.random()
            )

            em.add_field(
                name = "Ping",
                value = f"{round(status.latency, 2)}ms"
            )
            em.add_field(
                name = "Players Online:",
                value = status.players_online
            )
            
            await ctx.send(embed=em)
        if type_.lower() == "java":
            server = MinecraftServer.lookup(server_ip)

            status = server.status()

            em = discord.Embed(
                title = "Minecraft Server Status:",
                description = f"Looking for a java server: {server_ip}",
                color = discord.Color.random()
            )

            em.add_field(
                name = "Ping",
                value = f"{round(status.latency, 2)}ms"
            )
            em.add_field(
                name = "Players Online:",
                value = status.players.online
            )
            
            await ctx.send(embed=em)



def setup(client):
    client.add_cog(Minecraft(client))
