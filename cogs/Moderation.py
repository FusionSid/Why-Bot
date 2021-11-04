import discord
from datetime import datetime
import sqlite3
from discord.ext import commands
import os
import json

cd = "/home/runner/Why-Bot/cogs/"
dbpath = "/home/runner/Why-Bot/MainDB"


async def create_voice(guild, name, cat, limit=None):
    category = await guild.get_category_by_name(guild, cat)
    await guild.create_voice_channel(name, category=category, user_limit=limit)


async def get_log_channel(self, ctx):
    try:
        os.chdir("/home/runner/Why-Bot/Setup")
        with open(f"{ctx.guild.id}.json") as f:
            content = json.load(f)
        if content[0]["mod_channel"] == None:
            return
        else:
            channel = int(content[0]["mod_channel"])
        os.chdir(cd)
        return await self.client.fetch_channel(channel)
    except:
        return False


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rp'])
    async def report(self, ctx, type_: str):
        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author
        os.chdir("/home/runner/Why-Bot/Setup")
        with open(f"{ctx.guild.id}.json") as f:
            content = json.load(f)
        if content[0]["mod_channel"] == None:
            return
        else:
            channel = int(content[0]["mod_channel"])
        os.chdir(cd)
        em = discord.Embed(title="REPORT")

        if type_.lower() == "member":

            await ctx.send("Enter the @ of the member")
            member = await self.client.wait_for("message", check=wfcheck)
            member = member.content
            await ctx.send("Please give a short description about why you are reporting this person")
            reason = await self.client.wait_for("message", check=wfcheck)
            reporter = reason.author
            reason = reason.content
            em.description = "Member Report"
            em.add_field(name="Member:", value=member)
            em.add_field(name="Reason:", value=reason)
            em.add_field(name="Report By:", value=reporter)
            cha = await self.client.fetch_channel(channel)
            await cha.send(embed=em)

        elif type_.lower() == "message":

            await ctx.send("Enter the id of the message")
            messageid = await self.client.wait_for("message", check=wfcheck)
            messageid = messageid.content

            try:
                int(messageid)
            except:
                return

            await ctx.send("Please give a short description about why you are reporting this message")
            reason = await self.client.wait_for("message", check=wfcheck)
            reporter = reason.author
            reason = reason.content

            message = await ctx.channel.fetch_message(messageid)
            messagecontent = message.content
            messageauthor = message.author

            em.description = "Message Report"
            em.add_field(name="Reason:", value=reason, inline=False)
            em.add_field(name="Message Content:", value=messagecontent, inline=False)
            em.add_field(name="Message Author:", value=messageauthor, inline=False)
            em.add_field(name="Report By:", value=reporter, inline=False)
            cha = await self.client.fetch_channel(channel)
            await cha.send(embed=em)

        elif type_.lower() == "bug":

            await ctx.send("Please give a short description about the issure/bug")
            reason = await self.client.wait_for("message", check=wfcheck)
            reporter = reason.author
            reason = reason.content
            em.description = "Bug Report"
            em.add_field(name="Reason", value=reason)
            em.add_field(name="Report By:", value=reporter)

            cha = await self.client.fetch_channel(896932591620464690)
            await cha.send(embed=em)


    @commands.command(aliases=['grole'])
    @commands.has_permissions(administrator=True)
    async def giverole(self, ctx, role: discord.Role, user: discord.Member):
        await user.add_roles(role)
        channel = await get_log_channel(self, ctx)
        if channel == False:
            return channel.send(embed=discord.Embed(title="Give Role", description=f"***{user.mention}*** has been given the ***{role.mention}*** role"))
        else:
            pass
        await ctx.send(f"{user} has been given the {role} role")


    @commands.command(aliases=['trole'])
    @commands.has_permissions(administrator=True)
    async def takerole(self, ctx, role: discord.Role, user: discord.Member):
        await user.remove_roles(role)
        channel = await get_log_channel(self, ctx)
        if channel == False:
            return channel.send(embed=discord.embed(title="Remove Role", description=f"***{role.mention}*** has been removed from ***{user.mention}***"))
        else:
            pass
        await ctx.send(f"{role} has been removed from {user}")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await user.ban(reason=reason)
        channel = await get_log_channel(self, ctx)
        if channel == False:
            return channel.send(embed=discord.embed(title="Ban", description=f"***{user.mention}*** has been banned"))
        else:
            pass
        await ctx.send(f"User {user} has been banned")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        channel = await get_log_channel(self, ctx)
        if channel == False:
            return channel.send(embed=discord.embed(title="Kick", description=f"***{user.mention}*** has been kicked"))
        else:
            pass
        await ctx.send(f"User {user} has been kicked")


    @commands.command(aliases=['lock'])
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await channel.send("Channel is now in lockdown")
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        cha = await get_log_channel(self, ctx)
        if cha == False:
            return cha.send(embed=discord.embed(title="Lockdown", description=f"***{channel.mention}*** is now in lockdown"))
        else:
            pass


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await channel.send("Channel is no longer in lockdown")
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        cha = await get_log_channel(self, ctx)
        if cha == False:
            return cha.send(embed=discord.embed(title="Unlock", description=f"***{channel.mention}*** is no longer in lockdown"))
        else:
            pass


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        channel = await get_log_channel(self, ctx)
        if channel == False:
            return channel.send(embed=discord.embed(title="Message Clear", description=f"***{amount}*** messages have been cleared from ***{ctx.channel.name}***"))
        else:
            pass


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):
        embedVar = discord.Embed(description=message)
        msg = await ctx.channel.send(embed=embedVar)
        await msg.add_reaction(emoji)
        with open("react.json") as json_file:
            data = json.load(json_file)

            new_react_role = {
                "role_name": role.name,
                "role_id": role.id,
                "emoji": emoji,
                "message_id": msg.id,
            }

            data.append(new_react_role)

        with open("react.json", "w") as f:
            json.dump(data, f, indent=4)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def make_channel(self, ctx, *, name):
        guild = ctx.guild
        channel = await guild.create_text_channel(name)
        channel = await get_log_channel(self, ctx)
        if channel == False:
            return channel.send(embed=discord.embed(title="Create Channel", description=f"***{name}*** text channel has been created"))
        else:
            pass


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def make_vc(self, ctx, limit=None, *, name):
        guild = ctx.guild
        if limit == "None":
            channel = await guild.create_voice_channel(name)
        else:
            channel = await guild.create_voice_channel(name, user_limit=limit)
            channel = await get_log_channel(self, ctx)
        if channel == False:
            return channel.send(embed=discord.embed(title="Create Voice Channel", description=f"***{name}*** voice channel has been created"))
        else:
            pass


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member.id in [ctx.author.id, self.client.user.id]:
            return await ctx.send("You cant warn yourself/me LMAO")

        now = datetime.now()

        time = now.strftime("%Y-%m-%d %H:%M:%S")
        id_ = member.id
        if reason == None:
            reason = "None"

        os.chdir(dbpath)
        conn = sqlite3.connect(f"warn{ctx.guild.id}.db")
        c = conn.cursor()
        with conn:
            c.execute(
                "CREATE TABLE IF NOT EXISTS Warnings (id INTEGER, reason TEXT, time TEXT)")
            c.execute("INSERT INTO Warnings (id, reason, time) VALUES (:id, :reason, :time)", {
                      'id': id_, 'reason': reason, 'time': time})
        os.chdir(cd)
        channel = await get_log_channel(self, ctx)
        if channel == False:
            return channel.send(embed=discord.embed(title="Warn", description=f"***{member.mention}*** has been warned"))
        else:
            pass


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warnings(self, ctx, member: discord.Member):
        os.chdir(dbpath)
        conn = sqlite3.connect(f"warn{ctx.guild.id}.db")
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS Warnings (id INTEGER, reason TEXT, time TEXT)")
        c.execute("SELECT * FROM Warnings WHERE id = :id", {'id': member.id})
        warnings = c.fetchall()
        os.chdir(cd)

        em = discord.Embed(title="WARNINGS:")
        for i in warnings:
            t = i[2]
            r = i[1]
            em.add_field(name=t, value=f"Reason: {r}")

        await ctx.send(embed=em)
        channel = await get_log_channel(self, ctx)
        if channel == False:
            return channel.send(embed=discord.embed(title="", description=""))
        else:
            pass


def setup(client):
    client.add_cog(Moderation(client))
