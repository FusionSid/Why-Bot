import discord
import asyncio
from discord.ext import commands
import youtube_dl
from youtubesearchpython import VideosSearch
from multiprocessing import Pool
import os
import platform
import discord.voice_client
import nacl
import json
from gtts import gTTS
from mutagen.mp3 import MP3


ffmpeg = "/home/runner/Why-Bot/Why-Bot/ffmpeg.exe"
cookies = "/home/runner/Why-Bot/cookies.txt"
ffmpeg_options = {  # ffmpeg options
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}


loops = {}  # for +loop command
queues = {}  # for queues
now_playing_pos = {}  # to display the current song in +queue command correctly
all_queues_info = {}  # all queue info, for +queue command

# function, which splitting the queue into queues of 10 songs


def split(arr, size):
    arrays = []
    while len(arr) > size:
        pice = arr[:size]
        arrays.append(pice)
        arr = arr[size:]
    arrays.append(arr)
    return arrays


# function, which "loop" loops, checks the queue and replays the remaining links
def check_new_songs(guild_id, vc):
    global queues
    global now_playing_pos
    global all_queues_info

    # if the bot is not playing any songs, deleting the queue
    if not vc.is_connected():
        if guild_id in queues:
            del queues[guild_id]
        if guild_id in all_queues_info:
            del all_queues_info[guild_id]
        if guild_id in loops:
            del loops[guild_id]
        if guild_id in now_playing_pos:
            del now_playing_pos[guild_id]
        return

    # "loop" loops
    if guild_id in loops:
        if loops[guild_id] == "current track":
            src_video_url = queues[guild_id][0]["src_url"]

            # play music
            try:
                vc.play(discord.FFmpegPCMAudio(
                        src_video_url,
                        before_options=ffmpeg_options["before_options"],
                        options=ffmpeg_options["options"]
                        ), after=lambda a: check_new_songs(guild_id, vc))
            except discord.errors.ClientException:
                pass

            return

    if queues[guild_id]:
        queues[guild_id].pop(0)

        try:
            src_video_url = queues[guild_id][0]["src_url"]
            now_playing_pos[guild_id] += 1
        except IndexError:
            # if queue is empty and there is no queue loop, deleting the variables and return
            if guild_id not in loops or loops[guild_id] != "queue":
                del queues[guild_id]
                del all_queues_info[guild_id]
                del now_playing_pos[guild_id]
                return

            # else looping queue
            for track in all_queues_info[guild_id]:
                queues[guild_id].append(
                    {"url": track["url"], "src_url": track["src_url"]})
            now_playing_pos[guild_id] = 0
            src_video_url = queues[guild_id][0]["src_url"]

        # play music
        try:
            vc.play(discord.FFmpegPCMAudio(
                    src_video_url,
                    before_options=ffmpeg_options["before_options"],
                    options=ffmpeg_options["options"]
                    ), after=lambda a: check_new_songs(guild_id, vc))
        except discord.errors.ClientException:
            return


# this function extracts all info from video url
def extract_info(url):
    try:
        return youtube_dl.YoutubeDL({"format": "bestaudio", "cookiefile": cookies}).extract_info(url, download=False)
    # if there is an error, changing format
    except youtube_dl.utils.ExtractorError and youtube_dl.utils.DownloadError:
        return youtube_dl.YoutubeDL({"format": "95", "cookiefile": cookies}).extract_info(url, download=False)


async def playy(ctx, video=None):
    global queues
    global now_playing_pos
    global all_queues_info

    if ctx.author.voice is None:
        return await ctx.send(f"{ctx.author.mention}, You have to be connected to a voice channel.")

    channel = ctx.author.voice.channel
    if ctx.voice_client is None:  # if bot is not connected to a voice channel, connecting to a voice channel
        await channel.connect()
    else:  # else, just moving to ctx author voice channel
        await ctx.voice_client.move_to(channel)

    # self deaf
    await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)

    if video is None:
        return

    # searching for a video
    video_search = video
    if "https://www.youtube.com/" in video or "https://youtu.be/" in video:
        video_url = ""
        for el in video.split():
            if "https://www.youtube.com/" in el or "https://youtu.be/" in el:
                if "list=" in el:
                    await ctx.send("Loading playlist...")
                video_url = el
    else:
        video = VideosSearch(video, limit=1)
        video_url = video.result()["result"][0]["link"]

    # finding source video url
    pool = Pool()  # creating new pool which will extract all video info
    information = pool.apply_async(
        func=extract_info, args=(video_url,)).get()
    pool.close()  # closing pool
    pool.join()

    # if it's not a playlist, playing the song as usual
    if "_type" not in information:
        src_video_url = information["formats"][0]["url"]  # source url
        video_title = information["title"]

        # filling queues
        if ctx.guild.id in queues:
            queues[ctx.guild.id].append(
                {"url": video_url, "src_url": src_video_url})
            all_queues_info[ctx.guild.id].append(
                {"name": video_title, "url": video_url, "src_url": src_video_url})
        else:
            queues[ctx.guild.id] = [
                {"url": video_url, "src_url": src_video_url}]
            now_playing_pos[ctx.guild.id] = 0
            all_queues_info[ctx.guild.id] = [
                {"name": video_title, "url": video_url, "src_url": src_video_url}]

    else:  # else queueing playlist
        src_video_url = information["entries"][0]["url"]
        video_title = information["title"]

        # queuing first song
        if ctx.guild.id in queues:
            queues[ctx.guild.id].append(
                {"url": video_url, "src_url": src_video_url})
            all_queues_info[ctx.guild.id].append(
                {"name": information["entries"][0]["title"], "url": video_url, "src_url": src_video_url})
        else:
            queues[ctx.guild.id] = [
                {"url": video_url, "src_url": src_video_url}]
            now_playing_pos[ctx.guild.id] = 0
            all_queues_info[ctx.guild.id] = [
                {"name": information["entries"][0]["title"], "url": video_url, "src_url": src_video_url}]

        # queuing another songs
        for v in information["entries"]:
            if information["entries"].index(v) != 0:
                queues[ctx.guild.id].append(
                    {"url": video_url, "src_url": v["url"]})
                all_queues_info[ctx.guild.id].append(
                    {"name": v["title"], "url": video_url, "src_url": src_video_url})

    vc = ctx.voice_client

    try:
        vc.play(discord.FFmpegPCMAudio(
            src_video_url,
            before_options=ffmpeg_options["before_options"],
            options=ffmpeg_options["options"]
            # calling the check_new_songs function after playing the current music
        ), after=lambda a: check_new_songs(ctx.guild.id, vc))
    except discord.errors.ClientException:
        pass

    # Adding embed, depending on the queue
    if len(queues[ctx.guild.id]) != 1:
        embed = discord.Embed(
            title="Queue",
            description=f"🔎 Searching for `{video_search}`\n\n" +
            f"""✅ [{video_title}]({video_url}) - successfully added to queue.""",
            color=0x515596)
    else:
        embed = discord.Embed(
            title="Now playing",
            description=f"✅ Successfully joined to `{channel}`\n\n" +
            f"🔎 Searching for `{video_search}`\n\n" +
            f"""▶️ Now playing - [{video_title}]({video_url})""",
            color=0x515596)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    # join command
    @commands.command(aliases=["j"])
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send(f"{ctx.author.mention}, You have to be connected to a voice channel.")

        channel = ctx.author.voice.channel

        if ctx.voice_client is None:  # if bot is not connected to a voice channel, connecting to a voice channel
            await channel.connect()
        else:  # else, just moving to ctx author voice channel
            await ctx.voice_client.move_to(channel)

        # self deaf
        await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)

        await ctx.send(f"✅ Successfully joined to `{channel}`")

    # play command
    # noinspection PyTypeChecker

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, video=None):
        global queues
        global now_playing_pos
        global all_queues_info

        if ctx.author.voice is None:
            return await ctx.send(f"{ctx.author.mention}, You have to be connected to a voice channel.")

        channel = ctx.author.voice.channel
        if ctx.voice_client is None:  # if bot is not connected to a voice channel, connecting to a voice channel
            await channel.connect()
        else:  # else, just moving to ctx author voice channel
            await ctx.voice_client.move_to(channel)

        # self deaf
        await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)

        if video is None:
            return

        # searching for a video
        video_search = video
        if "https://www.youtube.com/" in video or "https://youtu.be/" in video:
            video_url = ""
            for el in video.split():
                if "https://www.youtube.com/" in el or "https://youtu.be/" in el:
                    if "list=" in el:
                        await ctx.send("Loading playlist...")
                    video_url = el
        else:
            video = VideosSearch(video, limit=1)
            video_url = video.result()["result"][0]["link"]

        # finding source video url
        pool = Pool()  # creating new pool which will extract all video info
        information = pool.apply_async(
            func=extract_info, args=(video_url,)).get()
        pool.close()  # closing pool
        pool.join()

        # if it's not a playlist, playing the song as usual
        if "_type" not in information:
            src_video_url = information["formats"][0]["url"]  # source url
            video_title = information["title"]

            # filling queues
            if ctx.guild.id in queues:
                queues[ctx.guild.id].append(
                    {"url": video_url, "src_url": src_video_url})
                all_queues_info[ctx.guild.id].append(
                    {"name": video_title, "url": video_url, "src_url": src_video_url})
            else:
                queues[ctx.guild.id] = [
                    {"url": video_url, "src_url": src_video_url}]
                now_playing_pos[ctx.guild.id] = 0
                all_queues_info[ctx.guild.id] = [
                    {"name": video_title, "url": video_url, "src_url": src_video_url}]

        else:  # else queueing playlist
            src_video_url = information["entries"][0]["url"]
            video_title = information["title"]

            # queuing first song
            if ctx.guild.id in queues:
                queues[ctx.guild.id].append(
                    {"url": video_url, "src_url": src_video_url})
                all_queues_info[ctx.guild.id].append(
                    {"name": information["entries"][0]["title"], "url": video_url, "src_url": src_video_url})
            else:
                queues[ctx.guild.id] = [
                    {"url": video_url, "src_url": src_video_url}]
                now_playing_pos[ctx.guild.id] = 0
                all_queues_info[ctx.guild.id] = [
                    {"name": information["entries"][0]["title"], "url": video_url, "src_url": src_video_url}]

            # queuing another songs
            for v in information["entries"]:
                if information["entries"].index(v) != 0:
                    queues[ctx.guild.id].append(
                        {"url": video_url, "src_url": v["url"]})
                    all_queues_info[ctx.guild.id].append(
                        {"name": v["title"], "url": video_url, "src_url": src_video_url})

        vc = ctx.voice_client

        try:
            vc.play(discord.FFmpegPCMAudio(
                src_video_url,
                before_options=ffmpeg_options["before_options"],
                options=ffmpeg_options["options"]
                # calling the check_new_songs function after playing the current music
            ), after=lambda a: check_new_songs(ctx.guild.id, vc))
        except discord.errors.ClientException:
            pass

        # Adding embed, depending on the queue
        if len(queues[ctx.guild.id]) != 1:
            embed = discord.Embed(
                title="Queue",
                description=f"🔎 Searching for `{video_search}`\n\n" +
                f"""✅ [{video_title}]({video_url}) - successfully added to queue.""",
                color=0x515596)
        else:
            embed = discord.Embed(
                title="Now playing",
                description=f"✅ Successfully joined to `{channel}`\n\n" +
                f"🔎 Searching for `{video_search}`\n\n" +
                f"""▶️ Now playing - [{video_title}]({video_url})""",
                color=0x515596)

        await ctx.send(embed=embed)

    # skip command

    @commands.command(aliases=["s"])
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any songs for you.")

        if ctx.author.voice is None:
            return await ctx.send(f"{ctx.author.mention}, You have to be connected to a voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("You are in the wrong channel.")

        ctx.voice_client.stop()  # skipping current track
        await ctx.message.add_reaction("✅")  # adding a reaction
        await ctx.send("Successfully skipped.")

    # leave command

    @commands.command(aliases=["l", "disconnect", "d"])
    async def leave(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any songs for you.")

        if ctx.author.voice is None:
            return await ctx.send(f"{ctx.author.mention}, You have to be connected to a voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("You are in the wrong channel.")

        await ctx.voice_client.disconnect()  # leaving a voice channel
        await ctx.message.add_reaction("✅")  # adding a reaction
        await ctx.send("Successfully disconnected.")

        # clearing queues and loops
        if ctx.guild.id in queues:
            del queues[ctx.guild.id]
        if ctx.guild.id in all_queues_info:
            del all_queues_info[ctx.guild.id]
        if ctx.guild.id in loops:
            del loops[ctx.guild.id]
        if ctx.guild.id in now_playing_pos:
            del now_playing_pos[ctx.guild.id]

    # stop command

    @commands.command(aliases=["stop"])
    async def pause(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any songs for you.")

        if ctx.author.voice is None:
            return await ctx.send(f"{ctx.author.mention}, You have to be connected to a voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("You are in the wrong channel.")

        ctx.voice_client.pause()  # stopping a music
        await ctx.message.add_reaction("✅")  # adding a reaction
        await ctx.send("⏸️ Successfully paused.")

    # continue command

    @commands.command(aliases=["continue", "unpause"])
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any songs for you.")

        if ctx.author.voice is None:
            return await ctx.send(f"{ctx.author.mention}, You have to be connected to a voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("You are in the wrong channel.")

        ctx.voice_client.resume()  # resume music
        await ctx.message.add_reaction("✅")  # adding a reaction
        await ctx.send("▶️ Successfully resumed.")

    # queue command

    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        global all_queues_info

        # if queue is empty, sending empty embed
        if ctx.voice_client is None:
            await ctx.send(embed=discord.Embed(title="Current Queue", description="Your current queue is empty!", color=0x515596))
        else:
            position = 0
            if ctx.guild.id in all_queues_info:
                # splitting the queue into queues of 10 songs
                queue_info = split(all_queues_info[ctx.guild.id], 10)
            else:
                return await ctx.send(embed=discord.Embed(
                    title="Current Queue",
                    description="Your current queue is empty!",
                    color=0x515596)
                )
            print(all_queues_info)
            content = []
            for _ in queue_info:
                content.append("")
            page = 0

            # filling content with songs

            for i in queue_info:
                for j in i:
                    if position == now_playing_pos[ctx.guild.id]:
                        content[page] += f"""{position+1}. [{j["name"]}]({j["url"]}) ⟵ current track\n"""  # output the current song
                    else:
                        content[page] += f"""{position+1}. [{j["name"]}]({j["url"]})\n"""
                    position += 1
                if page < len(queue_info) - 1:
                    page += 1

            # getting information about loops
            loops_info = ""
            if ctx.guild.id not in loops or loops[ctx.guild.id] == "none":
                loops_info = "🔁 Queue loop: disabled | 🔁 Current track loop: disabled"
            elif loops[ctx.guild.id] == "queue":
                loops_info = "🔁 Queue loop: enabled | 🔁 Current track loop: disabled"
            elif loops[ctx.guild.id] == "current track":
                loops_info = "🔁 Queue loop: disabled | 🔁 Current track loop: enabled"

            # sending the entire queue of 10 songs for each message
            print(content)
            for songs in content:
                if content.index(songs) == 0:
                    await ctx.send(embed=discord.Embed(
                        title="Current Queue",
                        description=songs,
                        color=0x515596)
                        .set_footer(text=loops_info))
                else:
                    await ctx.send(embed=discord.Embed(
                        description=songs,
                        color=0x515596)
                        .set_footer(text=loops_info))

    # loop command

    @commands.command()
    async def loop(self, ctx):
        global loops

        if ctx.voice_client is None:
            return await ctx.send("I am not playing any songs for you.")

        if ctx.author.voice is None:
            return await ctx.send(f"{ctx.author.mention}, You have to be connected to a voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("You are in the wrong channel.")

        # sending a message depending on whether is loop turned on or off
        if ctx.guild.id not in loops or loops[ctx.guild.id] == "none":
            await ctx.send("🔁 Queue loop enabled!")
            loops[ctx.guild.id] = "queue"
        elif loops[ctx.guild.id] == "queue":
            await ctx.send("🔁 Current track loop enabled!")
            loops[ctx.guild.id] = "current track"
        else:
            await ctx.send("❎ Loop disabled!")
            loops[ctx.guild.id] = "none"

    # Playlists

    @commands.command(aliases=['cp'])
    async def createplaylist(self, ctx, pname: str = None):
        if pname == None:
            return await ctx.send("You need to name the playlist")

        name = f"{ctx.author.id}"
        pname = pname

        with open('customplaylist.json') as f:
            data = json.load(f)
        if name in data:
            data[name][pname] = []
        else:
            plist = {pname: []}
            data[name] = plist
        with open('customplaylist.json', 'w') as f:
            json.dump(data, f, indent=4)
        return await ctx.send(embed=discord.Embed(title="Playlist created!", description="To add to the playlist use ?add [playlistname] [song/songurl]"))

    @commands.command()
    async def list(self, ctx, pname: str):
        with open('customplaylist.json') as f:
            data = json.load(f)
        if f"{ctx.author.id}" in data:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="You dont have any playlists!", description='Use ?createplaylist [name] to create one'))
        if pname in data[f"{ctx.author.id}"]:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="This playlist doesnt exist!", description='Use ?createplaylist [name] to create one'))
        if len(data[f"{ctx.author.id}"][pname]):
            for song in data[f"{ctx.author.id}"][pname]:
                await ctx.send(song)
        else:
            await ctx.send("List is empty use ?add [song]")

    @commands.command()
    async def add(self, ctx, pname: str, *,  song: str):
        with open('customplaylist.json') as f:
            data = json.load(f)
        if f"{ctx.author.id}" in data:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="You dont have any playlists!", description='Use ?createplaylist [name] to create one'))
        if pname in data[f"{ctx.author.id}"]:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="This playlist doesnt exist!", description='Use ?createplaylist [name] to create one'))
        data[f"{ctx.author.id}"][pname].append(song)
        await ctx.send(f"{song} Added to {pname}")
        with open('customplaylist.json', 'w') as f:
            json.dump(data, f, indent=4)

    @commands.command()
    async def playlist(self, ctx, pname: str):
        with open('customplaylist.json') as f:
            data = json.load(f)
        if f"{ctx.author.id}" in data:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="You dont have any playlists!", description='Use ?createplaylist [name] to create one'))
        if pname in data[f"{ctx.author.id}"]:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="This playlist doesnt exist!", description='Use ?createplaylist [name] to create one'))
        if len(data[f"{ctx.author.id}"][pname]):
            for song in data[f"{ctx.author.id}"][pname]:
                await playy(ctx, video=song)
        else:
            await ctx.send("List is empty use ?add [song]")

    @commands.command()
    async def pdel(self, ctx, pname: str):
        with open('customplaylist.json') as f:
            data = json.load(f)
        if f"{ctx.author.id}" in data:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="You dont have any playlists!", description='Use ?createplaylist [name] to create one'))
        if pname in data[f"{ctx.author.id}"]:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="This playlist doesnt exist!", description='Use ?createplaylist [name] to create one'))
        if len(data[f"{ctx.author.id}"][pname]):
            n = 1
            for song in data[f"{ctx.author.id}"][pname]:
                await ctx.send(f"{n}: {song}")
                n += 1
        else:
            await ctx.send("List is empty use ?add [song]")

        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author
        await ctx.send("Enter the number of the song you want to delete")
        index = await self.client.wait_for("message", check=wfcheck)
        index = index.content
        try:
            index = int(index)
            index = index-1
        except:
            await ctx.send("Index must be a number")
        try:
            rm = data[f"{ctx.author.id}"][pname][index]
            print(rm)
            data[f"{ctx.author.id}"][pname].remove(rm)
        except Exception as e:
            await ctx.send(e)
        with open('customplaylist.json', 'w') as f:
            json.dump(data, f, indent=4)

    # Text to speech

    @commands.command(aliases=['speak'])
    async def tts(self, ctx, *, text):
        text = str(text)

        language = 'en'

        output = gTTS(text=text, lang=language, slow=False)

        cd = os.getcwd()
        os.chdir("/home/runner/Why-Bot")
        name = ctx.author.id
        output.save(f"{name}.mp3")

        if ctx.author.voice is None:
            return await ctx.send(f"{ctx.author.mention}, You have to be connected to a voice channel.")

        channel = ctx.author.voice.channel

        if ctx.voice_client is None:  # if bot is not connected to a voice channel, connecting to a voice channel
            await channel.connect()
        else:  # else, just moving to ctx author voice channel
            await ctx.voice_client.move_to(channel)

        # self deaf
        await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)

        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(
            self.client.voice_clients, guild=guild)
        audio_source = discord.FFmpegPCMAudio(f'{name}.mp3')
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
        else:
            await ctx.send("Something is playling right now, Try using this command after its finished")
        audio = MP3(f"{name}.mp3")
        wait = int(audio.info.length)
        await asyncio.sleep(wait)
        os.remove(f'{name}.mp3')
        os.chdir(cd)


def setup(client):
    client.add_cog(Music(client))
