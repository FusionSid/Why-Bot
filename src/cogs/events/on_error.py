import datetime

import discord
from discord.ext import commands
from discord import InteractionResponded, CheckFailure

from utils import WhyBot
from log import log_errors


class OnError(commands.Cog):
    def __init__(self, client : WhyBot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx : commands.Context, error):

        if isinstance(error, commands.CommandNotFound):
            return


        elif isinstance(error, commands.CommandOnCooldown):
            async def better_time(cd: int):
                time = f"{cd}s"
                if cd > 60:
                    minutes = cd - (cd % 60)
                    seconds = cd - minutes
                    minutes = int(minutes / 60)
                    time = f"{minutes}min {seconds}s"
                    if minutes > 60:
                        hoursglad = minutes - (minutes % 60)
                        hours = int(hoursglad / 60)
                        minutes = minutes - (hours*60)
                        time = f"{hours}h {minutes}min {seconds}s"
                return time

            cd = round(error.retry_after)
            if cd == 0:
                cd = 1
            retry_after = await better_time(cd)
            em = discord.Embed(
                title="Wow buddy, Slow it down\nThis command is on cooldown",
                description=f"Try again in **{retry_after}** ",
                color=discord.Color.red()
            )
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")
        

        elif isinstance(error, InteractionResponded):
            pass


        elif isinstance(error, CheckFailure):
            pass


        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                title="Missing a requred value / argument",
                description=f"You haven't passed in all the required values for this command",
                color=discord.Color.red()
            )
            em.add_field(name=f"You have not passed in:",
                         value=f"`{error.param}`")
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(
                title="Missing permissions",
                description="You don't have permissions to use this commands ",
                color=discord.Color.red()
            )
            em.add_field(name="Permissions you need:",
                         value=f"`{', '.join(error.missing_permissions)}`")
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.MessageNotFound):
            em = discord.Embed(
                title="Message not found",
                description="The bot failed to find the message ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.MemberNotFound):
            em = discord.Embed(
                title="Member not found",
                description="The bot failed to find the member ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.GuildNotFound):
            em = discord.Embed(
                title="Guild not found",
                description="The bot faield to find the guild ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.UserNotFound):
            em = discord.Embed(
                title="User not found",
                description="The bot failed to find the user ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.ChannelNotFound):
            em = discord.Embed(
                title="Channel not found",
                description="The bot failed to find the channel ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.ChannelNotReadable):
            em = discord.Embed(
                title="Channel not readable",
                description="The bot is unable to read this channel ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.RoleNotFound):
            em = discord.Embed(
                title="Role not found",
                description="The bot was unable to find the role ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.ThreadNotFound):
            em = discord.Embed(
                title="Thread not found",
                description="The bot was unable to fund the thread ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.BotMissingPermissions):
            em = discord.Embed(
                title="Bot missing permissions",
                description="Why bot does not have the permissions do execute this command. Please gimme them perms ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.MissingRole):
            em = discord.Embed(
                title="Missing Role",
                description="User does not have the role to run this command ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.BotMissingRole):
            em = discord.Embed(
                title="Bot Missing Role",
                description="Why bot does not have the role to run this command, Gimme them roles ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.NSFWChannelRequired):
            em = discord.Embed(
                title="NSFW Only",
                description="This command can only be used in an nsfw channel ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, commands.DisabledCommand):
            em = discord.Embed(
                title="Command Disabled",
                description="This command has been disabled ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        elif isinstance(error, discord.HTTPException):
            em = discord.Embed(
                title="Error 404 Not Found",
                description=f"{error.code} {error.text} ",
                color=discord.Color.red()
            )
            
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
            
            await ctx.message.add_reaction("⚠️")


        else:
            log_errors(type(error), error, error.__traceback__)


def setup(client : WhyBot):
    client.add_cog(OnError(client))