import discord
from discord.ext import commands
import os
import json

cd = "/home/runner/Why-Bot/cogs/"
path = "/home/runner/Why-Bot/MainDB/"

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
      embed.add_field(name="This is the help command. This bot is divided into 12 main categories", value="Categories List:\nDatabase, Economy, Fun, Google, Minecraft, Moderation, Music, Reddit, Text, Utilities, Tickets and Other")
      embed.add_field(name="Use `?help [category]`", value= "for all commands related to said category")
      embed.add_field(name="If you havent already please run ?setup", value="To setup stuff")
      embed.add_field(name="Why Help:", value="Page Under Construction")
      embed.add_field(name="`?botinvite`", value="To invite the bot to you discord server")
      embed.set_footer(text="Default prefix is `?` thats why all the help commands say `?` It might be different on your server")
      embed.set_footer(
          text="Default prefix is ? might be different for your server")
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
        embed.set_footer(
            text="Default prefix is ? might be different for your server")

        return await ctx.send(embed=embed)

      if cat.lower() == 'economy':
        embed = discord.Embed(
          title="Economy Commands",
          color=0x515596
        )
        embed.add_field(name="`?beg`",value="Begs for coins")
        embed.add_field(name="`?gamble <amount>`",value="Gambles your money. 1 in 3 chance of winning")
        embed.add_field(name="`?deposit <amount>`",value="Deposit money into your bank account")
        embed.add_field(name="`?withdraw <amount>`",value="Withdraw money from your bank")
        embed.add_field(name="`?send <amount>`", value="Send money to your friends")
        embed.add_field(name="`?balance`",value="Checks your balance")
        embed.add_field(name="`?bag`",value="Shows all your items")
        embed.add_field(name="`?shop <item=optional>`",value="A place to purchase items")
        embed.add_field(name="`?buy <amount> <item>`",value="Buy things from the shop")
        embed.add_field(name="`?sell <amount> <item>`",value="Sell things you own for some money back")
        embed.add_field(name="`?daily`",value="Collect your daily coins")
        embed.set_footer(
            text="Default prefix is ? might be different for your server")
        return await ctx.send(embed=embed)
        

      if cat.lower() == 'fun':
        embed = discord.Embed(
          title="Fun Commands",
          color=0x515596
        )
        embed.add_field(name="`?roast`",value="The bot sends a roast in chat")
        embed.add_field(name="`?8ball <question>`",value="The bot uses his magic skills to answer your question")
        embed.add_field(name="`?sendroast <@person>`",value="Sends a roast through dm's to someone")
        embed.add_field(name="`?rps <rock/paper/scissors>`",value="Rock paper scissors")
        embed.add_field(name="`?say <text>`",value="Says what you want in chat")
        embed.add_field(name="`?embed <t/d/td> <fields> <img=optional> <channel=optional>`",value="The say command on sterioids")
        embed.add_field(name="`?dm <@person>`",value="The bot dms someone")
        embed.add_field(name="`?yesorno <questions>`",value="Creates a yes or no poll")
        embed.add_field(name='`?poll <time:seconds> "<question>" <options seperated by a space>`",value="Creates a yes or no poll')
        embed.add_field(name="`Counting`",value="This one doesnt have a command you just count in the counting chat")
        embed.add_field(name="`?numrn`",value="Displays current number for counting game")
        embed.set_footer(text="Default prefix is ? might be different for your server")

        return await ctx.send(embed=embed)

      if cat.lower() == 'google':
        embed = discord.Embed(
          title="Google Commands",
          color=0x515596
        )
        embed.add_field(name="`?google <query>`",value="Searches google for website links")
        embed.add_field(name="`?imagesearch <query>`",value="Search for an image")
        embed.add_field(name="`?youtube <query>`",value="Searches youtube for video links")
        embed.set_footer(
            text="Default prefix is ? might be different for your server")

        return await ctx.send(embed=embed)

      if cat.lower() == 'minecraft':
        embed = discord.Embed(
          title="Minecraft Commands",
          color=0x515596
        )
        embed.add_field(name="`?setign <ign>`",value="Sets your ign so you dont have to specify it each time")
        embed.add_field(name="`?hystats <person=optional, defaults to the value from ?setign>`",value="Gets your hypixel stats")
        embed.add_field(
            name="`?getuuid <person=optional, defaults to the value from ?setign>`", value="Gets your uuid")
        embed.add_field(name="`?bwstats <person=optional, defaults to the value from ?setign>`",
                        value="Gets your bedwars stats")
        embed.add_field(name="`?bwchallenge`",value="Bedwars challenge")
        embed.set_footer(
            text="Default prefix is ? might be different for your server")

        return await ctx.send(embed=embed)

      if cat.lower() == 'moderation':
        embed = discord.Embed(
          title="Moderation Commands",
          color=0x515596
        )
        embed.add_field(name="`?setup`",value="VERY IMPORTANT. Sets up the counting, mod and welome channel")
        embed.add_field(name="`?setprefix <prefix>`",value="Sets the server prefix for this bot. Default is: ?")
        embed.add_field(name="`?ban <@person>`", value="Bans a member")
        embed.add_field(name="`?kick <@person>`",value="Kicks a member")
        embed.add_field(name="`?giverole <@role> <@person>`",value="Gives a role to a person")
        embed.add_field(name="`?takerole <@role> <@person>`",value="Takes a role from a person")
        embed.add_field(name="`?report <person/bug/message>`",value="Report a member, message or bug. Member and message reports get sent to the mod chat if you have one")
        embed.add_field(name="`?lockdown <channel=optional, defaults to the channel you type the command in>`",value="Lockdowns a channel (stops members from sending messages)")
        embed.add_field(name="`?unlock <channel=optional, defaults to the channel you type the command in>`",
                        value="Unlocks a channel thats on lockdown")
        embed.add_field(name="`?reactrole <emoji> <@role> <message>`",value="Makes a message and reacting to the message will give you a role")
        embed.add_field(name="`?make_channel <name>`",value="Creates a channel")
        embed.add_field(name="`?make_vc <name>`",value="Creates a VC")
        embed.add_field(name="`?warn <@person> <reason>`",value="Warns a member")
        embed.add_field(name="`?warnings <@person>`",value="Displays the amount of warnings a person has")
        embed.add_field(name="`?clear <amount>`",value="Clears messages from the chat")
        embed.add_field(name="`Custom Vc`",value="This isnt a command but if you rename a VC to Custom VC, Joining it will create a new vc and then delete it upon leaving the vc")
        embed.set_footer(
            text="Default prefix is ? might be different for your server")

        return await ctx.send(embed=embed)

      if cat.lower() == 'music':
        embed = discord.Embed(
          title="Music Commands",
          color=0x515596
        )

        embed.add_field(name="`?join`", value="Why joins to your voice channel.", inline=False)
        embed.add_field(name="`?play <song/ytlink>`",value="Bot joins to your voice channel and plays music from a video link.",inline=False)
        embed.add_field(name="`?leave`", value="Leave the voice channel.", inline=False)
        embed.add_field(name="`?skip`", value="Skips current track.", inline=False)
        embed.add_field(name="`?pause`", value="Pause music.", inline=False)
        embed.add_field(name="`?resume`", value="Resume music.", inline=False)
        embed.add_field(name="`?queue`", value="Shows current queue.", inline=False)
        embed.add_field(name="`?loop`", value="Loops current track.", inline=False)
        embed.set_footer(
            text="Default prefix is ? might be different for your server")

        return await ctx.send(embed=embed)

      if cat.lower() == 'text':
        embed = discord.Embed(
          title="Text Commands",
          color=0x515596
        )
        embed.add_field(name="`?reverse <text>`",value="Reverse a string of text")
        embed.add_field(name="`?expand <text>`",value="E x p a n d s Some text")
        embed.add_field(name="`?drunkify <text>`", value="dRuNkIfy some text")
        embed.add_field(name="`?texttohex <text>`",value="Convert text to hex")
        embed.add_field(name="`?hexttotext <text>`",value="Convert hex to text")
        embed.add_field(name="`?emojify <text>`",value="Emojify text")
        embed.add_field(name="`?binarytotext <text>`",value="Convery binary to text")
        embed.add_field(name="`?texttobinary <text>`",
                        value="Convert text to binary")
        embed.set_footer(text="Default prefix is ? might be different for your server")

        return await ctx.send(embed=embed)

      if cat.lower() == 'utilities':
        embed = discord.Embed(
          title="Utilites Commands",
          color=0x515596
        )
        embed.add_field(name="`?qrcode <link>`",value="Make a qr code for a website")
        embed.add_field(name="`?calc <n1> <operator> <n2>`",value="Calculate things")
        embed.add_field(name="`?weather <city>`",value="Get a weather report for your city")
        embed.set_footer(
            text="Default prefix is ? might be different for your server")

        return await ctx.send(embed=embed)

      if cat.lower() == 'other':
        embed = discord.Embed(
            title="Other Commands",
            color=0x515596
        )
        embed.add_field(name="`?ping`", value="Shows you the bots ping")
        embed.add_field(name="`?invite`", value="Creates an invite link for your server")
        embed.add_field(name="`?botinvite`", value="Invite link for WHY bot, so you can add the bot to your server")
        embed.add_field(name="`?suggest <suggestion>`", value="Suggests somethings and i might add it into the bot")
        embed.add_field(name="`?info <server>`", value="Info about the server")
        embed.add_field(name="`?info <person> <@person>`", value="Info about a person")
        embed.set_footer(text="Default prefix is ? might be different for your server")

      if cat.lower() == 'reddit':
        embed = discord.Embed(
            title="Reddit Commands",
            color=0x515596
        )
        embed.add_field(name="`?meme`", value="Gets a nice new meme for you")
        embed.add_field(name="`?redditimg <subreddit>`", value="Gets an image from that subreddit. Might now work with all subreddits")
        embed.add_field(name="`?reddit <subreddit>`", value="Gets a hot post from that subreddit and gives you the link")
        embed.set_footer(text="Default prefix is ? might be different for your server")

        return await ctx.send(embed=embed)

      if cat.lower() == "ticket":
        os.chdir(path)
        with open(f"ticket{ctx.guild.id}.json") as f:
          data = json.load(f)
        os.chdir(cd)
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if ctx.author.guild_permissions.administrator or valid_user:

            em = discord.Embed(title="Tickets Help", color=0x00a8ff)
            em.add_field(name="`?newticket <message>`", value="This creates a new ticket. Add any words after the command if you'd like to send a message when we initially create your ticket.")
            em.add_field(name="`?closeticket`", value="Use this to close a ticket. This command only works in ticket channels.")
            em.add_field(name="`?addaccess <role_id>`", value="This can be used to give a specific role access to all tickets. This command can only be run if you have an admin-level role for this bot.")
            em.add_field(name="`?delaccess <role_id>`", value="This can be used to remove a specific role's access to all tickets. This command can only be run if you have an admin-level role for this bot.")
            em.add_field(name="`?addadminrole <role_id>`", value="This command gives all users with a specific role access to the admin-level commands for the bot, such as `?addpingedrole` and `?addaccess`. This command can only be run by users who have administrator permissions for the entire server.")
            em.add_field(name="`?deladminrole <role_id>`", value="This command removes access for all users with the specified role to the admin-level commands for the bot, such as `?addpingedrole` and `?addaccess`. This command can only be run by users who have administrator permissions for the entire server.")
            em.set_footer(text="Default prefix is ? might be different for your server")

            await ctx.send(embed=em)
        
        else:

            em = discord.Embed(title = "Tickets Help", color = 0x00a8ff)
            em.add_field(name="`?newticket <message>`", value="This creates a new ticket. Add any words after the command if you'd like to send a message when we initially create your ticket.")
            em.add_field(name="`?closeticket`", value="Use this to close a ticket. This command only works in ticket channels.")
            em.set_footer(text="Default prefix is ? might be different for your server")

            await ctx.send(embed=em)
      else:
        await ctx.send("```Invalid Category\nCategories List:\nCategories List:\nDatabase, Economy, Fun, Google, Minecraft, Moderation, Music, Reddit, Text, Utilities, Tickets and Other```")
  
def setup(client):
    client.add_cog(Help(client))

