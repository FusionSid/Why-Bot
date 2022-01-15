# Slash commands
import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ui import Button, View
from discord import Option
import json
import random
import os
from utils import is_it_me

cogs = []
for i in os.listdir("cogs/"):
    if i == "__pycache__":
        pass
    else:
        print(i[:-3])


async def get_roast():
    with open('./database/roastlist.json') as f:
        data = json.load(f)
    return random.choice(data)


class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name="hi", description="Hello")
    async def hello(self, ctx, user: Option(discord.Member, "The user", required=False) = None):
        if user is None:
            await ctx.respond("Hello")
        else:
            await ctx.respond(f"Hello {user.mention}")

    @slash_command(name="set", description="Set Channels")
    async def set(self, ctx, category: Option(str, "Category", required=True, choices=["Mod/Log Channel", "Counting Channel", "Welcome Channel"]), channel: Option(discord.TextChannel, "The channel", required=True)):
        channel_id = channel.id
        with open("./database/db.json") as f:
            data = json.load(f)

        if category == "Mod/Log Channel":
            for i in data:
                if i["guild_id"] == ctx.guild.id:
                    i["log_channel"] = channel_id

        elif category == "Counting Channel":
            for i in data:
                if i["guild_id"] == ctx.guild.id:
                    i["counting_channel"] = channel_id

        elif category == "Welcome Channel":
            for i in data:
                if i["guild_id"] == ctx.guild.id:
                    i["welcome_channel"] = channel_id
        await ctx.respond(f"{channel.name} successfully set as {category}")
        with open("./database/db.json", 'w') as f:
            json.dump(data, f, indent=4)

    @slash_command(name="rps", description="rock paper scissors")
    async def rps(self, ctx, rps: Option(str, "Rock Paper or Scissors", required=True, choices=["Rock", "Paper", "Scissors"])):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors")
        rps = rps.lower()
        if rps == 'rock':
            if cpu_choice == 'rock':
                em.description = "It's a tie!"
            elif cpu_choice == 'scissors':
                em.description = "You win!"
            elif cpu_choice == 'paper':
                em.description = "You lose!"

        elif rps == 'paper':
            if cpu_choice == 'paper':
                em.description = "It's a tie!"
            elif cpu_choice == 'rock':
                em.description = "You win!"
            elif cpu_choice == 'scissors':
                em.description = "You lose!"

        elif rps == 'scissors':
            if cpu_choice == 'scissors':
                em.description = "It's a tie!"
            elif cpu_choice == 'paper':
                em.description = "You win!"
            elif cpu_choice == 'rock':
                em.description = "You lose!"

        else:
            em.description = "Invalid Input"

        em.add_field(name="Your Choice", value=rps)
        em.add_field(name="Bot Choice", value=cpu_choice)
        await ctx.respond(embed=em)

    @slash_command(name="roast", description="Bot roasts you")
    async def roast(self, ctx):
        roast = await get_roast()
        em = discord.Embed(title=roast)
        await ctx.respond(embed=em)

    @slash_command(name="dm", description="The bot dms someone for you")
    async def dm(self, ctx, member: Option(discord.Member, "The person you want to dm", required=True), message: Option(str, 'The message', required=True)):
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)
        await ctx.respond("Done")

    @slash_command(name="sendroast", description="the bot sends someone a roast")
    async def sendroast(self, ctx, member: Option(discord.Member, "The person you want to roast", required=True)):
        message = await get_roast()
        embeddm = discord.Embed(
            title=message, description="Imagine being roasted by a bot")
        await member.send(embed=embeddm)
        await ctx.respond("Done")

    @slash_command(name="say", description="The bot says what you want")
    async def say(self, ctx, text: Option(str, "The text", required=True)):
        await ctx.respond(text)

    @slash_command(name="invite", description="Creates 10 day invite for this server")
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=10)
        await ctx.respond(link)

    @slash_command(name="botinvite", description="Invite why to your server :)")
    async def botinvite(self, ctx):
        await ctx.respond(embed=discord.Embed(title="Invite **Why?** to your server:", description="https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"))

    @slash_command(name="suggest", description="Suggest something for why bot")
    async def suggest(self, ctx, suggestion: Option(str, "The suggestion", required=True)):
        sid = await self.client.fetch_channel(925157029092413460)
        await sid.send(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.respond("Thank you for you suggestion!")

    @slash_command(name="ping", description="shows you the bots ping")
    async def ping(self, ctx):
        await ctx.respond(f"{round(self.client.latency * 1000)}ms")

    @slash_command(name="reload", description="reloads a cog")
    @commands.check(is_it_me)
    async def reload(self, ctx, extension:Option(str, "Cog Name", required=True, choices=cogs)):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(Slash(client))
