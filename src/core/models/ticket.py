import time
import io
from dataclasses import dataclass

import discord
import chat_exporter

from core.models.client import WhyBot
from core.utils.formatters import discord_timestamp
from core.db.setup_guild import setup_tickets
from core.helpers.views import ConfirmView, InputModalView


@dataclass
class TicketGuild:
    guild_id: int
    roles_allowed: list[int]
    ping_roles: list[int]
    create_button: bool
    category: int
    banned_users: list[int]


@dataclass
class Ticket:
    ticket_id: int
    guild_id: int
    channel_id: int
    ticket_creator: int
    time_created: int


class TicketView(discord.ui.View):
    def __init__(self, ticket_state: Ticket, member: discord.Member, client):
        self.member = member
        self.ticket = ticket_state
        self.client = client
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.gray, emoji="🔒")
    async def callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        # send a button to confirm to close or not
        are_you_sure = ConfirmView(target=interaction.user)
        em = discord.Embed(
            title="Close Ticket?",
            description=(
                f"{interaction.user.mention} are you sure you want to close this ticket?\nThis action removes \
                    access for the person who made the ticket from the channel\nHowever this action can be reversed"
            ),
            color=discord.Color.random(),
        )
        await interaction.response.send_message(
            embed=em, view=are_you_sure, ephemeral=True
        )
        await are_you_sure.wait()

        # if they hit no, do nothing
        if not are_you_sure.accepted:
            return

        # send the closed ticket view
        view = ClosedTicketView(self.ticket, self.member, self.client)
        embed = discord.Embed(
            title="Ticket has been closed!",
            description=f"Closed by: {interaction.user.mention}\nTo view a transcript of messages in this \
                channel hit the transcript button.\nNote that this will be an html file \
                    so you'll need to download it and open in a webbrowser",
        )
        await interaction.followup.send(embed=embed, view=view)
        await interaction.channel.set_permissions(
            self.member, send_messages=False, read_messages=False
        )
        try:
            await interaction.delete_original_message()
        except discord.Forbidden:
            return
        self.stop()


class ClosedTicketView(discord.ui.View):
    def __init__(self, ticket_state: Ticket, member: discord.Member, client):
        self.member = member
        self.ticket = ticket_state
        self.transcript = None
        self.client = client
        super().__init__(timeout=None)

    @discord.ui.button(label="Transcript", style=discord.ButtonStyle.grey, emoji="📄")
    async def transcript_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()
        if self.transcript is None:
            transcript = await chat_exporter.export(
                interaction.channel,
                limit=1000,
                tz_info="UTC",
                military_time=True,
                bot=self.client,
            )

            if transcript is None:
                return

            self.transcript_file = io.BytesIO(transcript.encode())
        await interaction.followup.send(
            file=discord.File(
                self.transcript_file,
                filename=f"transcript-{interaction.channel.name}.html",
            )
        )

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.grey, emoji="🗑️")
    async def delete_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        # send a button to confirm to close or not
        are_you_sure = ConfirmView(target=interaction.user)
        em = discord.Embed(
            title="Close Ticket?",
            description=(
                f"{interaction.user.mention} are you sure you want to DELETE this ticket?\n\
                    This action is permanent and can NOT be reversed"
            ),
            color=discord.Color.random(),
        )
        await interaction.response.send_message(
            embed=em, view=are_you_sure, ephemeral=True
        )
        await are_you_sure.wait()
        # if they hit no, do nothing
        if not are_you_sure.accepted:
            return

        await interaction.channel.delete()
        await self.client.db.execute(
            "DELETE FROM tickets WHERE id=$1", self.ticket.ticket_id
        )

    @discord.ui.button(label="Reopen", style=discord.ButtonStyle.grey, emoji="🔓")
    async def reopen_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()

        embed = discord.Embed(
            title=f"Ticket from {self.member.name} has been reopened!",
            description=f"Ticket was reopened by: {interaction.user}",
        )
        embed.set_footer(text="To close this ticket click the close button")
        view = TicketView(self.ticket, self.member, self.client)
        await interaction.followup.send(embed=embed, view=view)

        perms = {
            "send_messages": True,
            "read_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "read_message_history": True,
            "external_emojis": True,
        }
        await interaction.channel.set_permissions(self.member, **perms)

        try:
            await interaction.delete_original_message()
        except discord.Forbidden:
            return
        self.stop()


class NewTicketView(discord.ui.View):
    def __init__(self, guild_id: int, client: WhyBot):
        self.client = client
        self.guild_id = guild_id
        super().__init__(timeout=None)

        button = discord.ui.Button(
            label="New Ticket",
            style=discord.ButtonStyle.gray,
            emoji="📩",
            custom_id=f"new-ticket-view-{guild_id}",
        )
        button.callback = self.callback
        self.add_item(button)

    async def callback(self, interaction: discord.Interaction):
        # ik what ur thinking tHIs iS just COPy PaSTED codE fROm TIckEts.pY
        # well stfu didnt ask im lazy ok
        modal = InputModalView(
            title="Ticket Reason", label="Enter the reason why you're making the ticket"
        )
        modal.children[0].max_length = 2000
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.value is None:
            return await interaction.followup.send("Invalid Input", ephemeral=True)

        data: list[list] = await self.client.db.fetch(
            "SELECT * FROM ticket_guild WHERE guild_id=$1", self.guild_id
        )
        if len(data) == 0:
            await setup_tickets(self.client.db, self.guild_id)
            default_data = [self.guild_id, [], [], False, None, []]
            ticket_config = TicketGuild(*default_data)
        else:
            ticket_config = TicketGuild(*data[0])

        if interaction.user.id in ticket_config.banned_users:
            return await interaction.followup.send(
                "You are banned from making tickets (imagine)", ephemeral=True
            )

        # figure out if to make it in a category or not
        if ticket_config.category in (0, None):
            category = None
        else:
            category = list(
                filter(
                    lambda i: i.id == ticket_config.category,
                    interaction.guild.categories,
                )
            )
            category = None if len(category) == 0 else category[0]

        # create channel
        channel = await interaction.guild.create_text_channel(
            f"ticket-{interaction.user.id}", category=category
        )

        # set channel perms
        await channel.set_permissions(
            interaction.guild.get_role(interaction.guild.id),
            send_messages=False,
            read_messages=False,
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
        await channel.set_permissions(interaction.user, **perms)
        for role in ticket_config.roles_allowed:
            if role := interaction.guild.get_role(role) is not None:
                await channel.set_permissions(role, **perms)

        ticket_data = [
            interaction.guild.id,
            channel.id,
            interaction.user.id,
            int(time.time()),
        ]
        ticket_id = await self.client.db.fetch(
            """INSERT INTO tickets (
                guild_id, channel_id, ticket_creator, time_created
            ) VALUES ($1, $2, $3, $4) RETURNING id""",
            *ticket_data,
        )

        ticket = Ticket(ticket_id[0][0], *ticket_data)

        embed = discord.Embed(
            title=f"New ticket from {interaction.user.name}!",
            description=f"**Please wait, support will be with you shortly!**\
                \n\nTicket Created: {await discord_timestamp(ticket.time_created, 'ts')}",
            color=discord.Color.random(),
        )
        embed.add_field(name="Reason Provided:", value=str(modal.value))
        embed.set_footer(text="To close this ticket click the close button")
        view = TicketView(ticket, interaction.user, self.client)
        await channel.send(embed=embed, view=view)

        await interaction.followup.send(
            f"A new ticket has been created for you: {channel.mention}", ephemeral=True
        )
