import discord
import json
from discord.ext import commands
from discordLevelingSystem import DiscordLevelingSystem, LevelUpAnnouncement
from easy_pil import Editor, Canvas, Font, load_image_async, Text
import os
from utils.checks import is_it_me, plugin_enabled

lvlembed = discord.Embed(color=discord.Color.green())
lvlembed.set_author(name=LevelUpAnnouncement.Member.name)
lvlembed.description = f'Congrats {LevelUpAnnouncement.Member.mention}! You are now level {LevelUpAnnouncement.LEVEL} 😎'

announcement = LevelUpAnnouncement(lvlembed)

lvl = DiscordLevelingSystem(rate=1, per=10.0,level_up_announcement=announcement)
lvl.connect_to_database_file('database/DiscordLevelingSystem.db')

async def lb(self, ctx):
    data = await lvl.each_member_data(ctx.guild, sort_by='rank')

    leaderboard_image = Editor(Canvas((680, 800)))
    bg = await load_image_async("https://i.imgur.com/FRJXi4k.png")
    bg_img = Editor(bg).rotate(90.0)
    leaderboard_image.rectangle((0, 0), width=680, height=800, fill="#23272A")
    leaderboard_image.paste(bg_img, (-600, 0))
    
    n = 0
    yp = 5

    for i in data:
        try:
            member = ctx.guild.get_member(i.id_number)

            person = Editor(Canvas((670, 75), color="#5663F7"))

            if member.avatar is None:
                profile_image = await load_image_async("https://cdn.logojoy.com/wp-content/uploads/20210422095037/discord-mascot.png")
                person_avatar = Editor(profile_image).resize((60, 60)).circle_image()
            else:
                profile_image = await load_image_async(str(member.avatar.url))
                person_avatar = Editor(profile_image).resize((60, 60)).circle_image()

            person.paste(person_avatar, (7, 7))
            
            poppins_medium = Font.poppins(variant="bold", size=25)
            
            person.text((100, 20), f"#{n+1}  ●  {member.display_name}  ●  LVL: {i.level}", font=poppins_medium, color="white", align="left")


            leaderboard_image.paste(person, (5,yp))

            yp += 80
            n += 1
        except Exception as e:
            print(e)
        if n == 10:
            break 
    
    leaderboard_image.save(f"./tempstorage/leveling{ctx.author.id}.png")

    await ctx.send(file=discord.File(f"./tempstorage/leveling{ctx.author.id}.png"))

class Leveling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['lvl'], extras={"category":"Leveling"}, usage="rank [@user(optional)]", help="This command shows your rank for the leveling system.", description="Shows your rank image")
    @commands.check(plugin_enabled)
    async def rank(self, ctx, member:discord.Member=None):
        if member == None:
            data = await lvl.get_data_for(ctx.author)
        else:
             data = await lvl.get_data_for(member)

        LEVELS_AND_XP = {
            '0': 0,'1': 100,'2': 255,'3': 475,
            '4': 770,'5': 1150,'6': 1625,'7': 2205,'8': 2900,'9': 3720,'10': 4675,'11': 5775,'12': 7030,
            '13': 8450,'14': 10045,'15': 11825,'16': 13800,'17': 15980,'18': 18375,'19': 20995,'20': 23850,
            '21': 26950,'22': 30305,'23': 33925,'24': 37820,'25': 42000,'26': 46475,'27': 51255,'28': 56350,
            '29': 61770,'30': 67525,'31': 73625,'32': 80080,'33': 86900,'34': 94095,'35': 101675,'36': 109650,
            '37': 118030,'38': 126825,'39': 136045,'40': 145700,'41': 155800,'42': 166355,'43': 177375,'44': 188870,
            '45': 200850,'46': 213325,'47': 226305,'48': 239800,'49': 253820,'50': 268375,'51': 283475,'52': 299130,
            '53': 315350,'54': 332145,'55': 349525,'56': 367500,'57': 386080,'58': 405275,'59': 425095,'60': 445550,
            '61': 466650,'62': 488405,'63': 510825,'64': 533920,'65': 557700,'66': 582175,'67': 607355,'68': 633250,
            '69': 659870,'70': 687225,'71': 715325,'72': 744180,'73': 773800,'74': 804195,'75': 835375,'76': 867350,
            '77': 900130,'78': 933725,'79': 968145,'80': 1003400,'81': 1039500,'82': 1076455,'83': 1114275,'84': 1152970,
            '85': 1192550,'86': 1233025,'87': 1274405,'88': 1316700,'89': 1359920,'90': 1404075,'91': 1449175,'92': 1495230,
            '93': 1542250,'94': 1590245,'95': 1639225,'96': 1689200,'97': 1740180,'98': 1792175,'99': 1845195,'100': 1899250
        }

        if member == None:
            member = ctx.author
        else:
            pass
        arank = data.xp
        brank = LEVELS_AND_XP[f"{data.level+1}"]
        frac = arank/brank
        percentage = "{:.0%}".format(frac)
        percentage = int(percentage[:-1])

        user_data = {  # Most likely coming from database or calculation
        "name": f"{member.name}",  # The user's name
        "xp": arank,
        "level": data.level,
        "next_level_xp": brank,
        "percentage": percentage,
        "rank": data.rank
        }

        background = Editor(Canvas((934, 282), "#23272a"))
        profile_image = await load_image_async(str(member.avatar.url))
        profile = Editor(profile_image).resize((150, 150)).circle_image()


        poppins = Font.poppins(size=30)

        background.rectangle((20, 20), 894, 242, "#2a2e35")
        background.paste(profile, (50, 50))
        background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
        background.bar(
            (260, 180),
            max_width=630,
            height=40,
            percentage=user_data["percentage"],
            fill="#00fa81",
            radius=20,
        )
        
        background.text((270, 120), user_data["name"], font=poppins, color="#00fa81")
        background.text(
            (870, 125),
            f"{user_data['xp']} / {user_data['next_level_xp']}",
            font=poppins,
            color="#00fa81",
            align="right",
        )

        rank_level_texts = [
            Text("Rank ", color="#00fa81", font=poppins),
            Text(f"{user_data['rank']}", color="#1EAAFF", font=poppins),
            Text("   Level ", color="#00fa81", font=poppins),
            Text(f"{user_data['level']}", color="#1EAAFF", font=poppins),
        ]

        background.multicolor_text((850, 30), texts=rank_level_texts, align="right")

        # send
        background.save(f"tempstorage/rank{member.id}.png")
        await ctx.send(file=discord.File(f"tempstorage/rank{member.id}.png"))
        os.remove(f"tempstorage/rank{member.id}.png")


    @commands.command(aliases=['lb'], extras={"category":"Leveling"}, usage="leaderboard", help="This command shows the leaderboard for this server.\nIt is sorted by most highest level to lowest.", description="Shows the leaderboard for your server")
    @commands.check(plugin_enabled)
    async def leaderboard(self, ctx):
        await lb(self, ctx)
    

    @commands.command()
    @commands.check(is_it_me)
    async def addxp(self, ctx, member:discord.Member, amount:int):
        await ctx.message.delete()
        await lvl.add_xp(member=member, amount=amount)


    @commands.command()
    @commands.check(is_it_me)
    async def removexp(self, ctx, member:discord.Member, amount:int):
        await ctx.message.delete()
        await lvl.remove_xp(member=member, amount=amount)


    @commands.command()
    @commands.check(is_it_me)
    async def setlvl(self,ctx, member:discord.Member, level:int):
        await ctx.message.delete()
        await lvl.set_level(member=member, level=level)

    @commands.command()
    async def givexp(self, ctx, member:discord.Member, amount:int):
        await lvl.remove_xp(member=ctx.author, amount=amount)
        await lvl.add_xp(member=member, amount=amount)
        await ctx.send(f"Gave {amount} xp to {member.name}, Removed {amount} xp from {ctx.author.name}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
          return
        data = await self.client.get_db()
        if data[str(message.guild.id)]['settings']['plugins']['Leveling'] == False:
            return
        try:
          await lvl.award_xp(amount=[15, 25], message=message)
        except Exception:
          return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await lvl.reset_member(member)

def setup(client):
    client.add_cog(Leveling(client))