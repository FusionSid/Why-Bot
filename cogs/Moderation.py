import discord
from utils.checks import plugin_enabled
from datetime import datetime
from discord.ext import commands
import json
import dotenv
from discord_webhook import DiscordWebhook
from io import BytesIO
from urllib.request import urlopen
import requests
import asyncio
dotenv.load_dotenv()


async def create_voice(guild, name, cat, limit=None):
    category = await guild.get_category_by_name(guild, cat)
    await guild.create_voice_channel(name, category=category, user_limit=limit)


async def get_log_channel(self, ctx):
    with open("./database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == ctx.guild.id:
            if i['log_channel'] is None:
                return None
            channel = i['log_channel']
            return await self.client.fetch_channel(channel)

    return False

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rp'],help="This command is very useful. It lets you report bugs, messages and members. You need to /set Mod/Log channel for the member/message reports to work but bug reports will be sent to me.", extras={"category":"Moderation"}, usage="report [message/member/bug]", description="Report member/message to your server mods and report bugs to me")
    @commands.check(plugin_enabled)
    async def report(self, ctx, type_: str):
        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author

        channel = await get_log_channel(self, ctx)

        em = discord.Embed(title="REPORT", color=ctx.author.color)

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
            except:
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
            await cha.send(embed=em)

    @commands.command(aliases=['grole'], help="This command is used to give a role to a user.", extras={"category":"Moderation"}, usage="giverole [@role] [@member]", description="Give role to a member")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def giverole(self, ctx, role: discord.Role, user: discord.Member):
        await user.add_roles(role)
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Give Role", description=f"***{user.mention}*** has been given the ***{role.mention}*** role", color=ctx.author.color))
        else:
            pass
        await ctx.send(f"{user} has been given the {role} role")

    @commands.command(aliases=['trole'], help="This commmand is used to remove a role from a member", extras={"category":"Moderation"}, usage="takerole [@role] [@member]", description="Remove roles form member")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def takerole(self, ctx, role: discord.Role, user: discord.Member):
        await user.remove_roles(role)
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Remove Role", description=f"***{role.mention}*** has been removed from ***{user.mention}***", color=ctx.author.color))
        else:
            pass
        await ctx.send(f"{role} has been removed from {user}")

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
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Ban", description=f"***{member.mention}*** has been banned", color=ctx.author.color))
        else:
            pass
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
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Kick", description=f"***{member.mention}*** has been kicked", color=ctx.author.color))
        else:
            pass
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
        if cha == False:
            return await cha.send(embed=discord.Embed(title="Lockdown", description=f"***{channel.mention}*** is now in lockdown"))
        else:
            pass

    @commands.command(help="This command is the unlocks a discord text channel from lockdown", extras={"category":"Moderation"}, usage="unlock [#channel]", description="Unlock a channel")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await channel.send("Channel is no longer in lockdown")
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        cha = await get_log_channel(self, ctx)
        if cha == False:
            return await cha.send(embed=discord.Embed(title="Unlock", description=f"***{channel.mention}*** is no longer in lockdown", color=ctx.author.color))
        else:
            pass

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
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Message Clear", description=f"***{amount}*** messages have been cleared from ***{ctx.channel.name}***"))
        else:
            pass

    @commands.command(help="This command creates a simple react role that users can react to to get a role. ", extras={"category":"Moderation"}, usage="reactrole [:emoji:] [@role] [message text]", description="Creates a reactrole")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):
        embedVar = discord.Embed(description=message, color=ctx.author.color)
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

        with open("./database/react.json", "w") as f:
            json.dump(data, f, indent=4)

    @commands.Cog.listener()
    @commands.check(plugin_enabled)
    async def on_raw_reaction_add(self, payload):
        if not payload.guild_id:
          return
        if payload.member.bot:
            return
        with open("./database/react.json") as f:
            data = json.load(f)
        for x in data:
            if x['emoji'] == payload.emoji.name and x["message_id"] == payload.message_id:
                guild = await self.client.fetch_guild(payload.guild_id)
                role = guild.get_role(x['role_id'])
                await payload.member.add_roles(role)
            else:
                pass
    
    @commands.Cog.listener()
    @commands.check(plugin_enabled)
    async def on_raw_reaction_remove(self, payload):
        if not payload.guild_id:
          return
        with open("./database/react.json") as f:
            data = json.load(f)
        for x in data:
            if x['emoji'] == payload.emoji.name and x["message_id"] == payload.message_id:
                guild = await self.client.fetch_guild(payload.guild_id)
                role = guild.get_role(x['role_id'])
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)
            else:
                pass

    @commands.command(help="This command creates a discord Text Channel", extras={"category":"Moderation"}, usage="make_channel [name]", description="Create a text channel")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def make_channel(self, ctx, *, name):
        guild = ctx.guild
        channel = await guild.create_text_channel(name)
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Create Channel", description=f"***{name}*** text channel has been created", color=ctx.author.color))
        else:
            pass

    @commands.command(help="This command creates a discord Voice Channel", extras={"category":"Moderation"}, usage="make_vc [limit(If none change to None)] [name]", description="Create a VC")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def make_vc(self, ctx, limit=None, *, name):
        guild = ctx.guild
        if limit == "None":
            channel = await guild.create_voice_channel(name)
        else:
            channel = await guild.create_voice_channel(name, user_limit=limit)
            channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Create Voice Channel", description=f"***{name}*** voice channel has been created", color=ctx.author.color))
        else:
            pass

    @commands.command(help="This command is used to warn a user\nThe warning gets added and you can use the warnings command to check the users warnings", extras={"category":"Moderation"}, usage="warn [@user] [reason]", description="Warns a user")
    @commands.check(plugin_enabled)
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
                warn = {'time': time, 'reason': reason}
                try:
                    i['warnings'][f"{member.id}"].append(warn)
                except:
                    i['warnings'][f"{member.id}"] = []
                    i['warnings'][f"{member.id}"].append(warn)

        with open("./database/db.json",'w') as f:
          json.dump(data,f,indent=4)
        channel = await get_log_channel(self, ctx)
        if channel != False:
            return await channel.send(embed=discord.Embed(title="Warn", description=f"***{member.mention}*** has been warned", color=ctx.author.color))
        else:
            pass

    @commands.command(help="This commands shows all the warnings that a user has", extras={"category":"Moderation"}, usage="warnings [@user]", description="Displays a users warnings")
    @commands.check(plugin_enabled)
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

        em = discord.Embed(title="WARNINGS:", color=ctx.author.color)
        for i in warnings:
            t = i["time"]
            r = i["reason"]
            em.add_field(name=t, value=f"Reason: {r}")

        await ctx.send(embed=em)

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
        except:
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
    async def pin(self, ctx, id: int):
        message = await ctx.channel.fetch_message(id)
        await message.pin()
        await ctx.send("Successfully pinned that msg")

    @commands.command(name="unpin", help="Unpins the message with the specified ID from the current channel", extras={"category":"Moderation"}, usage="unpin [id]", description="Unpins a message")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_messages=True)
    async def unpin(self, ctx, id: int):
        pinned_messages = await ctx.channel.pins()
        message = discord.utils.get(pinned_messages, id=id)
        await message.unpin()
        await ctx.send("Successfully unpinned that msg")

    @commands.command(name="removereactions", help="Clear reactions from a message in the current channel", extras={"category":"Moderation"}, usage="removereactions [message id]", description="Removes reactions from a message")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_messages=True)
    async def removereactions(self, ctx, id: int):
        message = await ctx.channel.fetch_message(id)
        await message.clear_reactions()
        await ctx.send("Removed")

    @commands.command(help="This command is used to set the autorole for your server. It has 2 types: all and bot\nThe all type sets the autorole for all members who join the server and the bot type sets the autorole for all bots that join the server.", extras={"category":"Moderation"}, usage="autorole [@role] [all/bot]", description="Sets the autorole role for the server")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role, type: str):
        with open("./database/db.json") as f:
            data = json.load(f)
        for i in data:
            if i["guild_id"] == ctx.guild.id:
                if type.lower() == 'all':
                    i['autorole']['all'] = role.id
                elif type.lower() == 'bot':
                    i['autorole']['bot'] = role.id
                else:
                    return await ctx.send(f"{ctx.prefix}autorole @role [all/bot]\nYou must specify if roles if for all or for bots")
        with open('./database/db.json', 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"{role.mention} set as autorole for this server")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("./database/db.json") as f:
          data = json.load(f)
        for i in data:
          if i["guild_id"] == member.guild.id:
            if i['settings']['plugins']['Moderation'] == False:
              return
            else:
              pass
        with open("./database/db.json") as f:
            data = json.load(f)
        role = False
        for i in data:
            if i["guild_id"] == member.guild.id:
                if not member.bot:
                    role = i['autorole']['all']
                else:
                    role = i['autorole']['bot']
        if role == False:
            return
        elif role == None:
            return
        else:
            role = member.guild.get_role(role)
            await member.add_roles(role)

    @commands.command(aliases=["createwebhook", 'cwh'], help="This command is used to create a webhook.\nA webhook is sorta like a bot.Once the webhook is made it will be asigned to your name and whenever you type the id that you specify the webhook will send the message what you want.\nWebhooks only work in one channel at a time so if you want to use a webhook in another channel you will need to make another webhook", extras={"category":"Moderation"}, usage="createhook [name] [channel(optional)]", description="Creates a webhook")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_webhooks=True)
    async def createhook(self, ctx, name, channel:discord.TextChannel=None,):
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        if channel == None:
            channel = ctx.channel
        await ctx.send("Enter the url for the image you want to use as the profile pic (or type none for default)")
        avatarurl = await self.client.wait_for("message", timeout=300, check=check)
        avatarurl = avatarurl.content
        if avatarurl.lower() == "none":
            e = await channel.create_webhook(name=name,reason=None)
        else:
            aimg = requests.get(avatarurl)
            aimg = aimg.content
            e = await channel.create_webhook(name=name, avatar=bytes(aimg), reason=None)
        webhook = await self.client.fetch_webhook(e.id)
        await ctx.send(f"Enter the id for the bot (What youll use in the `{ctx.prefix}webhook` command)")
        id = await self.client.wait_for("message", timeout=300, check=check)
        id = id.content
        with open("./database/userdb.json") as f:
          data = json.load(f)
        for i in data:
          if i['user_id'] == ctx.author.id:
            i['webhooks'][id] = webhook.url
        with open('./database/userdb.json', 'w') as f:
          json.dump(data, f, indent=4)
        await ctx.message.delete()
        await ctx.send(embed=discord.Embed(title="Webhook Created", description=f"Use `{ctx.prefix}webhook {id} [message]` to send messages using that webhook", color=ctx.author.color))

    @commands.command(aliases=['webhook', 'swh'],help="This command uses a webhook that you previously made using the createhook command to send a message", extras={"category":"Moderation"}, usage="webhook [id] [text]", description="Send message through a webhook")
    @commands.check(plugin_enabled)
    async def wh(self, ctx, id, *, text):
        with open("./database/userdb.json") as f:
          data = json.load(f)
        found = False
        for i in data:
          if i['user_id'] == ctx.author.id:
            try:
              url = i['webhooks'][id]
            except:
              pass
            found = True
        if found == False:
          return await ctx.send("Id not found")
        await ctx.message.delete()
        webhook = DiscordWebhook(url=url, content=text)
        response = webhook.execute()



def setup(client):
    client.add_cog(Moderation(client))
