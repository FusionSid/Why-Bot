import discord
from discord.ext import commands
from discord.commands import ApplicationContext, Option, slash_command

async def finished_callback(sink, channel: discord.TextChannel, *args):
    recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
    await sink.vc.disconnect()
    files = [
        discord.File(audio.file, f"{user_id}.{sink.encoding}")
        for user_id, audio in sink.audio_data.items()
    ]
    await channel.send(
        f"Finished! Recorded audio for {', '.join(recorded_users)}.", files=files
    )


class VC(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="startrec", description="Start")
    async def startrec(
        self,
        ctx,encoding
        # encoding: Option(str, choices=["mp3","wav","pcm","ogg","mka","mkv","mp4","m4a",],),
    ):
        """
        Record your voice!
        """

        voice = ctx.author.voice

        if not voice:
            return await ctx.send("You're not in a vc right now")

        vc = await voice.channel.connect()
        self.client.connections.update({ctx.guild.id: vc})

        if encoding == "mp3":
            sink = discord.sinks.MP3Sink()
        elif encoding == "wav":
            sink = discord.sinks.WaveSink()
        elif encoding == "pcm":
            sink = discord.sinks.PCMSink()
        elif encoding == "ogg":
            sink = discord.sinks.OGGSink()
        elif encoding == "mka":
            sink = discord.sinks.MKASink()
        elif encoding == "mkv":
            sink = discord.sinks.MKVSink()
        elif encoding == "mp4":
            sink = discord.sinks.MP4Sink()
        elif encoding == "m4a":
            sink = discord.sinks.M4ASink()
        else:
            return await ctx.send("Invalid encoding.")

        vc.start_recording(
            sink,
            finished_callback,
            ctx.channel,
        )

        await ctx.send("The recording has started!")


    

    @commands.command(name="stoprec", description="Stop")
    async def stoprec(self, ctx):
        """
        Stop recording.
        """
        if ctx.guild.id in self.client.connections:
            vc = self.client.connections[ctx.guild.id]
            vc.stop_recording()
            del self.client.connections[ctx.guild.id]
            await ctx.delete()
        else:
            await ctx.send("Not recording in this guild.")



def setup(client):
    client.add_cog(VC(client))


