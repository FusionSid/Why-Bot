import discord
import random
from discord.ext import commands
import json

with open('./database/shop.json') as f:
    mainshop = json.load(f)

def is_it_me(ctx):
    return ctx.author.id == 624076054969188363

async def get_bank_data():
    with open('./database/economy.json', 'r') as f:
        users = json.load(f)

    return users


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
    with open('./database/economy.json', 'w') as f:
        json.dump(users, f, indent=4)
    return True


def conv2num(amount):
    lenght = 0
    for i in amount:
        lenght += 1
    lenght -= 1

    last_letter = amount[lenght]

    rest = amount[:-1]

    try:
        rest = int(rest)
        if last_letter.lower() == "k":
            amount = rest*1000

        elif last_letter.lower() == "m":
            amount = rest*1000000

    except:
        print("Not a number")

    return amount


async def update_bank(user, change=0, mode='wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('./database/economy.json', 'w') as f:
        json.dump(users, f, indent=4)
    bal = users[str(user.id)]['wallet'], users[str(user.id)]['bank']
    return bal


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.7 * item["price"]
            if item['sell'] == False:
                return
            break

    if name_ == None:
        return [False, 1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]
    for item in users[str(user.id)]["bag"]:
        if item["amount"] == 0:
            users[str(user.id)]["bag"].remove(item)
    with open("./database/economy.json", "w") as f:
        json.dump(users, f, indent=4)
    await update_bank(user, cost, "wallet")

    return [True, "Worked"]


async def buy_this(user, amount, item_name):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]
    with open("./database/economy.json", "w") as f:
        json.dump(users, f, indent=4)

    await update_bank(user, cost*-1, "wallet")

    return [True, "Worked"]


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, person: discord.Member = None):
        print(person)
        if person == None:
            print(ctx.author)
            await open_account(ctx.author)
            user = ctx.author

            users = await get_bank_data()

            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)]["bank"]

            # round
            wallet_amt = round(wallet_amt, 2)
            bank_amt = round(bank_amt, 2)

            wallet_amt = "{:,}".format(wallet_amt)
            bank_amt = "{:,}".format(bank_amt)

            em = discord.Embed(
                title=f'{ctx.author.name} Balance', color=discord.Color.red())
            em.add_field(name="Wallet Balance", value=wallet_amt)
            em.add_field(name='Bank Balance', value=bank_amt)
            await ctx.send(embed=em)
        else:
            await open_account(person)
            user = person

            users = await get_bank_data()

            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)]["bank"]

            # round
            wallet_amt = round(wallet_amt, 2)
            bank_amt = round(bank_amt, 2)

            wallet_amt = "{:,}".format(wallet_amt)
            bank_amt = "{:,}".format(bank_amt)

            em = discord.Embed(
                title=f'{person.name} Balance', color=discord.Color.red())
            em.add_field(name="Wallet Balance", value=wallet_amt)
            em.add_field(name='Bank Balance', value=bank_amt)
            await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)
        user = ctx.author

        users = await get_bank_data()

        earnings = random.randrange(101)

        await ctx.send(embed=discord.Embed(title=f'{ctx.author.display_name} Here you filty peasant', description=f'Got `{earnings}` coins!!'))

        users[str(user.id)]["wallet"] += earnings
        with open("./database/economy.json", 'w') as f:
            json.dump(users, f, indent=4)

    @commands.command()
    @commands.cooldown(1, 60*1440, commands.BucketType.user)
    async def daily(self, ctx):
        await open_account(ctx.author)
        user = ctx.author

        users = await get_bank_data()

        earnings = 10000

        await ctx.send(embed=discord.Embed(title=f'{ctx.author.display_name}', description='Got `{:,}` coins!!'.format(earnings)))

        users[str(user.id)]["wallet"] += earnings
        with open("./database/economy.json", 'w') as f:
            json.dump(users, f, indent=4)


    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amount=None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return

        user = ctx.author

        users = await get_bank_data()

        wallet = users[str(user.id)]["wallet"]
        bank = users[str(user.id)]["bank"]

        try:
            amount = int(amount)

        except:
            if amount.lower() == "max":
                amount = bank

            elif amount.lower() == "all":
                amount = bank

            else:
                amount = conv2num(amount)

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1*amount, 'bank')
        await ctx.send('{} You withdrew {:,} coins'.format(ctx.author.mention, amount))

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount=None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return

        user = ctx.author

        users = await get_bank_data()

        wallet = users[str(user.id)]["wallet"]
        bank = users[str(user.id)]["bank"]

        try:
            amount = int(amount)

        except:
            if amount.lower() == "max":
                amount = wallet

            elif amount.lower() == "all":
                amount = wallet

            else:
                amount = conv2num(amount)

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[0]:
            await ctx.send('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return

        await update_bank(ctx.author, -1*amount)
        await update_bank(ctx.author, amount, 'bank')
        await ctx.send('{} You deposited {:,} coins'.format(ctx.author.mention, amount))

    @commands.command(aliases=['sm', 'donate', 'give'])
    async def send(self, ctx, member: discord.Member, amount=None):
        await open_account(ctx.author)
        await open_account(member)
        if amount == None:
            await ctx.send("Please enter the amount i havent got all day")
            return
        try:
            amount = int(amount)
        except:
            amount = conv2num(amount)

        bal = await update_bank(ctx.author)
        if amount == 'all':
            amount = bal[0]

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send('Get some more coins\nYou do not have sufficient balance in your banl')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return

        await update_bank(ctx.author, -1*amount, 'bank')
        await update_bank(member, amount, 'wallet')
        await ctx.send(f'{ctx.author.mention} You gave {member} `{amount}` coins')

    @commands.command(aliases=['rb', 'steal'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member):
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank(member)

        if bal[0] < 100:
            await ctx.send('It is useless to rob them :(\nThey dont even have 100 coins')
            return

        earning = random.randrange(0, bal[0])

        await update_bank(ctx.author, earning)
        await update_bank(member, -1*earning)
        await ctx.send(f'{ctx.author.mention} You robbed {member} and got `{earning}` coins')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gamble(self, ctx, amount=None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return
        bal = await update_bank(ctx.author)

        user = ctx.author

        users = await get_bank_data()

        wallet = users[str(user.id)]["wallet"]
        bank = users[str(user.id)]["bank"]

        try:
            amount = int(amount)

        except:
            if amount.lower() == "max":
                amount = wallet

            elif amount.lower() == "all":
                amount = wallet

            else:
                amount = conv2num(amount)

        if amount > bal[0]:
            await ctx.send('You do not have sufficient balance')
            return
        if amount < 0:
            await ctx.send('Amount must be positive!')
            return

        win = False
        num = random.randint(1, 3)
        if num == 2:
            win = True

        if win == True:
            await update_bank(ctx.author, 2*amount)
            await ctx.send(f'{ctx.author.mention} You won :) `{2*amount}`')
        else:
            await update_bank(ctx.author, -1*amount)
            await ctx.send(f'{ctx.author.mention} You lose :( `{amount}`')

    @commands.command()
    async def shop(self, ctx, *, item_=None):
        img = None
        if item_ == None:
            em = discord.Embed(title="Shop")

            for item in mainshop:
                name = item["name"]
                price = item["price"]
                price = "{:,}".format(price)
                desc = item["description"]
                buy = item['buy']
                if buy == True:
                    em.add_field(name=f"**{name}**", value=f"$`{price}`")
        else:
            em = discord.Embed(title="Shop")
            inshop = False
            for item in mainshop:
                if item["name"].lower() == item_.lower():
                    name = item["name"]
                    price = item["price"]
                    price = "{:,}".format(price)
                    sell = float(item["price"])*0.7
                    sell = "{:,}".format(sell)
                    desc = item["description"]
                    buy = item['buy']
                    em.add_field(
                        name=f"**Item Name/Id: {name}**", value=f"Buy: $`{price}`\nSell: $`{sell}`\n{desc}")
                    if item["icon_path"] == None:
                        img = None
                    else:
                        img = True
                        file = discord.File(f"./database/shopimages/{item['icon_path']}")
                        em.set_thumbnail(url=f"attachment://./database/shopimages/{item['icon_path']}")
                    inshop = True
                    break
            if inshop == False:
                em.add_field(name=item_, value="Item not in shop")
        if img == None:
            await ctx.send(embed=em)
        if img == True:
            await ctx.send(file=file, embed=em)

    @commands.command(aliases=['purchase'])
    async def buy(self, ctx, amount=1, *, item=None):

        await open_account(ctx.author)

        res = await buy_this(ctx.author, amount, item)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("That Object isn't there!")
                return
            if res[1] == 2:
                await ctx.send(f"You don't have enough coins in your wallet to buy {amount} {item}")
                return

        await ctx.send(f"You just bought {amount} {item}")

    @commands.command(aliases=['inv', 'inventory'])
    async def bag(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em = discord.Embed(title="Bag")
        for item in bag:
            name = item["item"]
            amount = item["amount"]

            em.add_field(name=name, value=amount)

        await ctx.send(embed=em)

    @commands.command()
    async def sell(self, ctx, amount=1, *, item):
        await open_account(ctx.author)

        res = await sell_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("You dont have that item!")
                return
            if res[1] == 2:
                await ctx.send(f"You don't have {amount} {item} in your bag.")
                return
            if res[1] == 3:
                await ctx.send(f"You don't have {item} in your bag.")
                return

        await ctx.send(f"You just sold {amount} {item}.")


def setup(client):
    client.add_cog(Economy(client))
