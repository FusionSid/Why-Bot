import discord
import asyncio
from discord.ext import commands
import sqlite3
from utils import plugin_enabled


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        conn = sqlite3.connect('./database/voice.db')
        c = conn.cursor()
        guildID = member.guild.id
        c.execute("SELECT voiceChannelID FROM guild WHERE guildID = ?", (guildID,))
        voice=c.fetchone()
        if voice is None:
            pass
        else:
            voiceID = voice[0]
            try:
                if after.channel.id == voiceID:
                    c.execute("SELECT * FROM voiceChannel WHERE userID = ?", (member.id,))
                    cooldown=c.fetchone()
                    if cooldown is None:
                        pass
                    elif member.author.id == 624076054969188363:
                      pass
                    else:
                        await member.send("Creating channels too quickly you've been put on a 15 second cooldown!")
                        await asyncio.sleep(15)
                    c.execute("SELECT voiceCategoryID FROM guild WHERE guildID = ?", (guildID,))
                    voice=c.fetchone()
                    c.execute("SELECT channelName, channelLimit FROM userSettings WHERE userID = ?", (member.id,))
                    setting=c.fetchone()
                    c.execute("SELECT channelLimit FROM guildSettings WHERE guildID = ?", (guildID,))
                    guildSetting=c.fetchone()
                    if setting is None:
                        name = f"{member.name}'s channel"
                        if guildSetting is None:
                            limit = 0
                        else:
                            limit = guildSetting[0]
                    else:
                        if guildSetting is None:
                            name = setting[0]
                            limit = setting[1]
                        elif guildSetting is not None and setting[1] == 0:
                            name = setting[0]
                            limit = guildSetting[0]
                        else:
                            name = setting[0]
                            limit = setting[1]
                    categoryID = voice[0]
                    id = member.id
                    category = self.bot.get_channel(categoryID)
                    channel2 = await member.guild.create_voice_channel(name,category=category)
                    channelID = channel2.id
                    await member.move_to(channel2)
                    await channel2.set_permissions(self.bot.user, connect=True,read_messages=True)
                    await channel2.edit(name= name, user_limit = limit)
                    c.execute("INSERT INTO voiceChannel VALUES (?, ?)", (id,channelID))
                    conn.commit()
                    def check(a,b,c):
                        return len(channel2.members) == 0
                    await self.bot.wait_for('voice_state_update', check=check)
                    await channel2.delete()
                    await asyncio.sleep(3)
                    c.execute('DELETE FROM voiceChannel WHERE userID=?', (id,))
            except:
                pass
        conn.commit()
        conn.close()

    @commands.group( help="These commands are used to set the custom VC for your server. The custom vc is a voice channel which upon joining creates a new temporary discord Voice Channel and deletes said channel when all members leave the channel.\nYou can use voice set to set the channel and voice setlimit to set the limit. ", extras={"category":"Voice"}, usage="voice [set/setlimit]", description="Sets the custom vc for you voice channel")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator  = True)
    async def voice(self, ctx):
        if ctx.invoked_subcommand is not None:
            pass
        else:
            await ctx.send(f"`{ctx.prefix}voice set` To set the channel\n`{ctx.prefix}voice setlimit` To set the limit")

    @voice.command(extras={"category":"Voice"}, usage="voice setup", help="This command is used to set up the Custom Vc for your server.\nThis channel, upon joining will create a temporary vc with your name on it and once everyone leave that channel, it will be deleted", description="Sets the custom vc for the channel")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator = True)
    async def setup(self, ctx):
        conn = sqlite3.connect('./database/voice.db')
        c = conn.cursor()
        guildID = ctx.guild.id
        id = ctx.author.id
        def check(m):
            return m.author.id == ctx.author.id
        await ctx.channel.send("**You have 60 seconds to answer each question!**")
        await ctx.channel.send(f"**Enter the name of the category you wish to create the channels in:(e.g Voice Channels)**")
        try:
            category = await self.bot.wait_for('message', check=check, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.channel.send('Took too long to answer!')
        else:
            new_cat = await ctx.guild.create_category_channel(category.content)
            await ctx.channel.send('**Enter the name of the voice channel: (e.g Join To Create)**')
            try:
                channel = await self.bot.wait_for('message', check=check, timeout = 60.0)
            except asyncio.TimeoutError:
                await ctx.channel.send('Took too long to answer!')
            else:
                try:
                    channel = await ctx.guild.create_voice_channel(channel.content, category=new_cat)
                    c.execute("SELECT * FROM guild WHERE guildID = ? AND ownerID=?", (guildID, id))
                    voice=c.fetchone()
                    if voice is None:
                        c.execute ("INSERT INTO guild VALUES (?, ?, ?, ?)",(guildID,id,channel.id,new_cat.id))
                    else:
                        c.execute ("UPDATE guild SET guildID = ?, ownerID = ?, voiceChannelID = ?, voiceCategoryID = ? WHERE guildID = ?",(guildID,id,channel.id,new_cat.id, guildID))
                    await ctx.channel.send("**You are all setup and ready to go!**")
                except:
                    await ctx.channel.send(f"You didn't enter the names properly.\nUse `{ctx.prefix}voice setup` again!")
        conn.commit()
        conn.close()

    @voice.command(extras={"category":"Voice"}, usage="voice setlimit", help="This command sets the limit for the custom vc.", description="Sets limit for custom vc")
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator = True)
    async def setlimit(self, ctx, num):
        conn = sqlite3.connect('./database/voice.db')
        c = conn.cursor()
        c.execute("SELECT * FROM guildSettings WHERE guildID = ?", (ctx.guild.id,))
        voice=c.fetchone()
        if voice is None:
            c.execute("INSERT INTO guildSettings VALUES (?, ?, ?)", (ctx.guild.id,f"{ctx.author.name}'s channel",num))
        else:
            c.execute("UPDATE guildSettings SET channelLimit = ? WHERE guildID = ?", (num, ctx.guild.id))
        await ctx.send("You have changed the default channel limit for your server!")
        conn.commit()
        conn.close()

    @setup.error
    async def info_error(self, ctx, error):
        print(error)

def setup(bot):
    bot.add_cog(Voice(bot))