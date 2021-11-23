import discord
import os
import sqlite3
from discord.ext import commands
from cryptography.fernet import Fernet


def gen_key():
    key = Fernet.generate_key()
    return key


def encrypt(key, message):
    message = message.encode()
    f = Fernet(key)
    encrypted = f.encrypt(message)
    return encrypted


def decrypt(key, encrypted):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted).decode()
    return decrypted


db_path = "/home/runner/Why-Bot/EncryptDB/"
cd = "/home/runner/Why-Bot/cogs/"


class Database(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['storage', 'db'])
    async def store(self, ctx):
        conn = sqlite3.connect(f"/home/runner/Why-Bot/EncryptDB/{ctx.guild.id}.db")
        c = conn.cursor()

        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send("```|Database|\nBefore you start you will need a key.\nIf you dont have one type: exit and run ?gen_key to get a key\nIt is advised to use this command in dms```")

        await ctx.send("```Please enter key:```")
        key_ = await self.client.wait_for("message", check=wfcheck)
        key_ = key_.content
        try:
            await ctx.channel.purge(limit=1)
        except:
            pass

        if key_.lower() == "exit":
            return

        await ctx.send("```Please enter what you would like to name your stored content:```")
        name = await self.client.wait_for("message", check=wfcheck)
        name = name.content

        await ctx.send("```Lastly enter the text you want to store:```")
        value = await self.client.wait_for("message", check=wfcheck)
        value = value.content
        try:
            await ctx.channel.purge(limit=1)
        except:
            pass

        value = str(value)
        evalue = encrypt(key_, value)
        c.execute(
            f"CREATE TABLE IF NOT EXISTS {ctx.author.name} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT)")
        with conn:
            c.execute(f"INSERT INTO {ctx.author.name} (name, password) VALUES (:name, :password)", {
                      'name': name, 'password': evalue})
        await ctx.send("Done")

    @commands.command(aliases=['getdb', 'find'])
    async def get(self, ctx):
        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author
        conn = sqlite3.connect(f"/home/runner/Why-Bot/EncryptDB/{ctx.guild.id}.db")
        c = conn.cursor()

        def find(search_type="all", search=None):
            if search_type == 'name':
                with conn:
                    c.execute(
                        f"SELECT * FROM {ctx.author.name} WHERE name = :name", {'name': search})
                return c.fetchall()

            if search_type == 'id':
                with conn:
                    c.execute(
                        f"SELECT * FROM {ctx.author.name} WHERE id = :id", {'id': int(search)})
                return c.fetchall()

            if search_type == 'all':
                with conn:
                    c.execute(f"SELECT * FROM {ctx.author.name}")
                return c.fetchall()

            else:
                print("ERROR")

        await ctx.send("```Enter search type (name/id/all):```")
        stype = await self.client.wait_for("message", check=wfcheck)
        stype = stype.content
        stype = stype.lower()

        await ctx.send("```Enter search (if your search type was all type: all):```")
        search = await self.client.wait_for("message", check=wfcheck)
        search = search.content
        result = find(stype, search)
        resultem = discord.Embed(
            title=f"{ctx.author.name}'s Database", description="Showing Encrypted Version")
        for item in result:
            pid = item[0]
            pname = item[1]
            ppass = item[2]
            resultem.add_field(
                name=pname, value=f"Id: {pid}\Encrypted password: {ppass}")
        await ctx.send(embed=resultem)
        await ctx.send("```If you would like it decrypted enter the id of the one you want to decrypt if not type: no```")
        id_ = await self.client.wait_for("message", check=wfcheck)
        id_ = id_.content
        try:
            id_ = int(id_)
        except:
            return
        await ctx.send("```Please enter key:```")
        key_ = await self.client.wait_for("message", check=wfcheck)
        key_ = key_.content
        try:
            await ctx.channel.purge(limit=1)
        except:
            pass
        print(key_)
        value = find("id", id_)
        tdecrypt = value[0][2]
        decrypted = decrypt(key_, tdecrypt)
        id_ = value[0][0]
        name = value[0][1]
        await ctx.send("Decrypted sent to dms")
        await ctx.author.send(f"Id: {id_}\nName: {name}\nDecrypted: {decrypted}")

    @commands.command(aliases=['key', 'genkey'])
    async def gen_key(self, ctx):
        key_ = gen_key()
        key_ = key_.decode()
        await ctx.author.send(key_)
        await ctx.send("Key sent to dms")


def setup(client):
    client.add_cog(Database(client))
