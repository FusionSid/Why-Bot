import discord
import datetime
from discord.ext import commands
from utils import Log
import traceback
import sys

log = Log()

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
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
                description=f"Try again in **{retry_after}**",
                color = discord.Color.red()
            )
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                title="Missing a requred value/arg",
                description="You haven't passed in all value/arg",
                color = discord.Color.red()
            )
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(
                title="Missing permissions",
                description="You don't have permissions to use this commands",
                color = discord.Color.red()
            )
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
        
        elif isinstance(error, commands.CheckFailure):
            return

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            err = [('Ignoring exception in command {}:'.format(ctx.command)),traceback.format_exception(type(error), error, error.__traceback__)]
            log.log_command_error(err)

def setup(client):
    client.add_cog(Errors(client))