import discord
import random
import os
import json
import requests
from discord.ext import commands

api_key = os.environ['HYPIXEL']


async def get_uuid(user):
    url = f'https://api.mojang.com/users/profiles/minecraft/{user}?'
    response = requests.get(url)
    uuid = response.json()
    uuid = uuid['id']
    return uuid


async def get_user_uuid(ctx):
    with open('igns.json', 'r') as f:
        users = json.load(f)

        for user in users:
            if user["id"] == ctx.author.id:
                uuid = user["uuid"]
                return uuid
    await ctx.send("You havent set your ign yet. Use setign to set it")


async def get_hydata(uuid):
    url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
    response = requests.get(url).json()
    return response


class Minecraft(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['uuid'])
    async def getuuid(self, ctx, player=None):
        if player == None:
            uuid = await get_user_uuid(ctx)
        else:
            uuid = await get_uuid(str(player))
        await ctx.send(embed=discord.Embed(title="Your uuid:", description=f'{uuid}'))

    # Register IGN

    @commands.command(aliases=['ign'])
    async def setign(self, ctx):
        client = self.client
        confirm = False

        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author

        with open('igns.json', 'r') as f:
            users = json.load(f)

            for user in users:
                if user["id"] == ctx.author.id:
                    await ctx.send("You've already set you ign, Would you like to change it?\ny/n")
                    confirm = await client.wait_for("message", check=wfcheck)
                    confirm = confirm.content
                    if confirm.lower() == "y":
                        index = users.index(user)
                        lmao = users.remove[index]
                        confirm = True
                        break
                    else:
                        return
        if confirm == True:
            with open('igns.json', 'w') as f:
                json.dump(lmao, f, indent=4)
        await ctx.send("Enter your Minecraft ign:")
        ign = await client.wait_for("message", check=wfcheck)
        ign = str(ign.content)
        uuid = await get_uuid(ign)
        user = {"id": ctx.author.id, "uuid": uuid}
        with open('igns.json') as f:
            users = json.load(f)
            users.append(user)
        with open('igns.json', 'w') as f:
            json.dump(users, f, indent=4)

    # Hypixel image

    @commands.command(aliases=['hypixel'])
    async def hystats(self, ctx, player=None):
        if player == None:
            uuid = await get_user_uuid(ctx)
        else:
            uuid = await get_uuid(str(player))

        #    response = await get_hydata(uuid)
        #    player = response["player"]
        #    player_name = player["displayname"]
        #    lastLogin = player["lastLogin"]
        #    lastLogout = player["lastLogout"]

        #    if "monthlyPackageRank" in player:
        #        rank = "MVP++"
        #        full_ign = "{} {}".format(rank, player_name)
        #    elif "newPackageRank" in player:
        #        rank = player["newPackageRank"]
        #        if "_PLUS" in rank:
        #            rank = rank.replace("_PLUS", '+')
        #        full_ign = "{} {}".format(rank, player_name)
        #    else:
        #        rank = None
        #        full_ign = player_name

        #    if lastLogout < lastLogin:
        #        online = "Yes"
        #    else:
        #        online = "No"

        url = "https://hypixel.paniek.de/signature/{}/general-tooltip".format(
            uuid)
        response = requests.get(url)
        with open('hypixel_pic.png', 'wb') as f:
            f.write(response.content)
        await ctx.send(file=discord.File('hypixel_pic.png'))
        os.remove('hypixel_pic.png')

        # em = discord.Embed(title="Extra:")
        # em.add_field(name="IGN:", value=full_ign)
        # em.add_field(name="Online:", value=online)
        # await ctx.send(embed=em)


    @commands.command(aliases=['bw', 'bedwars'])
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
                           description="For {}".format(full_ign))
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


    @commands.command()
    async def bwchallenge(self, ctx):
        challenges = [
            "Ironman [All Modes]\nWin a game using only items that you can buy with iron.",
            "Midas [All Modes]\nWin a game using only items that you can buy with gold.",
            "Diamondy [All Modes]\nWin a game buying only wool and team-upgrades.",
            "Greedy Villager [All Modes]\nWin a game using only items you can buy with emeralds and wool.",
            "Upgradeless [SOLO only]\nWin a game with no team-upgrades.",
            "Emerald Forger [SOLO only]\nWin a game using only emeralds from your forge (you cant get emeralds from middle)",
            "Sudden Master [All Modes]\nKill a Sudden Death dragon.",
            "Bed Destroyer [4v4v4v4 only]\nBreak all the 3 beds of a 4v4v4v4 game.",
            "Pacifist [SOLO or DOUBLES]\nWin a game without breaking any beds.",
            "Middle Control [All Modes]\nBe in the middle collecting emeralds for 2 minutes in a row.",
            "Forever Alone [3v3v3v3 or 4v4v4v4]\nWin a team-game alone.",
            "Shouter [All Modes]\nShout 10 times in a single game.",
            "Storer [All Modes]\nFill your entire enderchest.",
            "Knockpower [SOLO only]\nWin a game using only the Knockback Stick as weapon.",
            "Trap Activator [All Modes]\nActivate 3 Its a Trap!s in a single game.",
            "Rusher [All Modes]\nBreak a bed in less than 100 seconds after the game started.",
            "Builder [All Modes]\nPlace 1000+ blocks of any type on a single game.",
            "Sleepless [SOLO only]\nWin a SOLO game without a bed.",
            "Ultimate Teamwork [4v4v4v4 only]\nWin a 4v4v4v4 game with none of your teammates dead.",
            "Prestige Diamond [SOLO and DOUBLES only]\nGet all Team-Upgrades to the max level.",
            "Money Waster\nBuy at least one of every single item on the shop.",
            "Feeding the Voidn\nThrow 10 players in the Void on a single Bedwars game.",
            "Player Finisher\nWin a game with only Final Kills.",
            "Oops, I reached a limit!\nFall in the Void after reaching the border of the map.",
            "Trust Your Pets\nWin a game getting kills only with your pets. (Silverfish and IG)"
        ]
        challenge = random.choice(challenges)
        await ctx.send(embed=discord.Embed(title="Bedwars challenge", description=challenge))


def setup(client):
    client.add_cog(Minecraft(client))
