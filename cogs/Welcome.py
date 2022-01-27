import discord
from utils.other import log
from discord.ext import commands
from easy_pil import Editor, Canvas, Font, load_image, Text
import os
import json

async def memberjoin(client, member):
    with open("./database/db.json") as f:
      data = json.load(f)
    for i in data:
      if i['guild_id'] == member.guild.id:
        WELCOMETEXT = i['settings']['welcometext']
    # Custom Image
    background = Editor(Canvas((900, 270), "#23272a"))

    # For profile to use users profile picture load it from url using the load_image/load_image_async function
    if member.avatar is not None:
      profile_image = load_image(str(member.avatar.url))
    else:
      profile_image = load_image(str("https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png"))
    profile = Editor(profile_image).resize((200, 200)).circle_image()

    # Fonts to use with different size
    poppins_big = Font.poppins(variant="bold", size=50)
    poppins_mediam = Font.poppins(variant="bold", size=40)
    poppins_regular = Font.poppins(variant="regular", size=30)
    poppins_thin = Font.poppins(variant="light", size=18)

    card_left_shape = [(0, 0), (0, 270), (330, 270), (260, 0)]

    background.polygon(card_left_shape, "#2C2F33")
    background.paste(profile, (40, 35))
    background.text((600, 20), "WELCOME", font=poppins_big, color="white", align="center")
    background.text(
        (600, 70), f"{member.name}", font=poppins_regular, color="white", align="center"
    )
    background.text(
        (600, 120), "THANKS FOR JOINING", font=poppins_mediam, color="white", align="center"
    )
    background.text(
        (600, 160), f"{member.guild.name}", font=poppins_regular, color="white", align="center"
    )
    background.text(
        (620, 245),
        f"{WELCOMETEXT}",
        font=poppins_thin,
        color="white",
        align="center",
    )

    background.save(f"./tempstorage/welcome{member.id}.png")

    with open(f"./database/db.json") as f:
        # Open setup file and check if there is a welcome channel
        data = json.load(f)
    for i in data:
        if i["guild_id"] == member.guild.id:
            cha = i["welcome_channel"]
    if cha == None:
        await member.guild.system_channel.send(file=discord.File(f"./tempstorage/welcome{member.id}.png"))
    else:
        channel = await client.fetch_channel(int(cha))
        # Send welcome message in server welcome channel
        await channel.send(file=discord.File(f"./tempstorage/welcome{member.id}.png"))
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

def setup(client):
    client.add_cog(Welcome(client))

