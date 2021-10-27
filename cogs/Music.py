import discord
from discord.ext import commands
import youtube_dl
from youtubesearchpython import VideosSearch
from multiprocessing import Pool
import os, platform
import discord.voice_client
import nacl

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
				queues[guild_id].append({"url": track["url"], "src_url": track["src_url"]})
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
	except youtube_dl.utils.ExtractorError and youtube_dl.utils.DownloadError:  # if there is an error, changing format
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

    await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)  # self deaf

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
        queues[ctx.guild.id].append({"url": video_url, "src_url": src_video_url})
        all_queues_info[ctx.guild.id].append({"name": video_title, "url": video_url, "src_url": src_video_url})
      else:
        queues[ctx.guild.id] = [{"url": video_url, "src_url": src_video_url}]
        now_playing_pos[ctx.guild.id] = 0
        all_queues_info[ctx.guild.id] = [{"name": video_title, "url": video_url, "src_url": src_video_url}]

    else:  # else queueing playlist
      src_video_url = information["entries"][0]["url"]
      video_title = information["title"]

      # queuing first song
      if ctx.guild.id in queues:
        queues[ctx.guild.id].append({"url": video_url, "src_url": src_video_url})
        all_queues_info[ctx.guild.id].append(
          {"name": information["entries"][0]["title"], "url": video_url, "src_url": src_video_url})
      else:
        queues[ctx.guild.id] = [{"url": video_url, "src_url": src_video_url}]
        now_playing_pos[ctx.guild.id] = 0
        all_queues_info[ctx.guild.id] = [
          {"name": information["entries"][0]["title"], "url": video_url, "src_url": src_video_url}]

      # queuing another songs
      for v in information["entries"]:
        if information["entries"].index(v) != 0:
          queues[ctx.guild.id].append({"url": video_url, "src_url": v["url"]})
          all_queues_info[ctx.guild.id].append({"name": v["title"], "url": video_url, "src_url": src_video_url})

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

    await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)  # self deaf

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

    await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)  # self deaf

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
        queues[ctx.guild.id].append({"url": video_url, "src_url": src_video_url})
        all_queues_info[ctx.guild.id].append({"name": video_title, "url": video_url, "src_url": src_video_url})
      else:
        queues[ctx.guild.id] = [{"url": video_url, "src_url": src_video_url}]
        now_playing_pos[ctx.guild.id] = 0
        all_queues_info[ctx.guild.id] = [{"name": video_title, "url": video_url, "src_url": src_video_url}]

    else:  # else queueing playlist
      src_video_url = information["entries"][0]["url"]
      video_title = information["title"]

      # queuing first song
      if ctx.guild.id in queues:
        queues[ctx.guild.id].append({"url": video_url, "src_url": src_video_url})
        all_queues_info[ctx.guild.id].append(
          {"name": information["entries"][0]["title"], "url": video_url, "src_url": src_video_url})
      else:
        queues[ctx.guild.id] = [{"url": video_url, "src_url": src_video_url}]
        now_playing_pos[ctx.guild.id] = 0
        all_queues_info[ctx.guild.id] = [
          {"name": information["entries"][0]["title"], "url": video_url, "src_url": src_video_url}]

      # queuing another songs
      for v in information["entries"]:
        if information["entries"].index(v) != 0:
          queues[ctx.guild.id].append({"url": video_url, "src_url": v["url"]})
          all_queues_info[ctx.guild.id].append({"name": v["title"], "url": video_url, "src_url": src_video_url})

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
        queue_info = split(all_queues_info[ctx.guild.id], 10)  # splitting the queue into queues of 10 songs
      else:
        return await ctx.send(embed=discord.Embed(
          title="Current Queue",
          description="Your current queue is empty!",
          color=0x515596)
        )
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

  
  @commands.command()
  async def playlist(self, ctx, name:str):
    with open('customplaylist.json') as f:
      pass

def setup(client):
    client.add_cog(Music(client))



