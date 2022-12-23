import io
import time

import discord
import chat_exporter
from discord.ext import commands
from discord.commands import SlashCommandGroup, default_permissions

from core.models import WhyBot
from core.helpers.views import ConfirmView
from core.db.setup_guild import setup_tickets
from core.utils.formatters import discord_timestamp
from core.helpers.checks import run_bot_checks
from core.models.ticket import (
    TicketGuild,
    Ticket,
    TicketView,
    NewTicketView,
    ClosedTicketView,
)


class Tickets(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    ticket = SlashCommandGroup("ticket", "Ticket related commands")

    async def __get_ticket_config(self, guild_id: int):
        data: list[list] = await self.client.db.fetch(
            "SELECT * FROM ticket_guild WHERE guild_id=$1", guild_id
        )
        if len(data) == 0:
            await setup_tickets(self.client.db, guild_id)
            default_data = [guild_id, [], [], False, None, []]
            return TicketGuild(*default_data)
        return TicketGuild(*data[0])

    async def __get_tickets(self, guild_id: int):
        data: list[list] = await self.client.db.fetch(
            "SELECT * FROM tickets WHERE guild_id=$1", guild_id
        )
        if len(data) == 0:
            return None
        return list(map(lambda x: Ticket(*x), data))

    @ticket.command()
    async def new(self, ctx: discord.ApplicationContext, reason=None):
        await ctx.defer()
        ticket_config = await self.__get_ticket_config(ctx.guild.id)
        if ctx.author.id in ticket_config.banned_users:
            return await ctx.respond(
                "You are banned from making tickets", ephemeral=True
            )

        # figure out if to make it in a category or not
        if ticket_config.category in (0, None):
            category = None
        else:
            category = list(
                filter(lambda i: i.id == ticket_config.category, ctx.guild.categories)
            )
            category = None if len(category) == 0 else category[0]

        # create channel
        channel = await ctx.guild.create_text_channel(
            f"ticket-{ctx.author.id}", category=category
        )

        # set channel perms
        await channel.set_permissions(
            ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False
        )
        perms = {
            "send_messages": True,
            "read_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "read_message_history": True,
            "external_emojis": True,
        }
        await channel.set_permissions(ctx.author, **perms)
        for role in ticket_config.roles_allowed:
            if (role := ctx.guild.get_role(role)) is not None:
                await channel.set_permissions(role, **perms)

        ticket_data = [ctx.guild.id, channel.id, ctx.author.id, int(time.time())]
        ticket_id = await self.client.db.fetch(
            """INSERT INTO tickets (
                guild_id, channel_id, ticket_creator, time_created
            ) VALUES ($1, $2, $3, $4) RETURNING id""",
            *ticket_data,
        )

        ticket = Ticket(ticket_id[0][0], *ticket_data)

        embed = discord.Embed(
            title=f"New ticket from {ctx.author.name}!",
            description=f"**Please wait, support will be with you shortly!**\
                \n\nTicket Created: {await discord_timestamp(ticket.time_created, 'ts')}",
            color=discord.Color.random(),
        )
        embed.add_field(name="Reason Provided:", value=str(reason))
        embed.add_field(name="Ticket ID:", value=ticket.ticket_id)
        embed.set_footer(text="To close this ticket click the close button")
        view = TicketView(ticket, ctx.author, self.client)

        who_to_ping = filter(
            lambda x: x is not None, map(ctx.guild.get_role, ticket_config.ping_roles)
        )
        await channel.send(
            embed=embed, view=view, content="".join(i.mention for i in who_to_ping)
        )

        await ctx.respond(f"A new ticket has been created for you: {channel.mention}")

    @ticket.command()
    async def close(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        tickets = await self.__get_tickets(ctx.guild.id)
        ticket = list(filter(lambda t: t.channel_id == ctx.channel_id, tickets))
        if not ticket:
            embed = discord.Embed(
                title="Could Not Find Ticket",
                description="This channel is not a ticket",
                color=discord.Color.random(),
            )
            return await ctx.respond(embed=embed, ephemeral=True)
        ticket: Ticket = ticket[0]
        are_you_sure = ConfirmView(target=ctx.author)
        em = discord.Embed(
            title="Close Ticket?",
            description=(
                f"{ctx.author.mention} are you sure you want to close this ticket?\nThis action removes \
                    access for the person who made the ticket from the channel\nHowever this action can be reversed"
            ),
            color=discord.Color.random(),
        )
        await ctx.respond(embed=em, view=are_you_sure, ephemeral=True)
        await are_you_sure.wait()

        # if they hit no, do nothing
        if not are_you_sure.accepted:
            return

        # send the closed ticket view
        member = ctx.guild.get_member(ticket.ticket_creator)
        if member is None:
            return
        view = ClosedTicketView(ticket, ctx.author, self.client)
        embed = discord.Embed(
            title="Ticket has been closed!",
            description=f"Closed by: {ctx.author.mention}\nTo view a transcript of messages in this \
                channel hit the transcript button.\nNote that this will be an html file \
                    so you'll need to download it and open in a webbrowser",
        )
        await ctx.send(embed=embed, view=view)
        await ctx.channel.set_permissions(
            member, send_messages=False, read_messages=False
        )

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def rename(self, ctx: discord.ApplicationContext, new_name: str):
        await ctx.defer()
        tickets = await self.__get_tickets(ctx.guild.id)
        ticket = list(filter(lambda t: t.channel_id == ctx.channel_id, tickets))
        if not ticket:
            embed = discord.Embed(
                title="Could Not Find Ticket",
                description="This channel is not a ticket",
                color=discord.Color.random(),
            )
            return await ctx.respond(embed=embed, ephemeral=True)
        ticket = ticket[0]
        await ctx.channel.edit(name=new_name)
        await ctx.respond("Ticket name updated!")

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def transcript(self, ctx: discord.ApplicationContext):
        transcript = await chat_exporter.export(
            ctx.channel,
            limit=1000,
            tz_info="UTC",
            military_time=True,
            bot=self.client,
        )

        if transcript is None:
            return await ctx.respond("Failed to generate transcript", ephemeral=True)

        self.transcript_file = io.BytesIO(transcript.encode())
        await ctx.respond(
            file=discord.File(
                self.transcript_file,
                filename=f"transcript-{ctx.channel.name}.html",
            )
        )

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def button(self, ctx: discord.ApplicationContext):
        view = NewTicketView(ctx.guild.id, self.client)
        await ctx.respond("Created button view!", ephemeral=True)
        await ctx.send(
            embed=discord.Embed(
                title="New Ticket",
                description="Press the New Ticket button to create a new ticket!",
                color=discord.Color.random(),
            ),
            view=view,
        )
        await self.client.db.execute(
            "UPDATE ticket_guild SET create_button=true WHERE guild_id=$1", ctx.guild.id
        )

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        tickets = await self.__get_tickets(ctx.guild.id)
        ticket = list(filter(lambda t: t.channel_id == ctx.channel_id, tickets))
        if not ticket:

            embed = discord.Embed(
                title="Could Not Find Ticket",
                description="This channel is not a ticket",
                color=discord.Color.random(),
            )
            return await ctx.respond(embed=embed, ephemeral=True)
        ticket: Ticket = ticket[0]
        await self.client.db.execute(
            "DELETE FROM tickets WHERE id=$1 AND guild_id=$2",
            ticket.ticket_id,
            ctx.guild.id,
        )
        await ctx.channel.delete()

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def delete_all(self, ctx: discord.ApplicationContext):
        # send a button to confirm to close or not
        are_you_sure = ConfirmView(target=ctx.author)
        em = discord.Embed(
            title="Delete ALL tickets?",
            description=(
                f"{ctx.author.mention} are you sure you want to close and delete ALL tickets?\n\
                    This action can not be reversed"
            ),
            color=discord.Color.random(),
        )
        await ctx.respond(embed=em, view=are_you_sure, ephemeral=True)
        await are_you_sure.wait()
        if not are_you_sure.accepted:
            return

        tickets = await self.__get_tickets(ctx.guild.id)
        channels = map(self.client.get_channel, (i.channel_id for i in tickets))
        for channel in channels:
            try:
                await channel.delete()
            except (AttributeError, discord.Forbidden):
                continue
        await self.client.db.execute(
            "DELETE FROM tickets WHERE guild_id=$1", ctx.guild.id
        )
        await ctx.send("All tickets have been deleted!")

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def add_ping_role(self, ctx: discord.ApplicationContext, role: discord.Role):
        ticket_config = await self.__get_ticket_config(ctx.guild.id)
        if role.id in ticket_config.ping_roles:
            return await ctx.respond(
                "Role is already in list for being pinged when tickets are made"
            )
        await self.client.db.execute(
            "UPDATE ticket_guild SET ping_roles = array_append(ping_roles, $1), \
                roles_allowed = array_append(roles_allowed, $1) WHERE guild_id=$2",
            role.id,
            ctx.guild.id,
        )
        await ctx.respond(
            embed=discord.Embed(
                title="Ping Role Added",
                description=f"{role.mention} will now be pinged when a new ticket is made",
                color=discord.Color.random(),
            )
        )

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def remove_ping_role(
        self, ctx: discord.ApplicationContext, role: discord.Role
    ):
        ticket_config = await self.__get_ticket_config(ctx.guild.id)
        if role.id not in ticket_config.ping_roles:
            return await ctx.respond(
                "Role was already not in the list for being pinged when tickets are made"
            )
        await self.client.db.execute(
            "UPDATE ticket_guild SET ping_roles = array_remove(ping_roles, $1) WHERE guild_id=$2",
            role.id,
            ctx.guild.id,
        )
        await ctx.respond(
            embed=discord.Embed(
                title="Ping Role Removed",
                description=f"{role.mention} will no longer be pinged when a new ticket is made",
                color=discord.Color.random(),
            )
        )

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def add_allowed_role(
        self, ctx: discord.ApplicationContext, role: discord.Role
    ):
        ticket_config = await self.__get_ticket_config(ctx.guild.id)
        if role.id in ticket_config.roles_allowed:
            return await ctx.respond(
                "Role is already in the list that have access to new tickets"
            )
        await self.client.db.execute(
            "UPDATE ticket_guild SET roles_allowed = array_append(roles_allowed, $1) WHERE guild_id=$2",
            role.id,
            ctx.guild.id,
        )
        await ctx.respond(
            embed=discord.Embed(
                title="Role Access Added",
                description=f"{role.mention} now has access to new tickets",
                color=discord.Color.random(),
            )
        )

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def remove_allowed_role(
        self, ctx: discord.ApplicationContext, role: discord.Role
    ):
        ticket_config = await self.__get_ticket_config(ctx.guild.id)
        if role.id not in ticket_config.roles_allowed:
            return await ctx.respond(
                "Role is already not in the list that have access to new tickets"
            )
        await self.client.db.execute(
            "UPDATE ticket_guild SET roles_allowed = array_remove(roles_allowed, $1) WHERE guild_id=$2",
            role.id,
            ctx.guild.id,
        )
        await ctx.respond(
            embed=discord.Embed(
                title="Role Access Removed",
                description=f"{role.mention} no longer has access to new tickets",
                color=discord.Color.random(),
            )
        )

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def ban_user(self, ctx: discord.ApplicationContext, member: discord.Member):
        ticket_config = await self.__get_ticket_config(ctx.guild.id)
        if member.id in ticket_config.banned_users:
            return await ctx.respond("User is already banned from making tickets")
        await self.client.db.execute(
            "UPDATE ticket_guild SET banned_users = array_append(banned_users, $1) WHERE guild_id=$2",
            member.id,
            ctx.guild.id,
        )
        await ctx.respond(
            embed=discord.Embed(
                title="User Banned",
                description=f"{member.mention} is banned from making tickets",
                color=discord.Color.random(),
            )
        )

    @ticket.command()
    @default_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def unban_user(self, ctx: discord.ApplicationContext, member: discord.Member):
        ticket_config = await self.__get_ticket_config(ctx.guild.id)
        if member.id not in ticket_config.banned_users:
            return await ctx.respond("User is already unbanned from making tickets")
        await self.client.db.execute(
            "UPDATE ticket_guild SET banned_users = array_remove(banned_users, $1) WHERE guild_id=$2",
            member.id,
            ctx.guild.id,
        )
        await ctx.respond(
            embed=discord.Embed(
                title="User Unbanned",
                description=f"{member.mention} is no longer banned from making tickets",
                color=discord.Color.random(),
            )
        )


def setup(client):
    client.add_cog(Tickets(client))
