import discord
from utils.checks import plugin_enabled
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import json
import datetime
import asyncio

homepath = "./database/tickets/"
newtickettemplate = {"ticket-counter": 0, "valid-roles": [],
                     "pinged-roles": [], "ticket-channel-ids": [], "verified-roles": []}


def createticketfile(ctx):
    try:
        with open(f"./database/tickets/{ctx.guild.id}.json") as f:
            print("Success")
    except FileNotFoundError:
        with open(f"./database/tickets/{ctx.guild.id}.json", 'w') as f:
            json.dump(newtickettemplate, f, indent=4)


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['new'], help="This command is use to create a new ticket.", extras={"category":"Ticket"}, usage="newticket", description="Creates a ticket")
    @commands.check(plugin_enabled)
    async def newticket(self, ctx, *, args=None):
        createticketfile(ctx)

        await self.client.wait_until_ready()

        if args == None:
            message_content = f"Please wait, we will be with you shortly!\nUse {ctx.prefix}closeticket to close the ticket"

        else:
            message_content = "Please wait, we will be with you shortly!\nYour Message: {}\nUse {ctx.prefix}closeticket to close the ticket".format(
                args, ctx.prefix)

        with open(f"./database/tickets/ticket{ctx.guild.id}.json") as f:
            data = json.load(f)

        ticket_number = int(data["ticket-counter"])
        ticket_number += 1

        ticket_channel = await ctx.guild.create_text_channel("{}'s Ticket'".format(ctx.author.name))
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

        for role_id in data["valid-roles"]:
            role = ctx.guild.get_role(role_id)

            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

        await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

        em = discord.Embed(title="New ticket from {}#{}".format(
            ctx.author.name, ctx.author.discriminator), description="{}".format(message_content), color=0x00a8ff)
        em.timestamp = datetime.datetime.utcnow()
        
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
        with open(f"./database/tickets/ticket{ctx.guild.id}.json", 'w') as f:
            json.dump(data, f, indent=4)

        created_em = discord.Embed(title="Why Tickets", description="Your ticket has been created at {}".format(
            ticket_channel.mention), color=0x00a8ff)
        created_em.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=created_em)

    @commands.command(aliases=['close'], help="This command is used to close a ticket", extras={"category":"Ticket"}, usage="closeticket", description="Close a ticket")
    @commands.check(plugin_enabled)
    async def closeticket(self, ctx):
        createticketfile(ctx)
        with open(f'./database/tickets/ticket{ctx.guild.id}.json') as f:
            data = json.load(f)

        if ctx.channel.id in data["ticket-channel-ids"]:

            channel_id = ctx.channel.id

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

            try:

                em = discord.Embed(
                    title="Why Tickets", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)
                em.timestamp = datetime.datetime.utcnow()

                await ctx.send(embed=em)
                await self.client.wait_for('message', check=check, timeout=60)
                await ctx.channel.delete()

                index = data["ticket-channel-ids"].index(channel_id)
                del data["ticket-channel-ids"][index]

                with open(f'./database/tickets/ticket{ctx.guild.id}.json', 'w') as f:
                    json.dump(data, f, indent=4)

            except asyncio.TimeoutError:
                em = discord.Embed(
                    title="Why Tickets", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em)

    @commands.command(help="This command is used to add access to a role for the tickets.\nWhen a new ticket is creates theses roles will have access to that ticket.", extras={"category":"Ticket"}, usage="addaccess [roleid]", description="Gives a role access to tickets")
    @commands.check(plugin_enabled)
    async def addaccess(self, ctx, role_id=None):
        createticketfile(ctx)
        with open(f'./database/tickets/ticket{ctx.guild.id}.json') as f:
            data = json.load(f)

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

                    with open(f"./database/tickets/ticket{ctx.guild.id}.json") as f:
                        data = json.load(f)
                    data["valid-roles"].append(role_id)

                    with open(f'./database/tickets/ticket{ctx.guild.id}.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    em = discord.Embed(title="Why Tickets", description="You have successfully added `{}` to the list of roles with access to tickets.".format(
                        role.name), color=0x00a8ff)
                    em.timestamp = datetime.datetime.utcnow()

                    await ctx.send(embed=em)

                except:
                    em = discord.Embed(
                        title="Why Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                    em.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed=em)

            else:
                em = discord.Embed(
                    title="Why Tickets", description="That role already has access to tickets!", color=0x00a8ff)
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em)

        else:
            em = discord.Embed(
                title="Why Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

    @commands.command(help="This command removes a role from accessing the tickets", extras={"category":"Ticket"}, usage="delaccess [roleid]", description="Removes a role from accessing tickets")
    @commands.check(plugin_enabled)
    async def delaccess(self, ctx, role_id=None):
        createticketfile(ctx)
        with open(f'./database/tickets/ticket{ctx.guild.id}.json') as f:
            data = json.load(f)

        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except Exception as e:
                pass

        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)
                with open(f"./database/tickets/{ctx.guild.id}.json") as f:
                    data = json.load(f)

                valid_roles = data["valid-roles"]

                if role_id in valid_roles:
                    index = valid_roles.index(role_id)

                    del valid_roles[index]

                    data["valid-roles"] = valid_roles
                    with open(f'./database/tickets/ticket{ctx.guild.id}.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    em = discord.Embed(title="Why Tickets", description="You have successfully removed `{}` from the list of roles with access to tickets.".format(
                        role.name), color=0x00a8ff)
                    em.timestamp = datetime.datetime.utcnow()

                    await ctx.send(embed=em)

                else:

                    em = discord.Embed(
                        title="Why Tickets", description="That role already doesn't have access to tickets!", color=0x00a8ff)
                    em.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed=em)

            except:
                em = discord.Embed(
                    title="Why Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em)

        else:
            em = discord.Embed(
                title="Why Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

    @commands.command(help="This command sets an admin role for the ticket system", extras={"category":"Ticket"}, usage="addadminrole [roleid]", description="Adds an admin role for tickets")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def addadminrole(self, ctx, role_id=None):
        createticketfile(ctx)

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)
            with open(f"./database/tickets/ticket{ctx.guild.id}.json") as f:
                data = json.load(f)

            data["verified-roles"].append(role_id)
            with open(f'./database/tickets/ticket{ctx.guild.id}.json', 'w') as f:
                json.dump(data, f, indent=4)

            em = discord.Embed(
                title="Why Tickets", description="You have successfully added `{}` to the list of roles that can run admin-level commands!".format(role.name), color=0x00a8ff)
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        except:
            em = discord.Embed(
                title="Why Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

    @commands.command(help="This command removes an admin role from accessing the tickets", extras={"category":"Ticket"}, usage="deladminrole [roleid]", description="Removes an admin role from accessing tickets")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def deladminrole(self, ctx, role_id=None):
        createticketfile(ctx)
        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)
            with open(f"./database/tickets/ticket{ctx.guild.id}.json") as f:
                data = json.load(f)

            admin_roles = data["verified-roles"]

            if role_id in admin_roles:
                index = admin_roles.index(role_id)

                del admin_roles[index]

                data["verified-roles"] = admin_roles
                with open(f'./database/tickets/ticket{ctx.guild.id}.json', 'w') as f:
                    json.dump(data, f, indent=4)

                em = discord.Embed(title="Why Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(
                    role.name), color=0x00a8ff)
                em.timestamp = datetime.datetime.utcnow()

                await ctx.send(embed=em)

            else:
                em = discord.Embed(
                    title="Why Tickets", description="That role isn't getting pinged when new tickets are created!", color=0x00a8ff)
                em.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em)

        except:
            em = discord.Embed(
                title="Why Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(Ticket(client))
