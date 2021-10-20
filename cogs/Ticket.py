import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import json
import asyncio
import os

cd = "home/runner/Why-Bot/cogs/"
homepath = "home/runner/Why-Bot/MainDB/"

class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def new(self, ctx, *, args = None):

        await self.client.wait_until_ready()

        if args == None:
            message_content = "Please wait, we will be with you shortly!"
        
        else:
            message_content = "".join(args)

        os.chdir(homepath)
        with open(f"ticket{ctx.guild.id}") as f:
            data = json.load(f)
        os.chdir(cd)

        ticket_number = int(data["ticket-counter"])
        ticket_number += 1

        ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ticket_number))
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

        for role_id in data["valid-roles"]:
            role = ctx.guild.get_role(role_id)

            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        
        await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

        em = discord.Embed(title="New ticket from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0x00a8ff)

        await ticket_channel.send(embed=em)

        pinged_msg_content = ""
        non_mentionable_roles = []

        if data["pinged-roles"] != []:

            for role_id in data["pinged-roles"]:
                role = ctx.guild.get_role(role_id)

                pinged_msg_content += role.mention
                pinged_msg_content += " "

                if role.mentionable:
                    pass
                else:
                    await role.edit(mentionable=True)
                    non_mentionable_roles.append(role)
            
            await ticket_channel.send(pinged_msg_content)

            for role in non_mentionable_roles:
                await role.edit(mentionable=False)
        
        data["ticket-channel-ids"].append(ticket_channel.id)

        data["ticket-counter"] = int(ticket_number)
        os.chdir(homepath)
        with open(f"ticket{ctx.guild.id}", 'w') as f:
            json.dump(data, f)
        os.chdir(cd)
        
        created_em = discord.Embed(title="Why Tickets", description="Your ticket has been created at {}".format(ticket_channel.mention), color=0x00a8ff)
        
        await ctx.send(embed=created_em)

    @commands.command()
    async def close(self, ctx):
        os.chdir(homepath)
        with open(f'ticket{ctx.guild.id}') as f:
            data = json.load(f)
        os.chdir(cd)

        if ctx.channel.id in data["ticket-channel-ids"]:

            channel_id = ctx.channel.id

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

            try:

                em = discord.Embed(title="Why Tickets", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)
            
                await ctx.send(embed=em)
                await self.client.wait_for('message', check=check, timeout=60)
                await ctx.channel.delete()

                index = data["ticket-channel-ids"].index(channel_id)
                del data["ticket-channel-ids"][index]

                os.chdir(homepath)
                with open(f'ticket{ctx.guild.id}', 'w') as f:
                    json.dump(data, f)
                os.chdir(cd)
            
            except asyncio.TimeoutError:
                em = discord.Embed(title="Why Tickets", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
                await ctx.send(embed=em)

            

    @commands.command()
    async def addaccess(self, ctx, role_id=None):
        os.chdir(homepath)
        with open(f'ticket{ctx.guild.id}') as f:
            data = json.load(f)
        os.chdir(cd)
        
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:
            role_id = int(role_id)

            if role_id not in data["valid-roles"]:

                try:
                    role = ctx.guild.get_role(role_id)

                    os.chdir(homepath)
                    with open(f"ticket{ctx.guild.id}") as f:
                        data = json.load(f)
                    os.chdir(cd)
                    data["valid-roles"].append(role_id)

                    os.chdir(homepath)
                    with open(f'ticket{ctx.guild.id}', 'w') as f:
                        json.dump(data, f)
                    os.chdir(cd)
                    
                    em = discord.Embed(title="Why Tickets", description="You have successfully added `{}` to the list of roles with access to tickets.".format(role.name), color=0x00a8ff)

                    await ctx.send(embed=em)

                except:
                    em = discord.Embed(title="Why Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                    await ctx.send(embed=em)
            
            else:
                em = discord.Embed(title="Why Tickets", description="That role already has access to tickets!", color=0x00a8ff)
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Why Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.send(embed=em)

    @commands.command()
    async def delaccess(self, ctx, role_id=None):
        os.chdir(homepath)
        with open(f'ticket{ctx.guild.id}') as f:
            data = json.load(f)
        os.chdir(cd)
        
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass

        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)
                os.chdir(homepath)
                with open(f"ticket{ctx.guild.id}") as f:
                    data = json.load(f)
                os.chdir(cd)

                valid_roles = data["valid-roles"]

                if role_id in valid_roles:
                    index = valid_roles.index(role_id)

                    del valid_roles[index]

                    data["valid-roles"] = valid_roles
                    os.chdir(homepath)
                    with open(f'ticket{ctx.guild.id}', 'w') as f:
                        json.dump(data, f)
                    os.chdir(cd)

                    em = discord.Embed(title="Why Tickets", description="You have successfully removed `{}` from the list of roles with access to tickets.".format(role.name), color=0x00a8ff)

                    await ctx.send(embed=em)
                
                else:
                    
                    em = discord.Embed(title="Why Tickets", description="That role already doesn't have access to tickets!", color=0x00a8ff)
                    await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Why Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Why Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.send(embed=em)

    @commands.command()
    async def addpingedrole(self, ctx, role_id=None):
        os.chdir(homepath)
        with open(f'ticket{ctx.guild.id}') as f:
            data = json.load(f)
        os.chdir(cd)
        
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:

            role_id = int(role_id)

            if role_id not in data["pinged-roles"]:

                try:
                    role = ctx.guild.get_role(role_id)
                    os.chdir(homepath)
                    with open(f"ticket{ctx.guild.id}") as f:
                        data = json.load(f)
                    os.chdir(cd)

                    data["pinged-roles"].append(role_id)
                    os.chdir(homepath)
                    with open(f'ticket{ctx.guild.id}', 'w') as f:
                        json.dump(data, f)
                    os.chdir(cd)

                    em = discord.Embed(title="Why Tickets", description="You have successfully added `{}` to the list of roles that get pinged when new tickets are created!".format(role.name), color=0x00a8ff)

                    await ctx.send(embed=em)

                except:
                    em = discord.Embed(title="Why Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                    await ctx.send(embed=em)
                
            else:
                em = discord.Embed(title="Why Tickets", description="That role already receives pings when tickets are created.", color=0x00a8ff)
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Why Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.send(embed=em)

    @commands.command()
    async def delpingedrole(self, ctx, role_id=None):
        os.chdir(homepath)
        with open(f'ticket{ctx.guild.id}') as f:
            data = json.load(f)
        os.chdir(cd)
        
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)
                os.chdir(homepath)
                with open(f"ticket{ctx.guild.id}") as f:
                    data = json.load(f)
                os.chdir(cd)

                pinged_roles = data["pinged-roles"]

                if role_id in pinged_roles:
                    index = pinged_roles.index(role_id)

                    del pinged_roles[index]

                    data["pinged-roles"] = pinged_roles
                    os.chdir(homepath)
                    with open(f'ticket{ctx.guild.id}', 'w') as f:
                        json.dump(data, f)
                    os.chdir(cd)

                    em = discord.Embed(title="Why Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0x00a8ff)
                    await ctx.send(embed=em)
                
                else:
                    em = discord.Embed(title="Why Tickets", description="That role already isn't getting pinged when new tickets are created!", color=0x00a8ff)
                    await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Why Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Why Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.send(embed=em)


    @commands.command()
    @has_permissions(administrator=True)
    async def addadminrole(self, ctx, role_id=None):

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)
            os.chdir(homepath)
            with open(f"ticket{ctx.guild.id}") as f:
                data = json.load(f)
            os.chdir(cd)

            data["verified-roles"].append(role_id)
            os.chdir(homepath)
            with open(f'ticket{ctx.guild.id}', 'w') as f:
                json.dump(data, f)
            os.chdir(cd)
            
            em = discord.Embed(title="Why Tickets", description="You have successfully added `{}` to the list of roles that can run admin-level commands!".format(role.name), color=0x00a8ff)
            await ctx.send(embed=em)

        except:
            em = discord.Embed(title="Why Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.send(embed=em)

    @commands.command()
    @has_permissions(administrator=True)
    async def deladminrole(self, ctx, role_id=None):
        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)
            os.chdir(homepath)
            with open(f"ticket{ctx.guild.id}") as f:
                data = json.load(f)
            os.chdir(cd)

            admin_roles = data["verified-roles"]

            if role_id in admin_roles:
                index = admin_roles.index(role_id)

                del admin_roles[index]

                data["verified-roles"] = admin_roles
                os.chdir(homepath)
                with open(f'ticket{ctx.guild.id}', 'w') as f:
                    json.dump(data, f)
                os.chdir(cd)
                
                em = discord.Embed(title="Why Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0x00a8ff)

                await ctx.send(embed=em)
            
            else:
                em = discord.Embed(title="Why Tickets", description="That role isn't getting pinged when new tickets are created!", color=0x00a8ff)
                await ctx.send(embed=em)

        except:
            em = discord.Embed(title="Why Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(Ticket(client))
