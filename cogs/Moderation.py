import discord
from datetime import datetime
from discord.ui import Button, View
from discord import Option
from discord.ext import commands
import os
import json
import dotenv

dotenv.load_dotenv()


async def create_voice(guild, name, cat, limit=None):
    category = await guild.get_category_by_name(guild, cat)
    await guild.create_voice_channel(name, category=category, user_limit=limit)


async def get_log_channel(self, ctx):
    with open("./database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == ctx.guild.id:
            channel = i['log_channel']
            return await self.client.fetch_channel(channel)

    return False


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rp'])
    async def report(self, ctx, type_: str):
        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author

        channel = await get_log_channel(self, ctx)

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
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Give Role", description=f"***{user.mention}*** has been given the ***{role.mention}*** role"))
        else:
            pass
        await ctx.send(f"{user} has been given the {role} role")


    @commands.command(aliases=['trole'])
    @commands.has_permissions(administrator=True)
    async def takerole(self, ctx, role: discord.Role, user: discord.Member):
        await user.remove_roles(role)
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Remove Role", description=f"***{role.mention}*** has been removed from ***{user.mention}***"))
        else:
            pass
        await ctx.send(f"{role} has been removed from {user}")


    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def ban(self,ctx,member:discord.Member,*,reason=None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason is not None:
                reason = f"{reason} - Requested by {ctx.author.name} ({ctx.author.id})"
            await member.ban(reason="".join(reason if reason != None else f"Requested by {ctx.author} ({ctx.author.id})"))
            await ctx.send(f"Banned {member} successfully.")
        else:
            await ctx.reply("Sorry, you cannot perform that action due to role hierarchy")
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Ban", description=f"***{member.mention}*** has been banned"))
        else:
            pass
        await ctx.send(f"User {member} has been banned")


    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def kick(self,ctx,member:discord.Member,*,reason=None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason is not None:
                reason = f"{reason} - Requested by {ctx.author.name} ({ctx.author.id})"
            await member.kick(reason="".join(reason if reason != None else f"Requested by {ctx.author} ({ctx.author.id})"))
            await ctx.send(f"Kicked {member} successfully.")
        else:
            await ctx.reply("Sorry, you cannot perform that action due to role hierarchy")
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Kick", description=f"***{member.mention}*** has been kicked"))
        else:
            pass
        await ctx.send(f"User {member} has been kicked")


    @commands.command(aliases=['lock'])
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await channel.send("Channel is now in lockdown")
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        cha = await get_log_channel(self, ctx)
        if cha == False:
            return await cha.send(embed=discord.Embed(title="Lockdown", description=f"***{channel.mention}*** is now in lockdown"))
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
            return await cha.send(embed=discord.Embed(title="Unlock", description=f"***{channel.mention}*** is no longer in lockdown"))
        else:
            pass


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Message Clear", description=f"***{amount}*** messages have been cleared from ***{ctx.channel.name}***"))
        else:
            pass


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):
        embedVar = discord.Embed(description=message)
        msg = await ctx.channel.send(embed=embedVar)
        await msg.add_reaction(emoji)
        with open("./database/react.json") as json_file:
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
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Create Channel", description=f"***{name}*** text channel has been created"))
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
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Create Voice Channel", description=f"***{name}*** voice channel has been created"))
        else:
            pass


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member.id in [ctx.author.id, self.client.user.id]:
            return await ctx.send("You cant warn yourself/me LMAO")

        now = datetime.now()

        time = now.strftime("%Y-%m-%d %H:%M:%S")
        if reason == None:
            reason = "None"

        with open("./database/db.json") as f:
            data = json.load(f)
        
        for i in data:
            if i["guild_id"] == ctx.guild.id:
                warn = {'time':time, 'reason':reason}
                try:
                    i['warnings'][f"{member.id}"].append(warn)
                except:
                    i['warnings'][f"{member.id}"] = []
                    i['warnings'][f"{member.id}"].append(warn)

        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Warn", description=f"***{member.mention}*** has been warned"))
        else:
            pass


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warnings(self, ctx, member: discord.Member):
        with open("./database/db.json") as f:
            data = json.load(f)
        for i in data:
            if i["guild_id"] == ctx.guild.id:
                warns = i['warnings']
        try:
            warnings = warns[f'{member.id}']
        except:
            return await ctx.send("This person has no warnings")

        em = discord.Embed(title="WARNINGS:")
        for i in warnings:
            t = i["time"]
            r = i["reason"]
            em.add_field(name=t, value=f"Reason: {r}")

        await ctx.send(embed=em)


    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def nickname(self, ctx, member: discord.Member, *, nickname: str = "no nick"):
        if ctx.author.top_role.position > member.top_role.position:
            await member.edit(nick=nickname)
        else:
            await ctx.reply("Sorry, you cannot perform that action due to role hierarchy")

    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def unban(self,ctx,memberid:int=None):
        member = discord.Object(id=memberid) 
        try:
            await ctx.guild.unban(member)
        except:
            await ctx.send("Sorry, a user with that id was not found or isn't a previously banned member.")


    @commands.group()
    async def slowmode(self,ctx, seconds: int=5):   
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

    @commands.command()
    async def rslowmode(self,ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send('removed slowmode for the channel')


    @commands.command(name="pin",help="Pins the message with the specified ID to the current channel")
    @commands.has_permissions(manage_messages=True)
    async def pin(self, ctx, id:int):      
        message = await ctx.channel.fetch_message(id)
        await message.pin()
        await ctx.send("Successfully pinned that msg")


    @commands.command(name="unpin",help="Unpins the message with the specified ID from the current channel")
    @commands.has_permissions(manage_messages=True)
    async def unpin(self, ctx, id:int):
        pinned_messages = await ctx.channel.pins()
        message = discord.utils.get(pinned_messages, id=id)
        await message.unpin()
        await ctx.send("Successfully unpinned that msg")
        
        
    @commands.command(name="removereactions",help="Clear reactions from a message in the current channel")
    @commands.has_permissions(manage_messages=True)
    async def removereactions(self, ctx, id:int):
        message = await ctx.channel.fetch_message(id)
        await message.clear_reactions()
        await ctx.send("Removed")

    @commands.command()
    async def settings(self, ctx):
        pass


def setup(client):
    client.add_cog(Moderation(client))



    

    

