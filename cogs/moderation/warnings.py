import discord
from discord.ext import commands
from utils import plugin_enabled, get_log_channel
import datetime


class Warnings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="This command is used to warn a user\nThe warning gets added and you can use the warnings command to check the users warnings", extras={"category":"Moderation"}, usage="warn [@user] [reason]", description="Warns a user")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member.id in [ctx.author.id, self.client.user.id]:
            return await ctx.send("You cant warn yourself/me LMAO")

        now = datetime.datetime.utcnow()

        time = now.strftime("%Y-%m-%d %H:%M:%S")
        if reason == None:
            reason = "None"

        data = await self.client.get_db()

        warn = {'time': time, 'reason': reason}
        try:
            data[str(ctx.guild.id)]['warnings'][f"{member.id}"].append(warn)
        except Exception:
            data[str(ctx.guild.id)]['warnings'][f"{member.id}"] = []
            data[str(ctx.guild.id)]['warnings'][f"{member.id}"].append(warn)

        await self.client.update_db(data)
        channel = await get_log_channel(self, ctx.guild)
        if channel != None:
            return await channel.send(embed=discord.Embed(title="Warn", description=f"***{member.mention}*** has been warned", color=ctx.author.color))
        await ctx.send(embed=discord.Embed(title="Warn", description=f"***{member.mention}*** has been warned", color=ctx.author.color))

    @commands.command(help="This commands shows all the warnings that a user has", extras={"category":"Moderation"}, usage="warnings [@user]", description="Displays a users warnings")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def warnings(self, ctx, member: discord.Member):
        data = await self.client.get_db()
        warns = data[str(ctx.guild.id)]['warnings']
        try:
            warnings = warns[f'{member.id}']
        except Exception:
            return await ctx.send("This person has no warnings")

        em = discord.Embed(title="WARNINGS:", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        for i in warnings:
            t = i["time"]
            r = i["reason"]
            em.add_field(name=t, value=f"Reason: {r}")

        await ctx.send(embed=em)



def setup(client):
    client.add_cog(Warnings(client))    
    