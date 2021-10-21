import discord
from discord.embeds import Embed
from discord.ext import commands
import aiohttp

async def get_meme():
  async with aiohttp.ClientSession() as conn:
    async with conn.get('https://www.reddit.com/r/memes/random/.json') as r:
      json = await r.json()
      parent = json[0]['data']['children'][0]['data']

      url = 'https://reddit.com{}'.format([parent['permalink']])
      img = parent['url']
      title = parent['title']
      up_votes = parent['ups']
      down_votes = parent['downs']
      comments = parent['num_comments']
      author = parent['author']

      return {
        "url":url,
        "img":img,
        "title":title,
        "up_votes":up_votes,
        "down_votes":down_votes,
        "comments":comments,
        "author":author
      }

class Reddit(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def meme(self, ctx):
    meme = await get_meme()

    em = discord.Embed()
    em.set_author(name=meme['title'])
    em.set_image(url=meme['img'])
    em.set_footer(text=f"Posted by: {meme['author']}, 👍 :{meme['up_votes']} | 👎 :{meme['down_votes']} | 💬 :{meme['comments']}")
  
def setup(client):
    client.add_cog(Reddit(client))