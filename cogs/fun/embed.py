import discord
from discord.ext import commands
import base64
import json
from urllib.parse import unquote

async def decode(url):
    url = url.split("?data=")
    b64_string = url[1]
    b64_string = b64_string.replace("%3D", "=")
    base_decode = base64.b64decode(b64_string)
    json_data = json.loads(unquote(base_decode))

    return json_data


class CustomEmbed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def customembed(self, ctx, url:str):
        await ctx.message.delete()
        if "/account/embed?data=" not in url:
            return await ctx.send(embed=discord.Embed(title="Link Invalid", description="Go to [why dashboard](https://why.fusionsid.repl.co/account/embed) to create embed then copy the link"))
        
        json_data = await decode(url)

        em = discord.Embed()

        if "embed" not in json_data and "message" not in json_data:
            return await ctx.send("cant send an empty message")

        if json_data["embed"]:
            print("e")
            embed = json_data["embed"]
            if "title" in embed:
                em.title = embed["title"]

            if "description" in embed:
                em.description = embed["description"]

            if "color" in embed:
                em.color = embed["color"]

            if "timestamp" in embed:
                em.timestamp = embed["timestamp"]

            if "url" in embed:
                em.url = embed["url"]

            if "author" in embed:
                if "name" in embed["author"]:
                    author_name = embed["author"]["name"]
                else:
                    author_name = None
                    
                if "url" in embed["author"]:
                    author_url = embed["author"]["url"]
                else:
                    author_url = None

                if "icon_url" in embed["author"]:
                    author_icon_url = embed["author"]["icon_url"]
                else:
                    author_icon_url = None
                
                em.set_author(author_name, author_url, author_icon_url)
            
            if "footer" in embed:
                if "name" in embed["footer"]:
                    footer_text = embed["footer"]["text"]
                else:
                    footer_text = None
                    
                if "url" in embed["footer"]:
                    footer_icon = embed["footer"]["url"]
                else:
                    footer_icon = None
                
                if footer_icon is None:
                    em.set_footer(text=footer_text)
                else:
                    em.set_footer(text=footer_text, icon_url=footer_icon)

            if "thumbnail" in embed:
                em.set_thumbnail(embed['thumbnail']["url"])

            if "image" in embed:
                em.set_thumbnail(embed['image']["url"])

            if "fields" in embed:
                for i in embed["fields"]:
                    em.add_field(name= i["name"], value=i["value"], inline=i["inline"])

        else:
            em=None

        if "content" in json_data:
            await ctx.send(json_data["content"], embed=em)
        else:
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(CustomEmbed(client))