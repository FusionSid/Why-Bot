import discord
from utils import plugin_enabled
import datetime as datetim
from datetime import datetime
from discord.ext import commands
import dotenv
from utils import get_log_channel
import humanfriendly

dotenv.load_dotenv()

async def create_voice(guild, name, cat, limit=None):
    category = await guild.get_category_by_name(guild, cat)
    await guild.create_voice_channel(name, category=category, user_limit=limit)


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rp'],help="This command is very useful. It lets you report bugs, messages and members. You need to /set Mod/Log channel for the member/message reports to work but bug reports will be sent to me.", extras={"category":"Moderation"}, usage="report [message/member/bug]", description="Report member/message to your server mods and report bugs to me")
    @commands.check(plugin_enabled)
    async def report(self, ctx, type_: str):
        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author

        channel = await get_log_channel(self.client, ctx.guild)
        if channel is None and type_.lower() != "bug":
            return await ctx.send("You dont have a log channel set on your server")

        em = discord.Embed(title="REPORT", color=ctx.author.color)
        em.timestamp = datetime.utcnow()

        if type_.lower() == "member":

            await ctx.send("Enter the @ of the member")
            member = await self.client.wait_for("message", timeout=300, check=wfcheck)
            member = member.content
            await ctx.send("Please give a short description about why you are reporting this person")
            reason = await self.client.wait_for("message", check=wfcheck, timeout=300)
            reporter = reason.author
            reason = reason.content
            em.description = "Member Report"
            em.add_field(name="Member:", value=member)
            em.add_field(name="Reason:", value=reason)
            em.add_field(name="Report By:", value=reporter)
            await channel.send(embed=em)

        elif type_.lower() == "message":

            await ctx.send("Enter the id of the message")
            messageid = await self.client.wait_for("message", check=wfcheck, timeout=300)
            messageid = messageid.content

            try:
                int(messageid)
            except Exception:
                return

            await ctx.send("Please give a short description about why you are reporting this message")
            reason = await self.client.wait_for("message", check=wfcheck, timeout=300)
            reporter = reason.author
            reason = reason.content

            message = await ctx.channel.fetch_message(messageid)
            messagecontent = message.content
            messageauthor = message.author

            em.description = "Message Report"
            em.add_field(name="Reason:", value=reason, inline=False)
            em.add_field(name="Message Content:",
                         value=messagecontent, inline=False)
            em.add_field(name="Message Author:",
                         value=messageauthor, inline=False)
            em.add_field(name="Report By:", value=reporter, inline=False)

            await channel.send(embed=em)

        elif type_.lower() == "bug":

            await ctx.send("Please give a short description about the issure/bug")
            reason = await self.client.wait_for("message", check=wfcheck, timeout=300)
            reporter = reason.author
            reason = reason.content
            em.description = "Bug Report"
            em.add_field(name="Reason", value=reason)
            em.add_field(name="Report By:", value=reporter)

            cha = await self.client.fetch_channel(940469380054126633)
            await cha.send(content=ctx.author.id, embed=em) 

    @commands.command(usage = "bug [bug]", description = "Report a bug", help = "This command lets you report a bug to the Why bot dev/s", extras={"category": "Moderation"})
    @commands.check(plugin_enabled)
    async def bug(self, ctx, *, bug):
        em = discord.Embed(title="REPORT", color=ctx.author.color)
        em.timestamp = datetime.utcnow()
        em.description = "Bug Report"
        em.add_field(name="Bug", value=bug)
        em.add_field(name="Report By:", value=ctx.author.name)

        cha = await self.client.fetch_channel(940469380054126633)
        await cha.send(content=ctx.author.id, embed=em)

    
    @commands.command(help="This command is used to ban a member", extras={"category":"Moderation"}, usage="ban [@user]", description="Ban a member")
    @commands.check(plugin_enabled)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason is not None:
                reason = f"{reason} - Requested by {ctx.author.name} ({ctx.author.id})"
            await member.ban(reason="".join(reason if reason != None else f"Requested by {ctx.author} ({ctx.author.id})"))
            await ctx.send(f"Banned {member} successfully.")
        else:
            await ctx.reply("Sorry, you cannot perform that action due to role hierarchy")
        channel = await get_log_channel(self.client, ctx.guild)
        if channel != None:
            return await channel.send(embed=discord.Embed(title="Ban", description=f"***{member.mention}*** has been banned", color=ctx.author.color))
        await ctx.send(f"User {member} has been banned")

    @commands.command(help="This command is used to kick a member", extras={"category":"Moderation"}, usage="kick [@user]", description="Kick a member")
    @commands.check(plugin_enabled)
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role.position > member.top_role.position:
            if reason is not None:
                reason = f"{reason} - Requested by {ctx.author.name} ({ctx.author.id})"
            await member.kick(reason="".join(reason if reason != None else f"Requested by {ctx.author} ({ctx.author.id})"))
            await ctx.send(f"Kicked {member} successfully.")
        else:
            await ctx.reply("Sorry, you cannot perform that action due to role hierarchy")
        channel = await get_log_channel(self.client, ctx.guild)
        if channel != None:
            return await channel.send(embed=discord.Embed(title="Kick", description=f"***{member.mention}*** has been kicked", color=ctx.author.color))
        await ctx.send(f"User {member} has been kicked")

    @commands.command(aliases=['lock'], help="This command is used to put a discord text channel into lockdown", extras={"category":"Moderation"}, usage="lockdown [#channel]", description="Lockdown a channel")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await channel.send("Channel is now in lockdown")
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        cha = await get_log_channel(self, ctx)
        if cha == None:
            return await cha.send(embed=discord.Embed(title="Lockdown", description=f"***{channel.mention}*** is now in lockdown"))

    @commands.command(help="This command is the unlocks a discord text channel from lockdown", extras={"category":"Moderation"}, usage="unlock [#channel]", description="Unlock a channel")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await channel.send("Channel is no longer in lockdown")
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        cha = await get_log_channel(self, ctx)
        if cha == None:
            return await cha.send(embed=discord.Embed(title="Unlock", description=f"***{channel.mention}*** is no longer in lockdown", color=ctx.author.color))

    @commands.command(help="This command deletes a certain amount of message from a channel. Limit it 50 messages", extras={"category":"Moderation"}, usage="clear [amount]", description="Delete messages")
    @commands.check(plugin_enabled)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def clear(self, ctx, amount: int = 10):
        if amount > 50:
            amount = 50
            await ctx.channel.purge(limit=amount+1)
        else:
            await ctx.channel.purge(limit=amount+1)
        channel = await get_log_channel(self.client, ctx.guild)
        if channel != None:
            return await channel.send(embed=discord.Embed(title="Message Clear", description=f"***{amount}*** messages have been cleared from ***{ctx.channel.name}***"))

    

    @commands.command(help="This command creates a discord Text Channel", extras={"category":"Moderation"}, usage="make_channel [name]", description="Create a text channel")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def make_channel(self, ctx, *, name):
        guild = ctx.guild
        channel = await guild.create_text_channel(name)
        channel = await get_log_channel(self.client, ctx.guild)
        if channel != None:
            return await channel.send(embed=discord.Embed(title="Create Channel", description=f"***{name}*** text channel has been created", color=ctx.author.color))

    @commands.command(help="This command creates a discord Voice Channel", extras={"category":"Moderation"}, usage="make_vc [limit(If none change to None)] [name]", description="Create a VC")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def make_vc(self, ctx, limit=None, *, name):
        guild = ctx.guild
        if limit == "None":
            channel = await guild.create_voice_channel(name)
        else:
            channel = await guild.create_voice_channel(name, user_limit=limit)
            channel = await get_log_channel(self.client, ctx.guild)
        if channel != None:
            return await channel.send(embed=discord.Embed(title="Create Voice Channel", description=f"***{name}*** voice channel has been created", color=ctx.author.color))

   
    @commands.command(aliases=['nick'],help="This command is used to change the nick of a user", extras={"category":"Moderation"}, usage="nick [@user] [nickname]", description="Change a users nick")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_nicknames=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nickname(self, ctx, member: discord.Member, *, nickname: str = "no nick"):
        if ctx.author.top_role.position > member.top_role.position:
            await member.edit(nick=nickname)
        else:
            await ctx.reply("Sorry, you cannot perform that action due to role hierarchy")

    @commands.command(help="This command is used to unban a user who is banned from the guild.", extras={"category":"Moderation"}, usage="unban [member id]", description="Unban a banned member")
    @commands.check(plugin_enabled)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unban(self, ctx, memberid: int = None):
        member = discord.Object(id=memberid)
        try:
            await ctx.guild.unban(member)
        except Exception:
            await ctx.send("Sorry, a user with that id was not found or isn't a previously banned member.")

    @commands.command(help="This command is used to put the discord channel youre in into slow mode", extras={"category":"Moderation"}, usage="slowmode [seconds]", description="Set channel to slowmode")
    @commands.check(plugin_enabled)
    async def slowmode(self, ctx, seconds: int = 5):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

    @commands.command(help="This command is used to put a channel thats in slowmode no longer into slowmode", extras={"category":"Moderation"}, usage="rslowmode", description="Removes slowmode from a channel")
    @commands.check(plugin_enabled)
    async def rslowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send('removed slowmode for the channel')

    @commands.command(name="pin", help="Pins the message with the specified ID to the current channel",extras={"category":"Moderation"}, usage="pin [message id]", description="Pin a message")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_messages=True)
    async def pin(self, ctx, _id: int):
        message = await ctx.channel.fetch_message(_id)
        await message.pin()
        await ctx.send("Successfully pinned that msg")

    @commands.command(name="unpin", help="Unpins the message with the specified ID from the current channel", extras={"category":"Moderation"}, usage="unpin [id]", description="Unpins a message")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_messages=True)
    async def unpin(self, ctx, _id: int):
        pinned_messages = await ctx.channel.pins()
        message = discord.utils.get(pinned_messages, id=_id)
        await message.unpin()
        await ctx.send("Successfully unpinned that msg")

    @commands.command(name="removereactions", help="Clear reactions from a message in the current channel", extras={"category":"Moderation"}, usage="removereactions [message id]", description="Removes reactions from a message")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_messages=True)
    async def removereactions(self, ctx, _id: int):
        message = await ctx.channel.fetch_message(_id)
        await message.clear_reactions()
        await ctx.send("Removed")


    @commands.command(aliases=["mute"])
    @commands.has_guild_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, time, *, reason=None):
        if reason is None:
            reason = "No reason"
        time = humanfriendly.parse_timespan(time)
        await member.timeout(until=discord.utils.utcnow() + datetim.timedelta(seconds=time), reason=reason)
        channel = await get_log_channel(self.client, ctx.guild)
        if channel != None:
            return await channel.send(embed=discord.Embed(title="Timeout", description=f"***{member.mention}*** has been muted", color=ctx.author.color))
        await ctx.send(embed=discord.Embed(
            title= "Timeout",
            description=f"{member.mention} has been muted for {time} seconds.\nReason: {reason}",
            color = ctx.author.color))


def setup(client):
    client.add_cog(Moderation(client))
