import discord
from discord.ext import commands

from core.models.client import WhyBot
from core.helpers.log import log_errors
from core.utils.formatters import format_seconds


class OnError(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):

            retry_after = await format_seconds(int(error.retry_after))
            em = discord.Embed(
                title="Wow buddy, Slow it down\nThis command is on cooldown",
                description=f"Try again in **{retry_after}**",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                title="Missing a requred value / argument",
                description=f"You haven't passed in all the required values for this command",
                color=discord.Color.red(),
            )
            em.add_field(name=f"You have not passed in:", value=f"`{error.param}`")
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(
                title="Missing permissions",
                description="You don't have permissions to use this commands ",
                color=discord.Color.red(),
            )
            em.add_field(
                name="Permissions you need:",
                value=f"`{', '.join(error.missing_permissions)}`",
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.MessageNotFound):
            em = discord.Embed(
                title="Message not found",
                description="The bot failed to find the message ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.MemberNotFound):
            em = discord.Embed(
                title="Member not found",
                description="The bot failed to find the member ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.GuildNotFound):
            em = discord.Embed(
                title="Guild not found",
                description="The bot faield to find the guild ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.UserNotFound):
            em = discord.Embed(
                title="User not found",
                description="The bot failed to find the user ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.ChannelNotFound):
            em = discord.Embed(
                title="Channel not found",
                description="The bot failed to find the channel ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.ChannelNotReadable):
            em = discord.Embed(
                title="Channel not readable",
                description="The bot is unable to read this channel ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.RoleNotFound):
            em = discord.Embed(
                title="Role not found",
                description="The bot was unable to find the role ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.ThreadNotFound):
            em = discord.Embed(
                title="Thread not found",
                description="The bot was unable to fund the thread ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            em = discord.Embed(
                title="Bot missing permissions",
                description="Why bot does not have the permissions do execute this command. Please gimme them perms ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.MissingRole):
            em = discord.Embed(
                title="Missing Role",
                description="User does not have the role to run this command ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.NotOwner):
            em = discord.Embed(
                title="Not Owner",
                description="You must be owner of Why Bot to be able to run this command",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.BotMissingRole):
            em = discord.Embed(
                title="Bot Missing Role",
                description="Why bot does not have the role to run this command, Gimme them roles ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.NSFWChannelRequired):
            em = discord.Embed(
                title="NSFW Only",
                description="This command can only be used in an nsfw channel ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.DisabledCommand):
            em = discord.Embed(
                title="Command Disabled",
                description="This command has been disabled ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, commands.NoPrivateMessage):
            em = discord.Embed(
                title="Command not allowed in private message",
                description="This command has been disabled in private messages/dms and can be only used in a server/guild",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, discord.HTTPException):
            em = discord.Embed(
                title="Error 404 Not Found",
                description=f"{error.code} {error.text} ",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)

        elif isinstance(error, discord.CheckFailure):
            em = discord.Embed(
                title="You cannot use this command!",
                description="Reasons why it may not be working for you:\n- You are blacklisted\n- The plugin where the command belongs to is disabled",
                color=discord.Color.red(),
            )
            await ctx.respond(embed=em, ephemeral=True)
        else:
            log_errors(type(error), error, error.__traceback__)


def setup(client: WhyBot):
    client.add_cog(OnError(client))
