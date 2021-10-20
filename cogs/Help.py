import discord
from discord.ext import commands

class Help(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def help(self, ctx, cat=None, cmd=None):

    if cat == None:
      embed = discord.Embed(
        title="WHY HELP",
        color=0x515596
      )
      embed.add_field(name="This is the help command. This bot is divided into 12 main categories", value="Categories List:\ndatabase, economy fun, google, minecraft, moderation, music, reddit, text, utilities, help and other")
      embed.add_field(name="Use `?help [category]`", value= "for all commands related to said category")
      embed.add_field(name="If you havent already please run ?setup", value="To setup stuff")
      embed.add_field(name="Use `?help [category] [command`]", value = "for specific help about a command")
      embed.set_footer(text="Default prefix is `?` thats why all the help commands say `?` It might be differnt on your server")
      return await ctx.send(embed=embed)

    else:
      if cat.lower() == 'database':
        embed = discord.Embed(
          title="Database Commands",
          color=0x515596
        )
        embed.add_field(name="`?genkey`",value="Generates a key for encrypting and decrypting")
        embed.add_field(name="`?store`",value="Encrypts text and stores it in a database. Can only be encrypted/decrypted with a key")
        embed.add_field(name="`?get`",value="Gets items from the database")

        return await ctx.send(embed=embed)

      if cat.lower() == 'economy':
        embed = discord.Embed(
          title="Economy Commands",
          color=0x515596
        )
        embed.add_field(name="`?beg`",value="Begs for coins")
        embed.add_field(name="`?gamble`",value="Gambles your money. 1 in 3 chance of winning")
        embed.add_field(name="`?deposit`",value="Deposit money into your bank account")
        embed.add_field(name="`?withdraw`",value="Withdraw money from your bank")
        embed.add_field(name="`?send`",value="Send money to your friends")
        embed.add_field(name="`?balance`",value="Checks your balance")
        embed.add_field(name="`?bag`",value="Shows all your items")
        embed.add_field(name="`?shop`",value="A place to purchase items")
        embed.add_field(name="`?buy`",value="Buy things from the shop")
        embed.add_field(name="`?sell`",value="Sell things you own for some money back")
        return await ctx.send(embed=embed)
        

      if cat.lower() == 'fun':
        embed = discord.Embed(
          title="Fun Commands",
          color=0x515596
        )
        embed.add_field(name="`?roast`",value="The bot sends a roast in chat")
        embed.add_field(name="`?8ball`",value="The bot uses his magic skills to answer your question")
        embed.add_field(name="`?sendroast`",value="Sends a roast through dm's to someone")
        embed.add_field(name="`?rps`",value="Rock paper scissors")
        embed.add_field(name="`?say`",value="Says what you want in chat")
        embed.add_field(name="`?embed`",value="The say command on sterioids")
        embed.add_field(name="`?dm`",value="The bot dms someone")
        embed.add_field(name="`Counting`",value="This one doesnt have a command you just count in the counting chat")
        embed.add_field(name="`?numrn`",value="Displays current number for counting game")

        return await ctx.send(embed=embed)

      if cat.lower() == 'google':
        embed = discord.Embed(
          title="Google Commands",
          color=0x515596
        )
        embed.add_field(name="`?google`",value="Searches google for website links")
        embed.add_field(name="`?imagesearch`",value="Search for an image")
        embed.add_field(name="`?youtube`",value="Searches youtube for video links")

        return await ctx.send(embed=embed)

      if cat.lower() == 'minecraft':
        embed = discord.Embed(
          title="Minecraft Commands",
          color=0x515596
        )
        embed.add_field(name="`?setign`",value="Sets your ign so you dont have to specify it each time")
        embed.add_field(name="`?hystats`",value="Gets your hypixel stats")
        embed.add_field(name="`?getuuid`",value="Gets your uuid")
        embed.add_field(name="`?bwstats`",value="Gets your bedwars stats")
        embed.add_field(name="`?bwchallenge`",value="Bedwars challenge")

        return await ctx.send(embed=embed)

      if cat.lower() == 'moderation':
        embed = discord.Embed(
          title="Moderation Commands",
          color=0x515596
        )
        embed.add_field(name="`?setup`",value="VERY IMPORTANT. Sets up the counting, mod and welome channel")
        embed.add_field(name="`?setprefix`",value="Sets the server prefix for this bot. Default is: ?")
        embed.add_field(name="`?ban`",value="Bans a member")
        embed.add_field(name="`?kick`",value="Kicks a member")
        embed.add_field(name="`?giverole`",value="Gives a role to a person")
        embed.add_field(name="`?takerole`",value="Takes a role from a person")
        embed.add_field(name="`?report`",value="Report a member, message or bug. Member and message reports get sent to the mod chat if you have one")
        embed.add_field(name="`?lockdown`",value="Lockdowns a channel (stops members from sending messages)")
        embed.add_field(name="`?unlock`",value="Unlocks a channel thats on lockdown")
        embed.add_field(name="`?reactrole`",value="Makes a message and reacting to the message will give you a role")
        embed.add_field(name="`?make_channel`",value="Creates a channel")
        embed.add_field(name="`?make_vc`",value="Creates a VC")
        embed.add_field(name="`?warn`",value="Warns a member")
        embed.add_field(name="`?warnings`",value="Displays the amount of warnings a person has")
        embed.add_field(name="`?clear`",value="Clears messages from the chat")
        embed.add_field(name="`Custom Vc`",value="This isnt a command but if you rename a VC to Custom VC, Joining it will create a new vc and then delete it upon leaving the vc")

        return await ctx.send(embed=embed)

      if cat.lower() == 'music':
        embed = discord.Embed(
          title="Music Commands",
          color=0x515596
        )

        embed.add_field(name="`?join`", value="Why joins to your voice channel.", inline=False)
        embed.add_field(name="`?play`",value="Bot joins to your voice channel and plays music from a video link.",inline=False)
        embed.add_field(name="`?leave`", value="Leave the voice channel.", inline=False)
        embed.add_field(name="`?skip`", value="Skips current track.", inline=False)
        embed.add_field(name="`?pause`", value="Pause music.", inline=False)
        embed.add_field(name="`?resume`", value="Resume music.", inline=False)
        embed.add_field(name="`?queue`", value="Shows current queue.", inline=False)
        embed.add_field(name="`?loop`", value="Loops current track.", inline=False)

        return await ctx.send(embed=embed)

      if cat.lower() == 'text':
        embed = discord.Embed(
          title="Text Commands",
          color=0x515596
        )
        embed.add_field(name="`?reverse`",value="Reverse a string of text")
        embed.add_field(name="`?expand`",value="E x p a n d Some text")
        embed.add_field(name="`?drunkify`",value="dRuNkIfy some text")
        embed.add_field(name="`?texttohex`",value="Convert text to hex")
        embed.add_field(name="`?hexttotext`",value="Convert hex to text")
        embed.add_field(name="`?emojify`",value="Emojify text")
        embed.add_field(name="`?binarytotext`",value="Convery binary to text")
        embed.add_field(name="`?texttobinary`",value="Convert text to binary")

        return await ctx.send(embed=embed)

      if cat.lower() == 'utilities':
        embed = discord.Embed(
          title="Utilites Commands",
          color=0x515596
        )
        embed.add_field(name="`?qrcode`",value="Make a qr code for a website")
        embed.add_field(name="`?calc`",value="Calculate things")
        embed.add_field(name="`?weather`",value="Get a weather report for your city")

        return await ctx.send(embed=embed)

      if cat.lower() == 'other':
        pass

      if cat.lower() == 'reddit':
        pass

      if cat.lower() == "ticket":
        pass
      else:
        await ctx.send("```Invalid Category\nCategories List:\ndatabase, economy fun, google, minecraft, moderation, music, reddit, text, utilities and other```")
  
def setup(client):
    client.add_cog(Help(client))

