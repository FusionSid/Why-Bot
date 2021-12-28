# Slash commands
import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ui import Button, View
from discord import Option
import json


class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(guild_ids=[763348615233667082,893653614990606346], name="hi", description="Hello")
    async def hello(self, ctx, user: Option(discord.Member, "The user", required=False) = None):
        if user is None:
            await ctx.respond("Hello")
        else:
            await ctx.respond(f"Hello {user.mention}")

    @slash_command(guild_ids=[763348615233667082,893653614990606346], name="set", description="Set Channels")
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

def setup(client):
    client.add_cog(Slash(client))
