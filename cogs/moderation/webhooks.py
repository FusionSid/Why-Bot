import discord
from discord.ext import commands
from utils import plugin_enabled
import requests
from discord_webhook import DiscordEmbed, DiscordWebhook
import json

class Webhooks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["createwebhook", 'cwh'], help="This command is used to create a webhook.\nA webhook is sorta like a bot.Once the webhook is made it will be asigned to your name and whenever you type the id that you specify the webhook will send the message what you want.\nWebhooks only work in one channel at a time so if you want to use a webhook in another channel you will need to make another webhook", extras={"category":"Moderation"}, usage="createhook [name] [channel(optional)]", description="Creates a webhook")
    @commands.check(plugin_enabled)
    @commands.has_permissions(manage_webhooks=True)
    async def createhook(self, ctx, name, channel:discord.TextChannel=None,):
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        if channel == None:
            channel = ctx.channel
        await ctx.send("Enter the url for the image you want to use as the profile pic (or type none for default)")
        avatarurl = await self.client.wait_for("message", timeout=300, check=check)
        avatarurl = avatarurl.content
        if avatarurl.lower() == "none":
            e = await channel.create_webhook(name=name,reason=None)
        else:
            aimg = requests.get(avatarurl)
            aimg = aimg.content
            e = await channel.create_webhook(name=name, avatar=bytes(aimg), reason=None)
        webhook = await self.client.fetch_webhook(e.id)
        await ctx.send(f"Enter the id for the bot (What youll use in the `{ctx.prefix}webhook` command)")
        id = await self.client.wait_for("message", timeout=300, check=check)
        id = id.content
        with open("./database/userdb.json") as f:
          data = json.load(f)
        for i in data:
          if i['user_id'] == ctx.author.id:
            i['webhooks'][id] = webhook.url
        with open('./database/userdb.json', 'w') as f:
          json.dump(data, f, indent=4)
        await ctx.message.delete()
        await ctx.send(embed=discord.Embed(title="Webhook Created", description=f"Use `{ctx.prefix}webhook {id} [message]` to send messages using that webhook", color=ctx.author.color))


    @commands.command(aliases=['webhook', 'swh'],help="This command uses a webhook that you previously made using the createhook command to send a message", extras={"category":"Moderation"}, usage="webhook [id] [text]", description="Send message through a webhook")
    @commands.check(plugin_enabled)
    async def wh(self, ctx, id, *, text):
        with open("./database/userdb.json") as f:
          data = json.load(f)
        found = False
        for i in data:
          if i['user_id'] == ctx.author.id:
            try:
              url = i['webhooks'][id]
            except:
              pass
            found = True
        if found == False:
          return await ctx.send("Id not found")
        await ctx.message.delete()
        webhook = DiscordWebhook(url=url, content=text)
        response = webhook.execute()



def setup(client):
    client.add_cog(Webhooks(client))    
       