import io
import chat_exporter
from dataclasses import dataclass
from core.helpers.views import ConfirmView
import discord


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


async def get_button(guild_id: int) -> discord.ui.Button:
    return discord.ui.Button()


class NewTicketView(discord.ui.View):
    def __init__(self, button: discord.ui.Button):
        super().__init__(timeout=None)
        self.add_item(button)


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
