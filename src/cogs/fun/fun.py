import json
import random
import asyncio
import datetime

import dotenv
import discord
import pyfiglet
from discord.ui import View
from discord.utils import get
from discord.ext import commands

from utils import kwarg_to_embed, blacklisted
from utils.views import ClaimView

dotenv.load_dotenv()

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    @commands.check(blacklisted)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def claim(self, ctx):
        em = discord.Embed(title="Claim 100k Why Coins", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        await ctx.respond(embed=em, view=ClaimView())

    @commands.command()
    @commands.check(blacklisted)
    async def nitro(self, ctx):
        em = discord.Embed(title="Claim Free Nitro", color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.set_image(
            url="https://gudstory.s3.us-east-2.amazonaws.com/wp-content/uploads/2021/02/08150513/Discord-Nitro.png"
        )
        await ctx.send(embed=em, view=ClaimView())

    @commands.slash_command()
    @commands.check(blacklisted)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ascii(self, ctx, *, message):
        font = "big"
        message = pyfiglet.figlet_format(message, font=font)
        await ctx.respond("```\n{}\n```".format(message))

    @commands.slash_command()
    @commands.check(blacklisted)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def fascii(self, ctx, font: str, *, message):
        if font not in ["1943____", "3-d", "3x5", "4x4_offr", "5slalineoblique", "5x7", "5x8", "64f1____", "6x10", "6x9", "a_zooloo", "acrobatic", "advenger", "alligator", "alligator2", "alphabet", "aquaplan", "arrows", "asc_____", "ascii___", "assalt_m", "asslt__m", "atc_____", "atc_gran", "avatar", "b_m__200", "banner", "banner3", "banner3-D", "banner4", "barbwire", "basic", "battle_s", "battlesh", "baz__bil", "beer_pub", "bell", "big", "bigchief", "binary", "block", "brite", "briteb", "britebi", "britei", "broadway", "bubble", "bubble__", "bubble_b", "bulbhead", "c1______", "c2______", "c_ascii_", "c_consen", "calgphy2", "caligraphy", "catwalk", "caus_in_", "char1___", "char2___", "char3___", "char4___", "charact1", "charact2", "charact3", "charact4", "charact5", "charact6", "characte", "charset_", "chartr", "chartri", "chunky", "clb6x10", "clb8x10", "clb8x8", "cli8x8", "clr4x6", "clr5x10", "clr5x6", "clr5x8", "clr6x10", "clr6x6", "clr6x8", "clr7x10", "clr7x8", "clr8x10", "clr8x8", "coil_cop", "coinstak", "colossal", "com_sen_", "computer", "contessa", "contrast", "convoy__", "cosmic", "cosmike", "cour", "courb", "courbi", "couri", "crawford", "cricket", "cursive", "cyberlarge", "cybermedium", "cybersmall", "d_dragon", "dcs_bfmo", "decimal", "deep_str", "defleppard", "demo_1__", "demo_2__", "demo_m__", "devilish", "diamond", "digital", "doh", "doom", "dotmatrix", "double", "drpepper", "druid___", "dwhistled", "e__fist_", "ebbs_1__", "ebbs_2__", "eca_____", "eftichess", "eftifont", "eftipiti", "eftirobot", "eftitalic", "eftiwall", "eftiwater", "epic", "etcrvs__", "f15_____", "faces_of", "fair_mea", "fairligh", "fantasy_", "fbr12___", "fbr1____", "fbr2____", "fbr_stri", "fbr_tilt", "fender", "finalass", "fireing_", "flyn_sh", "fourtops", "fp1_____", "fp2_____", "fraktur", "funky_dr", "future_1", "future_2", "future_3", "future_4", "future_5", "future_6", "future_7", "future_8", "fuzzy", "gauntlet", "ghost_bo", "goofy", "gothic", "gothic__", "graceful", "gradient", "graffiti", "grand_pr", "greek", "green_be", "hades___", "heavy_me", "helv", "helvb", "helvbi", "helvi", "heroboti", "hex", "high_noo", "hills___", "hollywood", "home_pak", "house_of", "hypa_bal", "hyper___", "inc_raw_", "invita", "isometric1", "isometric2", "isometric3", "isometric4", "italic", "italics_", "ivrit", "jazmine", "jerusalem", "joust___", "katakana", "kban", "kgames_i", "kik_star", "krak_out", "larry3d", "lazy_jon", "lcd", "lean", "letter_w", "letters", "letterw3", "lexible_", "linux", "lockergnome", "mad_nurs", "madrid", "magic_ma", "marquee", "master_o", "maxfour", "mayhem_d", "mcg_____", "mig_ally", "mike", "mini", "mirror", "mnemonic", "modern__", "morse", "moscow", "mshebrew210", "nancyj", "nancyj-fancy", "nancyj-underlined", "new_asci", "nfi1____", "nipples", "notie_ca", "npn_____", "ntgreek", "nvscript", "o8", "octal", "odel_lak", "ogre", "ok_beer_", "os2", "outrun__", "p_s_h_m_", "p_skateb", "pacos_pe", "panther_", "pawn_ins", "pawp", "peaks", "pebbles", "pepper", "phonix__", "platoon2", "platoon_", "pod_____", "poison", "puffy", "pyramid", "r2-d2___", "rad_____", "rad_phan", "radical_", "rainbow_", "rally_s2", "rally_sp", "rampage_", "rastan__", "raw_recu", "rci_____", "rectangles", "relief", "relief2", "rev", "ripper!_", "road_rai", "rockbox_", "rok_____", "roman", "roman___", "rot13", "rounded", "rowancap", "rozzo", "runic", "runyc", "sans", "sansb", "sansbi", "sansi", "sblood", "sbook", "sbookb", "sbookbi", "sbooki", "script", "script__", "serifcap", "shadow", "shimrod", "short", "skate_ro", "skateord", "skateroc", "sketch_s", "slant", "slide", "slscript", "sm______", "small", "smisome1", "smkeyboard", "smscript", "smshadow", "smslant", "smtengwar", "space_op", "spc_demo", "speed", "stacey", "stampatello", "standard", "star_war", "starwars", "stealth_", "stellar", "stencil1", "stencil2", "stop", "straight", "street_s", "subteran", "super_te", "t__of_ap", "tanja", "tav1____", "taxi____", "tec1____", "tec_7000", "tecrvs__", "tengwar", "term", "thick", "thin", "threepoint", "ti_pan__", "ticks", "ticksslant", "tiles", "times", "timesofl", "tinker-toy", "tomahawk", "tombstone", "top_duck", "trashman", "trek", "triad_st", "ts1_____", "tsalagi", "tsm_____", "tsn_base", "tty", "ttyb", "tubular", "twin_cob", "twopoint", "type_set", "ucf_fan_", "ugalympi", "unarmed_", "univers", "usa_____", "usa_pq__", "usaflag", "utopia", "utopiab", "utopiabi", "utopiai", "vortron_", "war_of_w", "wavy", "weird", "whimsy", "xbrite", "xbriteb", "xbritebi", "xbritei", "xchartr", "xchartri", "xcour", "xcourb", "xcourbi", "xcouri", "xhelv", "xhelvb", "xhelvbi", "xhelvi", "xsans", "xsansb", "xsansbi", "xsansi", "xsbook", "xsbookb", "xsbookbi", "xsbooki", "xtimes", "xtty", "xttyb", "yie-ar__", "yie_ar_k", "z-pilot_", "zig_zag_", "zone7___"]:
            return await ctx.send("Invalid Font")
        message = pyfiglet.figlet_format(message, font=font)
        await ctx.respond("```\n{}\n```".format(message))

    @commands.slash_command()
    @commands.check(blacklisted)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _8ball(self, ctx, *, question):
        _8ballans = [
            "As I see it, yes",
            "It is certain",
            "It is decidedly so",
            "Most likely",
            "Outlook good",
            "Signs point to yes",
            "Without a doubt",
            "Yes",
            "Yes - definitely",
            "You may rely on it",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
        ]
        em = discord.Embed(
            title="8 Ball",
            description=f"{question}\nAnswer: {random.choice(_8ballans)}",
            color=ctx.author.color
        )
        em.timestamp = datetime.datetime.utcnow()
        await ctx.respond(embed=em)

    @commands.command()
    @commands.check(blacklisted)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def embed(self, ctx, *, kwargs):
        data = await kwarg_to_embed(self.client, ctx, kwargs)
        if data is None:
            return
        em = data[0]
        channel = data[1]
        content = data[2]

        await ctx.message.delete()
        await channel.send(embed=em, content=content)


    @commands.slash_command()
    @commands.check(blacklisted)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def say(self, ctx, *, text):
        await ctx.respond(f"{text}\n\n|| On behalf of {ctx.author.name} ||")


    @commands.slash_command()
    @commands.check(blacklisted)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def whypp(self, ctx):
        await ctx.respond(
            """
**|   WHY PP   |**
**         **<:why:932912321544728576> 
        <:why:932912321544728576> 
        <:why:932912321544728576> 
        <:why:932912321544728576> 
        <:why:932912321544728576> 
<:why:932912321544728576> **       **  <:why:932912321544728576>
"""
        )

    @commands.slash_command()
    @commands.check(blacklisted)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hack(self, ctx, member: discord.Member):

        email_ext = ["gmail.com", "yahoo.com", "hotmail.com", "aol.com", "hotmail.co.uk", "hotmail.fr", "msn.com", "yahoo.fr", "wanadoo.fr", "orange.fr", "comcast.net", "yahoo.co.uk", "yahoo.com.br", "yahoo.co.in", "live.com", "rediffmail.com", "free.fr", "gmx.de", "web.de", "yandex.ru", "ymail.com", "libero.it", "outlook.com", "uol.com.br", "bol.com.br", "mail.ru", "cox.net", "hotmail.it", "sbcglobal.net", "sfr.fr", "live.fr", "verizon.ne","live.co.uk"]
        most_used_words = ["TrASh", "gEt gUd", "waSsUp", "noOb", "LmAo", "lol", "lMfao", "e", "seNd nUkeS", "f&Ck", "sH#t", "nub", "b1T#h"]
        passwords = [ "123456", "password", "12345", "123456789", "password1", "abc123", "12345678", "qwerty", "111111", "1234567", "1234", "iloveyou", "sunshine", "monkey", "1234567890", "123123", "princess", "baseball", "dragon", "football", "shadow", "michael", "soccer", "unknown", "maggie", "000000.", "ashley", "myspace1", "purple", "fuckyou", "charlie", "jordan", "hunter", "superman", "tigger", "michelle", "buster", "pepper", "justin", "andrew", "harley", "matthew", "bailey", "jennifer", "samantha", "ginger", "anthony", "qwerty123", "qwerty1", "peanut"]

        hack_message = await ctx.respond(f"[▖] Hacking {member.name} now...")
        await asyncio.sleep(1.420)
        await hack_message.edit(content="[▘] Finding discord login... (2fa bypassed)")
        await asyncio.sleep(1.69)
        email = f"{member.name}.{random.randint(1, 100)}@{random.choice(email_ext)}"
        await hack_message.edit(
            content=f"[▝] `Email: {email}`\n    `Password: {random.choice(passwords)}`"
        )
        await asyncio.sleep(1.420)
        await hack_message.edit(content="[▗] IP address: 127.0.0.1:50")
        await asyncio.sleep(1.69)
        await hack_message.edit(
            content=f"[▖] Most used words: {random.choice(most_used_words)}"
        )
        await asyncio.sleep(1.420)
        await hack_message.edit(
            content=f"[▘] Injecting trojan virus into discriminator: {member.discriminator}"
        )
        await asyncio.sleep(1.69)
        await hack_message.edit(content="[▝] Selling information to the government...")
        await asyncio.sleep(1.420)
        await hack_message.edit(
            content=f"[▗] Reporting account to discord for breaking TOS..."
        )
        await asyncio.sleep(1.69)
        await hack_message.edit(content="[▖] Hacking medical records...")
        await asyncio.sleep(1.420)
        await hack_message.edit(content=f"Finished hacking {member.mention}")

        await ctx.send("The *totally* real and dangerous hack is complete!")

    
def setup(client):
    client.add_cog(Fun(client))
