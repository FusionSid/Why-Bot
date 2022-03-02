import discord
from discord.ext import commands
from utils import plugin_enabled, get_log_channel, kwarg_to_embed
import datetime
import json

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['grole'], help="This command is used to give a role to a user.", extras={"category":"Moderation"}, usage="giverole [@role] [@member]", description="Give role to a member")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def giverole(self, ctx, role: discord.Role, user: discord.Member):
        await user.add_roles(role)
        channel = await get_log_channel(self, ctx)
        if channel != None:
            return await channel.send(embed=discord.Embed(title="Give Role", description=f"***{user.mention}*** has been given the ***{role.mention}*** role", color=ctx.author.color))
        await ctx.send(f"{user} has been given the {role} role")

    @commands.command(aliases=['trole'], help="This commmand is used to remove a role from a member", extras={"category":"Moderation"}, usage="takerole [@role] [@member]", description="Remove roles form member")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def takerole(self, ctx, role: discord.Role, user: discord.Member):
        await user.remove_roles(role)
        channel = await get_log_channel(self, ctx)
        if channel != None:
            return await channel.send(embed=discord.Embed(title="Remove Role", description=f"***{role.mention}*** has been removed from ***{user.mention}***", color=ctx.author.color))
        await ctx.send(f"{role} has been removed from {user}")

    @commands.command(help="This command creates a simple react role that users can react to to get a role. ", extras={"category":"Moderation"}, usage="reactrole [:emoji:] [@role] [message text]", description="Creates a reactrole")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):
        if message.startswith("--embed"):
            kwargs = message.replace("--embed ", "")
            data = await kwarg_to_embed(self.client, ctx, kwargs)
            em = data[0]
        else:
            em = discord.Embed(description=message, color=ctx.author.color)
            em.timestamp = datetime.datetime.utcnow()

        msg = await ctx.channel.send(embed=em)
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
    
    @commands.command(aliases=['sar'],help="This command is used to set the autorole for your server. It has 2 types: all and bot\nThe all type sets the autorole for all members who join the server and the bot type sets the autorole for all bots that join the server.", extras={"category":"Moderation"}, usage="autorole [all/bot] [@role]", description="Sets the autorole role for the server")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role_type: str, roles: commands.Greedy[discord.Role]):
        data = await self.client.get_db()
        for role in roles: 
            if role_type.lower() == 'all':
                if role.id in data[str(ctx.guild.id)]['autorole']['all']:
                    roles.remove(role)
                    continue
                data[str(ctx.guild.id)]['autorole']['all'].append(role.id)
            elif role_type.lower() == 'bot':
                if role.id in data[str(ctx.guild.id)]['autorole']['bot']:
                    roles.remove(role)
                    continue
                data[str(ctx.guild.id)]['autorole']['bot'].append(role.id)
            else:
                return await ctx.send(f"{ctx.prefix}autorole [all/bot] @role\nYou must specify if roles if for all or for bots")
        await self.client.update_db(data)
        if len (roles) == 0:
            return
        await ctx.send(f"{[role.mention for role in roles]} set as autorole for this server")

    
    #remove react role commands:
    @commands.command(aliases=['rar'], help="This command is used to remove the autorole for your server. It has 2 types: all and bot\nThe all type sets the autorole for all members who join the server and the bot type sets the autorole for all bots that join the server.", extras={"category":"Moderation"}, usage="remove_autorole [all/bot] [@role]", description="Sets the autorole role for the server")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def remove_autorole(self, ctx, role : discord.Role):
        data = await self.client.get_db()

        return

        await self.client.update_db(data)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = await self.client.get_db()
        if data[str(member.guild.id)]['settings']['plugins']['Moderation'] == False:
            return
        await self.client.update_db(data)

        if member.bot:
            if len(data[str(member.guild.id)]['autorole']['bot']) != 0:
                for role in data[str(member.guild.id)]['autorole']['bot']:
                    try:
                        role = member.guild.get_role(role)
                        await member.add_roles(role)
                    except Exception as e:
                        continue
            return

        if len(data[str(member.guild.id)]['autorole']['all']) != 0:
            for role in data[str(member.guild.id)]['autorole']['all']:
                try:
                    role = member.guild.get_role(role)
                    await member.add_roles(role)
                except:
                    return

        
        
    
            
def setup(client):
    client.add_cog(Roles(client))