import discord
from utils.checks import plugin_enabled
import random
import binascii
from discord.ext import commands
from discord.ext.commands import clean_content


class TextConvert(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['mock'], help="This command dRuNKiFies text", extras={"category":"Text"}, usage="drunkify [text]", description="Drunkifies Text")
    @commands.check(plugin_enabled)
    async def drunkify(self, ctx, *, s):
        lst = [str.upper, str.lower]
        newText = await commands.clean_content().convert(ctx, ''.join(random.choice(lst)(c) for c in s))
        if len(newText) <= 380:
            await ctx.send(newText)
        else:
            try:
                await ctx.author.send(newText)
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command(aliases=['exp'], help="This command e x p a n d s text", extras={"category":"Text"}, usage="expand [num] [text]", description="Expands Text")
    @commands.check(plugin_enabled)
    async def expand(self, ctx,  num: int, *, s: clean_content):
        spacing = ""
        if num > 0 and num <= 10:
            for _ in range(num):
                spacing += " "
            result = spacing.join(s)
            if len(result) <= 200:
                await ctx.send(result)
            else:
                try:
                    await ctx.author.send(result)
                    await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
                except Exception:
                    await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")
        else:
            await ctx.send("```fix\nError: The number can only be from 1 to 5```")

    @commands.command(aliases=['rev'], help="This command Reverses text like this:\nsiht ekil txet sesreveR dnammoc sihT", extras={"category":"Text"}, usage="reverse [text]", description="Reverses Text")
    @commands.check(plugin_enabled)
    async def reverse(self, ctx, *, s: clean_content):
        result = await commands.clean_content().convert(ctx, s[::-1])
        if len(result) <= 350:
            await ctx.send(f"{result}")
        else:
            try:
                await ctx.author.send(f"{result}")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command(aliases=['tth'], help="This command converts text to hexadecimal", extras={"category":"Text"}, usage="texttohex [text]", description="Converts Text to hex")
    @commands.check(plugin_enabled)
    async def texttohex(self, ctx, *, s):
        try:
            hexoutput = await commands.clean_content().convert(ctx, (" ".join("{:02x}".format(ord(c)) for c in s)))
        except Exception as e:
            await ctx.send(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/hexadecimal/#data**")
        if len(hexoutput) <= 479:
            await ctx.send(f"```fix\n{hexoutput}```")
        else:
            try:
                await ctx.author.send(f"```fix\n{hexoutput}```")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command(aliases=['htt'], help="This command converts hexcadecimal text to text", extras={"category":"Text"}, usage="hextotext [text]", description="Converts hex to Text")
    @commands.check(plugin_enabled)
    async def hextotext(self, ctx, *, s):
        try:
            cleanS = await commands.clean_content().convert(ctx, bytearray.fromhex(s).decode())
        except Exception as e:
            await ctx.send(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/hexadecimal/#data**")
        if len(cleanS) <= 479:
            await ctx.send(f"```{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```{cleanS}```")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command(aliases=['ttb'], help="This command converts text to binary 0s and 1s ", extras={"category":"Text"}, usage="texttobinary", description="Convert to binary")
    @commands.check(plugin_enabled)
    async def texttobinary(self, ctx, *, s):
        try:
            cleanS = await commands.clean_content().convert(ctx, ' '.join(format(ord(x), 'b') for x in s))
        except Exception as e:
            await ctx.send(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/convert-text-to-binary/#data**")
        if len(cleanS) <= 479:
            await ctx.send(f"```fix\n{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```fix\n{cleanS}```")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command(aliases=['btt'], help="This command converts binary to text", extras={"category":"Text"}, usage="binarytotext", description="Convert binary to text")
    @commands.check(plugin_enabled)
    async def binarytotext(self, ctx, *, s):
        try:
            cleanS = await commands.clean_content().convert(ctx, ''.join([chr(int(s, 2)) for s in s.split()]))
        except Exception as e:
            await ctx.send(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/convert-text-to-binary/#data**")
        if len(cleanS) <= 479:
            await ctx.send(f"```{cleanS}```")
        else:
            try:
                await ctx.author.send(f"```{cleanS}```")
                await ctx.send(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.send(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

    @commands.command(aliases=['emoji'], help="This command converts text to emojies", extras={"category":"Text"}, usage="emojify [text]", description="Emojifies Text")
    @commands.check(plugin_enabled)
    async def emojify(self, ctx, *, text):
        emojis = []
        for s in text.lower():
            if s.isdecimal():
                num2emo = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four',
                           5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}
                emojis.append(f':{num2emo.get(s)}:')
            elif s.isalpha():
                emojis.append(f':regional_indicator_{s}:')
            else:
                emojis.append(s)
        await ctx.send(' '.join(emojis))


def setup(client):
    client.add_cog(TextConvert(client))
