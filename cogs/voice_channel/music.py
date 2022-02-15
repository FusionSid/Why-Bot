import discord
import datetime
import importlib
import pyttsx3
from utils.checks import plugin_enabled
import shutil
from discord import interactions
import wget
import requests
import asyncio
from discord.ext import commands
import youtube_dl
from youtubesearchpython import VideosSearch
from multiprocessing import Pool
import os
import discord.voice_client
import json
from gtts import gTTS
from mutagen.mp3 import MP3
from discord.ui import Button, View
from discord import Option
import random

cookies = "./database/cookies.txt"
ffmpeg_options = {  # ffmpeg options
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}


loops = {}  # for +loop command
queues = {}  # for queues
now_playing_pos = {}  # to display the current song in +queue command correctly
all_queues_info = {}  # all queue info, for +queue command

# function, which splitting the queue into queues of 10 songs

class MusicView(View):
    def __init__(self, ctx, client):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.em = discord.Embed(title="Music", color=ctx.author.color)
        self.client = client

    @discord.ui.button(style=discord.ButtonStyle.green, emoji="▶️", custom_id="button")
    
    async def play(self, button, interaction):
        if self.ctx.voice_client is None:
            self.em.description = "I am not playing any songs for you."

        if self.ctx.author.voice is None:
            self.em.description = f"{self.ctx.author.mention}, You have to be connected to a voice channel."

        if self.ctx.author.voice.channel.id != self.ctx.voice_client.channel.id:
            self.em.description = "You are in the wrong channel."

        self.ctx.voice_client.resume()  # resume music
        self.em.description = "Successfully resumed."

        await interaction.response.edit_message(embed=self.em)
        
    @discord.ui.button(style=discord.ButtonStyle.red, emoji="⏸️", custom_id="button2")
    async def pause(self, button, interaction):
        if self.ctx.voice_client is None:
            self.em.description = "I am not playing any songs for you."

        if self.ctx.author.voice is None:
            self.em.description = f"{self.ctx.author.mention}, You have to be connected to a voice channel."

        if self.ctx.author.voice.channel.id != self.ctx.voice_client.channel.id:
            self.em.description = "You are in the wrong channel."

        self.ctx.voice_client.pause()  # stopping a music
        self.em.description = "Successfully paused."

        await interaction.response.edit_message(embed=self.em)

    @discord.ui.button(style=discord.ButtonStyle.green, emoji="⏭️", custom_id="button3")
    async def skip(self, button, interaction):
        if self.ctx.voice_client is None:
            self.em.description = "I am not playing any songs for you."

        if self.ctx.author.voice is None:
            self.em.description = f"{self.ctx.author.mention}, You have to be connected to a voice channel."

        if self.ctx.author.voice.channel.id != self.ctx.voice_client.channel.id:
            self.em.description = "You are in the wrong channel."

        self.ctx.voice_client.stop()  # skipping current track
        self.em.description = "Successfully skipped."
        await interaction.response.edit_message(embed=self.em)

    @discord.ui.button(style=discord.ButtonStyle.grey, label="Leave VC", custom_id="button4", row=2)
    async def leave(self, button, interaction):
        if self.ctx.voice_client is None:
            self.em.description = "I am not playing any songs for you."

        if self.ctx.author.voice is None:
            self.em.description = f"{self.ctx.author.mention}, You have to be connected to a voice channel."

        if self.ctx.author.voice.channel.id != self.ctx.voice_client.channel.id:
            self.em.description = "You are in the wrong channel."

        await self.ctx.voice_client.disconnect()  # leaving a voice channel
        self.em.description = "Successfully disconnected."
        await interaction.response.edit_message(embed=self.em)
    
    @discord.ui.button(style=discord.ButtonStyle.grey, label="Join VC", custom_id="button5", row=2)
    async def join(self, button, interaction):
        if self.ctx.author.voice is None:
            self.em.description = f"{self.ctx.author.mention}, You have to be connected to a voice channel."

        channel = self.ctx.author.voice.channel

        if self.ctx.voice_client is None:  # if bot is not connected to a voice channel, connecting to a voice channel
            await channel.connect()
        else:  # else, just moving to ctx author voice channel
            await self.ctx.voice_client.move_to(channel)

        # self deaf
        await self.ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)

        self.em.description = f"Successfully joined to `{channel}`"
        await interaction.response.edit_message(embed=self.em)


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
            except discord.errors.ClientException as e: 
                print("ClientException")

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
        return youtube_dl.YoutubeDL({"format": "bestaudio" }).extract_info(url, download=False)
    # if there is an error, changing format
    except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError):
        return youtube_dl.YoutubeDL({"format": "95"}).extract_info(url, download=False)


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
    except Exception as e:
        print(e)

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    # join command
    @commands.command(aliases=["j"], help="Running this command lets the bot join the discord VC you are in.", extras={"category":"Music"}, usage="join", description="Bot joins VC")
    @commands.check(plugin_enabled)
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

    @commands.command(aliases=["p"], help="This command is used to play songs. You can type in the name, yt url or yt playlist url and the bot will play the song.", extras={"category":"Music"}, usage="play [name/url]", description="Play a song")
    @commands.check(plugin_enabled)
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
            print("ClientException")

        # Adding embed, depending on the queue
        if len(queues[ctx.guild.id]) != 1:
            embed = discord.Embed(
                title="Queue",
                description=f"🔎 Searching for `{video_search}`\n\n" +
                f"""✅ [{video_title}]({video_url}) - successfully added to queue.""",
                color=0x515596)
            embed.timestamp = datetime.datetime.utcnow()
        else:
            embed = discord.Embed(
                title="Now playing",
                description=f"✅ Successfully joined to `{channel}`\n\n" +
                f"🔎 Searching for `{video_search}`\n\n" +
                f"""▶️ Now playing - [{video_title}]({video_url})""",
                color=0x515596)
            embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)

    # skip command

    @commands.command(aliases=["s"], help="This command is used to skip the song that is playing", extras={"category":"Music"}, usage="skip", description="Skips the playing song")
    @commands.check(plugin_enabled)
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

    @commands.command(aliases=["l", "disconnect", "d"], help="This command is used to disconnect/make the bot leave the VC.", extras={"category":"Music"}, usage="leave", description="Leave vc")
    @commands.check(plugin_enabled)
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

    @commands.command(aliases=["stop"], help="This command is used to pause the current plauing song", extras={"category":"Music"}, usage="pause", description="Pause song")
    @commands.check(plugin_enabled)
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

    @commands.command(aliases=["continue", "unpause"], help="This command is used to resume the currently playing song", extras={"category":"Music"}, usage="resume", description="Resume the paused song")
    @commands.check(plugin_enabled)
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

    @commands.command(aliases=["q"], help="This command is used to dispay all the songs in the queue", extras={"category":"Music"}, usage="queue", description="Show queue")
    @commands.check(plugin_enabled)
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

    @commands.command( help="This command is used to loop the queue/song", extras={"category":"Music"}, usage="loop", description="Loop queue/song")
    @commands.check(plugin_enabled)
    async def loop(self, ctx):
        global loops
        loops[ctx.guild.id] = "none"

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


    @commands.command(aliases=['cp'], help="This command is used to create playlists", extras={"category":"Music"}, usage="createplaylist [playlist name]", description="Create a playlist")
    @commands.check(plugin_enabled)
    async def createplaylist(self, ctx, pname: str = None):
        if pname == None:
            return await ctx.send("You need to name the playlist")

        name = f"{ctx.author.id}"
        pname = pname

        with open('./database/playlists.json') as f:
            data = json.load(f)
        if name in data:
            data[name][pname] = []
        else:
            plist = {pname: []}
            data[name] = plist
        with open('./database/playlists.json', 'w') as f:
            json.dump(data, f, indent=4)
        return await ctx.send(embed=discord.Embed(title=f"Playlist `{pname}` created!", description=f"To add to the playlist use {ctx.prefix}padd [playlistname] [song/songurl]", color=ctx.author.color))

    @commands.command(help="This command is used to list all the songs in a playlist", extras={"category":"Music"}, usage="plist [playlist name]", description="Displays all the songs in a playlist")
    @commands.check(plugin_enabled)
    async def plist(self, ctx, pname: str):
        with open('./database/playlists.json') as f:
            data = json.load(f)
        if f"{ctx.author.id}" in data:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="You dont have any playlists!", description=f'Use {ctx.prefix}createplaylist [name] to create one', color=ctx.author.color))
        if pname in data[f"{ctx.author.id}"]:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="This playlist doesnt exist!", description=f'Use {ctx.prefix}createplaylist [name] to create one', color=ctx.author.color))
        em = discord.Embed(title=f"Playlist: {pname}", description="Songs:")
        em.timestamp = datetime.datetime.utcnow()
        if len(data[f"{ctx.author.id}"][pname]):
            c = 1
            for song in data[f"{ctx.author.id}"][pname]:
                em.add_field(name=f"{c}. {song}", value="** **", inline=False)
                c += 1
            await ctx.send(embed=em)
        else:
            await ctx.send(f"List is empty use {ctx.prefix}padd {pname} [songname/url]")

    @commands.command(help="Lets you add a song to a playlist", extras={"category":"Music"}, usage="padd [playlist name] [song/songurl]", description="Add song to a playlist")
    @commands.check(plugin_enabled)
    async def padd(self, ctx, pname: str, *,  song: str):
        with open('./database/playlists.json') as f:
            data = json.load(f)
        if f"{ctx.author.id}" in data:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="You dont have any playlists!", description=f'Use {ctx.prefix}createplaylist [name] to create one', color=ctx.author.color))
        if pname in data[f"{ctx.author.id}"]:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="This playlist doesnt exist!", description=f'Use {ctx.prefix}createplaylist [name] to create one', color=ctx.author.color))
        data[f"{ctx.author.id}"][pname].append(song)
        await ctx.send(f"{song} Added to {pname}")
        with open('./database/playlists.json', 'w') as f:
            json.dump(data, f, indent=4)

    @commands.command( help="This command is used to play the songs in a playlist. The command works by adding all the songs in the playlist to queue.\nplease dont kick the bot from the vc while the command is running", extras={"category":"Music"}, usage="playlist [playlist name]", description="Play a playlist")
    @commands.check(plugin_enabled)
    async def playlist(self, ctx, pname: str):
        with open('./database/playlists.json') as f:
            data = json.load(f)
        if f"{ctx.author.id}" in data:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="You dont have any playlists!", description=f'Use {ctx.prefix}createplaylist [name] to create one', color=ctx.author.color))
        if pname in data[f"{ctx.author.id}"]:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="This playlist doesnt exist!", description=f'Use {ctx.prefix}createplaylist [name] to create one', color=ctx.author.color))
        await ctx.send(embed=discord.Embed(title=f"Playing playlist: {pname}", description=f"Songs are being added to queue"))
        if len(data[f"{ctx.author.id}"][pname]):
            for song in data[f"{ctx.author.id}"][pname]:
                try:
                  await playy(ctx, video=song)
                except Exception as e:
                  print(e)
                await asyncio.sleep(1)
        else:
            await ctx.send(f"List is empty use {ctx.prefix}add [song]")

    @commands.command(help="This command is used to play the songs in a playlist on shuffle. The command works by adding all the songs in the playlist to queue in a random order.\nplease dont kick the bot from the vc while the command is running", extras={"category":"Music"}, usage="shuffleplaylist [playlist name]", description="Shuffle a playlist")
    @commands.check(plugin_enabled)
    async def shuffleplaylist(self, ctx, pname: str):
        with open('./database/playlists.json') as f:
            data = json.load(f)
        if f"{ctx.author.id}" in data:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="You dont have any playlists!", description=f'Use {ctx.prefix}createplaylist [name] to create one', color=ctx.author.color))
        if pname in data[f"{ctx.author.id}"]:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="This playlist doesnt exist!", description=f'Use {ctx.prefix}createplaylist [name] to create one', color=ctx.author.color))
        await ctx.send(embed=discord.Embed(title="Playing Playlist", description=f"Songs are being added to queue in random order"))
        if len(data[f"{ctx.author.id}"][pname]):
            slist = data[f"{ctx.author.id}"][pname]
            def myfunction():
              return 0.1
            random.shuffle(slist, myfunction)
            print(slist)
            for song in slist:
                try:
                  await playy(ctx, video=song)
                except Exception as e:
                  print(e)
                await asyncio.sleep(1)
        else:
            await ctx.send(f"List is empty use {ctx.prefix}add [song]")

    @commands.command( help="This command is used to delete songs from a playlist ", extras={"category":"Music"}, usage="pdel [playlist name]", description="Delete song from a playlist")
    @commands.check(plugin_enabled)
    async def pdel(self, ctx, pname: str):
        with open('./database/playlists.json') as f:
            data = json.load(f)
        if f"{ctx.author.id}" in data:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="You dont have any playlists!", description=f'Use {ctx.prefix}createplaylist [name] to create one', color=ctx.author.color))
        if pname in data[f"{ctx.author.id}"]:
            pass
        else:
            return await ctx.send(embed=discord.Embed(title="This playlist doesnt exist!", description=f'Use {ctx.prefix}createplaylist [name] to create one', color=ctx.author.color))
        if len(data[f"{ctx.author.id}"][pname]):
            n = 1
            for song in data[f"{ctx.author.id}"][pname]:
                await ctx.send(f"{n}: {song}")
                n += 1
        else:
            await ctx.send(f"List is empty use {ctx.prefix}add [song]")

        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author
        await ctx.send("Enter the number of the song you want to delete")
        index = await self.client.wait_for("message", check=wfcheck, timeout=300)
        index = index.content
        try:
            index = int(index)
            index = index-1
        except Exception:
            await ctx.send("Index must be a number")
        try:
            rm = data[f"{ctx.author.id}"][pname][index]
            print(rm)
            data[f"{ctx.author.id}"][pname].remove(rm)
        except Exception as e:
            print(e)
            return
        with open('./database/playlists.json', 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.send("Song deleted from playlist.")

    # Text to speech

    @commands.command(aliases=['speak'], help="This command is used to play text in vc. You type text and the bot will text to speech the text in your vc", extras={"category":"Music"}, usage="tts [text]", description="Text to speech")
    @commands.check(plugin_enabled)
    async def tts(self, ctx, *, text):
        text = str(text)

        language = 'en'

        output = gTTS(text=text, lang=language, slow=False)

        name = ctx.author.id
        output.save(f"./tempstorage/{name}.mp3")

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
        audio_source = discord.FFmpegPCMAudio(f'./tempstorage/{name}.mp3')
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
        else:
            await ctx.send("Something is playling right now, Try using this command after its finished")
        audio = MP3(f"./tempstorage/{name}.mp3")
        wait = int(audio.info.length)
        await asyncio.sleep(wait+5)
        os.remove(f'./tempstorage/{name}.mp3')
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if not member.id == self.client.user.id:
            return

        elif before.channel is None:
            voice = after.channel.guild.voice_client
            while voice.is_playing(): #Checks if voice is playing
                await asyncio.sleep(1) #While it's playing it sleeps for 1 second
        else:
            await asyncio.sleep(300) #If it's not playing it waits 15 seconds
            while voice.is_playing(): #and checks once again if the bot is not playing
                break #if it's playing it breaks
            else:
                await voice.disconnect() #if not it disconnects

    @commands.command(help="This command is used to play an mp3 file ", extras={"category":"Music"}, usage="mp3 [attach mp3 file]", description="Play an mp3 file")
    @commands.check(plugin_enabled)
    async def mp3(self, ctx):

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
        if len(ctx.message.attachments) == 0:
            return await ctx.send("You must provide an mp3 file for this to work")
        attachment_url = ctx.message.attachments[0].url
        if attachment_url.endswith(".mp3"):
            pass
        else:
            return await ctx.send("Must be an mp3 file")
        r = requests.get(attachment_url, stream=True)
        filename=f"./tempstorage/{ctx.author.id}.mp3"
        if r.status_code == 200:
            with open(f"./tempstorage/{ctx.author.id}.mp3", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        audio_source = discord.FFmpegPCMAudio(filename)
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
        else:
            await ctx.send("Something is playling right now, Try using this command after its finished")
        audio = MP3(filename)
        wait = int(audio.info.length)
        await asyncio.sleep(wait+5)
        os.remove(filename)
    
    @commands.command(help="This command is used to make a small button dashboard for the music", extras={"category":"Music"}, usage="music", description="Small music button dashboard")
    @commands.check(plugin_enabled)
    async def music(self, ctx):
        em = discord.Embed(title="Music", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        view= MusicView(ctx, self.client)
        message = await ctx.send(embed=em, view=view)
        res = await view.wait()
        if res:
          for i in view.children:
            i.disabled = True
          return await message.edit(view=view)
          
def setup(client):
    client.add_cog(Music(client))
