import discord
import qrcode
import math
import json
import requests
from discord.ext import commands
import os
import datetime


def calculator(num1, operator, num2):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "/":
        return num1 / num2
    elif operator == "x":
        return num1 * num2

class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['calculator'])
    async def calc(self, ctx, n1: float, op, n2: float):
        ans = calculator(n1, op, n2)
        await ctx.send(embed=discord.Embed(title='Calculator Result:', description=ans))

    @commands.command(aliases=['qr'])
    async def qrcode(self, ctx, *, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(url))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",
                            back_color="white").convert('RGB')
        img.save('qrcode.png')
        await ctx.send(file=discord.File('qrcode.png'))


def setup(client):
    client.add_cog(Utilities(client))
