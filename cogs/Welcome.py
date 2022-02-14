import discord
from discord.ext import commands
from easy_pil import Editor, Canvas, Font, load_image, Text
import os
import json

async def memberjoin(client, member):
    with open("./database/db.json") as f:
      data = json.load(f)
    for i in data:
      if i['guild_id'] == member.guild.id:
        welcome_bg_color = i['welcome']["bg_color"]
        welcome_bg_image = i['welcome']["bg_image"]
        welcome_text_color = i['welcome']["text_color"]
        welcome_text_footer = i['welcome']["text_footer"]


    welcome_profile_url = "https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png"

    welcome_image = Editor(Canvas((900, 270)))

    if welcome_bg_color is None:
        welcome_bg_color = "#23272a"

    # Background Color    
    welcome_image.rectangle((0, 0), width=970, height=270, fill=welcome_bg_color)

    # Fonts to use with different size
    poppins_big = Font.poppins(variant="bold", size=50)
    poppins_mediam = Font.poppins(variant="bold", size=40)
    poppins_regular = Font.poppins(variant="regular", size=30)
    poppins_thin = Font.poppins(variant="regular", size=20)

    # Background
    if welcome_bg_image is not None:
        try:
            bg_img_url = load_image(str(welcome_bg_image))
            bg_img = Editor(bg_img_url).resize((970, 270))
            welcome_image.paste(bg_img, (0, 0))
        except Exception as err:
            print(err)


    card_left_shape = [(0, 0), (0, 270), (330, 270), (260, 0)]
    welcome_image.polygon(card_left_shape, "#2C2F33")

    # Profile Picture
    if member.avatar is not None:
        profile_image = load_image(str(member.avatar.url))
    else:
        profile_image = load_image(str(welcome_profile_url))
    profile = Editor(profile_image).resize((200, 200)).circle_image()
    welcome_image.paste(profile, (40, 35))


    # Text
    if welcome_text_color is None:
        welcome_text_color = "#FFFFFF"
    welcome_image.text((600, 35), "WELCOME", font=poppins_big, color=str(welcome_text_color), align="center")
    welcome_image.text((600, 85), str(member.name), font=poppins_regular, color=str(welcome_text_color), align="center")
    welcome_image.text((600, 135), "THANKS FOR JOINING", font=poppins_mediam, color=str(welcome_text_color), align="center")
    welcome_image.text((600, 175), str(member.guild.name), font=poppins_regular, color=str(welcome_text_color), align="center")
    if welcome_text_footer is None:
      welcome_text_footer = "Hope you enjoy your stay at this amazing server"
    welcome_image.text((620, 237),str(welcome_text_footer),font=poppins_thin,color=str(welcome_text_color),align="center",)


    welcome_image.save(f"./tempstorage/welcome{member.id}.png")


    with open(f"./database/db.json") as f:
        # Open setup file and check if there is a welcome channel
        data = json.load(f)
    for i in data:
        if i["guild_id"] == member.guild.id:
            cha = i["welcome_channel"]
    if cha == None:
        try:
          # await member.send(file=discord.File(f"./tempstorage/welcome{member.id}.png"))
          pass
        except:
          pass
    else:
        channel = await client.fetch_channel(int(cha))
        # Send welcome message in server welcome channel
        await channel.send(content=member.mention, file=discord.File(f"./tempstorage/welcome{member.id}.png"))
    
    os.remove(f"./tempstorage/welcome{member.id}.png")

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("./database/db.json") as f:
          data = json.load(f)
        for i in data:
          if i["guild_id"] == member.guild.id:
            if i['settings']['plugins']['Welcome'] == False:
              return
            else:
              pass
        await memberjoin(self.client, member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
      try:
        await member.send(f"Goodbye {member.name}")
      except:
        pass
      with open("./database/db.json") as f:
        data = json.load(f)
      for i in data:
        if i["guild_id"] == member.guild.id:
          if i['settings']['plugins']['Welcome'] == False:
            return
          else:
            pass
      with open(f"./database/db.json") as f:
        data = json.load(f)
      for i in data:
          if i["guild_id"] == member.guild.id:
              cha = i["welcome_channel"]
      if cha == None:
        pass
      else:
        cha.send(f"Goodbye: {member.name}")

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
      if ctx.invoked_subcommand is None:
        member = ctx.author
        with open("./database/db.json") as f:
          data = json.load(f)
        for i in data:
          if i['guild_id'] == member.guild.id:
            welcome_bg_color = i['welcome']["bg_color"]
            welcome_bg_image = i['welcome']["bg_image"]
            welcome_text_color = i['welcome']["text_color"]
            welcome_text_footer = i['welcome']["text_footer"]


        welcome_profile_url = "https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png"
        
        welcome_image = Editor(Canvas((900, 270)))

        if welcome_bg_color is None:
            welcome_bg_color = "#23272a"

        # Background Color    
        welcome_image.rectangle((0, 0), width=970, height=270, fill=welcome_bg_color)


        # Fonts to use with different size
        poppins_big = Font.poppins(variant="bold", size=50)
        poppins_mediam = Font.poppins(variant="bold", size=40)
        poppins_regular = Font.poppins(variant="regular", size=30)
        poppins_thin = Font.poppins(variant="regular", size=20)


        # Background
        if welcome_bg_image is not None:
            try:
                bg_img_url = load_image(str(welcome_bg_image))
                bg_img = Editor(bg_img_url).resize((970, 270)).blur(amount=3)
                welcome_image.paste(bg_img, (0, 0))
            except Exception as err:
                print(err)

        card_left_shape = [(0, 0), (0, 270), (330, 270), (260, 0)]

        welcome_image.polygon(card_left_shape, "#2C2F33")
        # Profile Picture
        if member.avatar is not None:
            profile_image = load_image(str(member.avatar.url))
        else:
            profile_image = load_image(str(welcome_profile_url))
        profile = Editor(profile_image).resize((200, 200)).circle_image()
        welcome_image.paste(profile, (40, 35))


        # Text
        if welcome_text_color is None:
            welcome_text_color = "#FFFFFF"
        welcome_image.text((600, 35), "WELCOME", font=poppins_big, color=str(welcome_text_color), align="center")
        welcome_image.text((600, 85), str(member.name), font=poppins_regular, color=str(welcome_text_color), align="center")
        welcome_image.text((600, 135), "THANKS FOR JOINING", font=poppins_mediam, color=str(welcome_text_color), align="center")
        welcome_image.text((600, 175), str(member.guild.name), font=poppins_regular, color=str(welcome_text_color), align="center")
        if welcome_text_footer is None:
          welcome_text_footer = "Hope you enjoy your stay at this amazing server"
        welcome_image.text((620, 237),str(welcome_text_footer),font=poppins_thin,color=str(welcome_text_color),align="center",)

  
        welcome_image.save(f"./tempstorage/welcome{member.id}.png")
        await ctx.send(file=discord.File(f"./tempstorage/welcome{member.id}.png"), embed=discord.Embed(title="This is the image that will show as the welcome message",description=f"`{ctx.prefix}welcome textcolor`\n`{ctx.prefix}welcome image`\n`{ctx.prefix}welcome bgcolor`\n`{ctx.prefix}welcome text\n`", color=ctx.author.color))
        os.remove(f"./tempstorage/welcome{member.id}.png")
        
    

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def textcolor(self, ctx, color:str):
      if color.lower() == "none":
        color = None
      with open("./database/db.json") as f:
          data = json.load(f)
      for i in data:
        if i['guild_id'] == ctx.author.guild.id:
          i['welcome']["text_color"] = color
        
      with open("./database/db.json","w") as f:
        json.dump(data, f, indent=4)
      
      await ctx.send(embed=discord.Embed(title="Welcome", description=f"Welcome text color set!\nUse `{ctx.prefix}welcome` with no subcommand to see the welcome message that will display", color=ctx.author.color))
      
    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def bgcolor(self, ctx, color:str):
      if color.lower() == "none":
        color = None
      with open("./database/db.json") as f:
          data = json.load(f)
      for i in data:
        if i['guild_id'] == ctx.author.guild.id:
          i['welcome']["bg_color"] = color
        
      with open("./database/db.json","w") as f:
        json.dump(data, f, indent=4)

      await ctx.send(embed=discord.Embed(title="Welcome", description=f"Welcome background color set!\nUse `{ctx.prefix}welcome` with no subcommand to see the welcome message that will display", color=ctx.author.color))


    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def text(self, ctx, *, text):
      if len(text) > 55:
        return await ctx.send("Text is to big")
      if text.lower() == "none":
        text = None
      with open("./database/db.json") as f:
          data = json.load(f)
      for i in data:
        if i['guild_id'] == ctx.author.guild.id:
          i['welcome']["text_footer"] = text
        
      with open("./database/db.json","w") as f:
        json.dump(data, f, indent=4)
      await ctx.send(embed=discord.Embed(title="Welcome", description=f"Welcome test set!\nUse `{ctx.prefix}welcome` with no subcommand to see the welcome message that will display", color=ctx.author.color))


    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def image(self, ctx, url:str):
      if url.lower() == "none":
        url = None
      with open("./database/db.json") as f:
          data = json.load(f)
      for i in data:
        if i['guild_id'] == ctx.author.guild.id:
          i['welcome']["bg_image"] = url
        
      with open("./database/db.json","w") as f:
        json.dump(data, f, indent=4)
      
      await ctx.send(embed=discord.Embed(title="Welcome", description=f"Welcome background image set!\nUse `{ctx.prefix}welcome` with no subcommand to see the welcome message that will display", color=ctx.author.color))
      

def setup(client):
    client.add_cog(Welcome(client))

