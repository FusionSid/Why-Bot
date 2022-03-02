import discord
from io import BytesIO
from discord.ext import commands
from easy_pil import Editor, Canvas, Font, load_image_async, Text
import os
from utils import plugin_enabled

async def generate_welcome_message(client, member, guild):
    data = await client.get_db()
    data = data[str(guild.id)]
    welcome_bg_color = data['welcome']["bg_color"]
    welcome_bg_image = data['welcome']["bg_image"]
    welcome_text_color = data['welcome']["text_color"]
    welcome_text_footer = data['welcome']["text_footer"]

    welcome_profile_url = "https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png"

    welcome_image = Editor(Canvas((900, 270)))

    if welcome_bg_color is None:
        welcome_bg_color = "#23272a"

    # Background Color
    welcome_image.rectangle(
        (0, 0), width=970, height=270, fill=welcome_bg_color)

    # Fonts to use with different size
    poppins_big = Font.poppins(variant="bold", size=50)
    poppins_mediam = Font.poppins(variant="bold", size=40)
    poppins_regular = Font.poppins(variant="regular", size=30)
    poppins_thin = Font.poppins(variant="regular", size=20)

    # Background
    if welcome_bg_image is not None:
        try:
            bg_img_url = await load_image_async(str(welcome_bg_image))
            bg_img = Editor(bg_img_url).resize((970, 270)).blur(amount=3)
            welcome_image.paste(bg_img, (0, 0))
        except Exception as err:
            print(err)

    card_left_shape = [(0, 0), (0, 270), (330, 270), (260, 0)]

    welcome_image.polygon(card_left_shape, "#2C2F33")
    # Profile Picture
    if member.avatar is not None:
        profile_image = await load_image_async(str(member.avatar.url))
    else:
        profile_image = await load_image_async(str(welcome_profile_url))
    profile = Editor(profile_image).resize((200, 200)).circle_image()
    welcome_image.paste(profile, (40, 35))

    # Text
    if welcome_text_color is None:
        welcome_text_color = "#FFFFFF"
    welcome_image.text((600, 35), "WELCOME", font=poppins_big, color=str(
        welcome_text_color), align="center")
    welcome_image.text((600, 85), str(member.name), font=poppins_regular, color=str(
        welcome_text_color), align="center")
    welcome_image.text((600, 135), "THANKS FOR JOINING", font=poppins_mediam, color=str(
        welcome_text_color), align="center")
    welcome_image.text((600, 175), str(member.guild.name), font=poppins_regular, color=str(
        welcome_text_color), align="center")
    if welcome_text_footer is None:
        welcome_text_footer = "Hope you enjoy your stay at this amazing server"
    welcome_image.text((620, 237), str(welcome_text_footer), font=poppins_thin, color=str(
        welcome_text_color), align="center",)

    d = BytesIO()
    d.seek(0)
    welcome_image.save(d, "PNG")
    d.seek(0)
    return d


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = await self.client.get_db()

        if data[str(member.guild.id)]['settings']['plugins']['Welcome'] == False:
            return
        file_path = await generate_welcome_message(self.client, member, member.guild)

        cha = data[str(member.guild.id)]["welcome_channel"]
        if cha is not None:
            channel = await self.client.fetch_channel(int(cha))
            # Send welcome message in server welcome channel
            await channel.send(content=member.mention, file=discord.File(file_path, "welcome.png"))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            await member.send(f"Goodbye {member.name}")
        except:
            pass
        data = await self.client.get_db()
        if data[str(member.guild.id)]['settings']['plugins']['Welcome'] == False:
            return
        cha = data[str(member.guild.id)]['welcome_channel']
        if cha is not None:
            cha.send(f"Goodbye: {member.name}")

    @commands.group()
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        file_path = await generate_welcome_message(self.client, ctx.author, ctx.guild)
        await ctx.send(file=discord.File(file_path, "welcome.png"), embed=discord.Embed(title="This is the image that will show as the welcome message", description=f"`{ctx.prefix}welcome textcolor`\n`{ctx.prefix}welcome image`\n`{ctx.prefix}welcome bgcolor`\n`{ctx.prefix}welcome text\n`", color=ctx.author.color))

    @welcome.command()
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def textcolor(self, ctx, color: str):
        if color.lower() == "none":
            color = None
        data = await self.client.get_db()
        data[str(ctx.guild.id)]['welcome']["text_color"] = color

        await self.client.update_db(data)

        await ctx.send(embed=discord.Embed(title="Welcome", description=f"Welcome text color set!\nUse `{ctx.prefix}welcome` with no subcommand to see the welcome message that will display", color=ctx.author.color))

    @welcome.command()
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def bgcolor(self, ctx, color: str):
        if color.lower() == "none":
            color = None
        data = await self.client.get_db()
        data[str(ctx.guild.id)]['welcome']["bg_color"] = color

        await self.client.update_db(data)

        await ctx.send(embed=discord.Embed(title="Welcome", description=f"Welcome background color set!\nUse `{ctx.prefix}welcome` with no subcommand to see the welcome message that will display", color=ctx.author.color))

    @welcome.command()
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def text(self, ctx, *, text):
        if len(text) > 55:
            return await ctx.send("Text is to big")
        if text.lower() == "none":
            text = None
        data = await self.client.get_db()
        data[str(ctx.guild.id)]['welcome']["text_footer"] = text

        await self.client.update_db(data)
        await ctx.send(embed=discord.Embed(title="Welcome", description=f"Welcome test set!\nUse `{ctx.prefix}welcome` with no subcommand to see the welcome message that will display", color=ctx.author.color))

    @welcome.command()
    @commands.check(plugin_enabled)
    @commands.has_permissions(administrator=True)
    async def image(self, ctx, url: str):
        if url.lower() == "none":
            url = None
        data = await self.client.get_db()
        data[str(ctx.guild.id)]['welcome']["bg_image"] = url

        await self.client.update_db(data)

        await ctx.send(embed=discord.Embed(title="Welcome", description=f"Welcome background image set!\nUse `{ctx.prefix}welcome` with no subcommand to see the welcome message that will display", color=ctx.author.color))


def setup(client):
    client.add_cog(Welcome(client))
