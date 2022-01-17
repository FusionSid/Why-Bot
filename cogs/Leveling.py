import discord
from discord.ext import commands
from discordLevelingSystem import DiscordLevelingSystem, RoleAward, LevelUpAnnouncement
from easy_pil import Editor, Canvas, Font, load_image, Text
import os
from utils.checks import is_it_me

lvlembed = discord.Embed()
lvlembed.set_author(name=LevelUpAnnouncement.Member.name,
                    icon_url=LevelUpAnnouncement.Member.avatar_url)
lvlembed.description = f'Congrats {LevelUpAnnouncement.Member.mention}! You are now level {LevelUpAnnouncement.LEVEL} 😎'

announcement = LevelUpAnnouncement(lvlembed)

lvl = DiscordLevelingSystem(
    rate=1, per=10.0, level_up_announcement=announcement)
lvl.connect_to_database_file('database/DiscordLevelingSystem.db')

class Leveling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['lvl'])
    async def rank(ctx, member:discord.Member=None):
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
        profile_image = load_image(str(member.avatar.url))
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


    @commands.command()
    async def leaderboard(ctx):
        data = await lvl.each_member_data(ctx.guild, sort_by='rank')
        em = discord.Embed(title="Leaderboard")
        n = 0
        for i in data:
            em.add_field(name=f'{i.rank}: {i.name}', value=f'Level: {i.level}, Total XP: {i.total_xp}', inline=False)
            n += 1
            if n == 10:
                break 
            await ctx.send(embed=em)


    @commands.command()
    @commands.check(is_it_me)
    async def addxp(ctx, member:discord.Member, amount:int):
        await ctx.message.delete()
        await lvl.add_xp(member=member, amount=amount)


    @commands.command()
    @commands.check(is_it_me)
    async def removexp(ctx, member:discord.Member, amount:int):
        await ctx.message.delete()
        await lvl.remove_xp(member=member, amount=amount)


    @commands.command()
    @commands.check(is_it_me)
    async def setlvl(ctx, member:discord.Member, level:int):
        await ctx.message.delete()
        await lvl.set_level(member=member, level=level)

    @commands.command()
    async def givexp(ctx, member:discord.Member, amount:int):
        await lvl.remove_xp(member=ctx.author, amount=amount)
        await lvl.add_xp(member=member, amount=amount)
        await ctx.send(f"Gave {amount} xp to {member.name}, Removed {amount} xp from {ctx.author.name}")

