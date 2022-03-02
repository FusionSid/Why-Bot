import discord
import asyncio
from utils import plugin_enabled, get_url_json
from discord.ext import commands
from discord.ui import Button
import urllib.parse


class TriviaView(discord.ui.View):
    def __init__(self, json_response, ctx):

        self.ctx = ctx

        if json_response["difficulty"] == "easy":
            timeout = 10
        if json_response["difficulty"] == "medium":
            timeout = 15
        if json_response["difficulty"] == "hard":
            timeout = 20
    
        super().__init__(timeout=timeout)
        
        self.json = json_response
        
        self.question = json_response["question"]
        self.correct_answer = json_response["correct_answer"]
        self.answers = json_response["incorrect_answers"]
        self.answers.append(json_response["correct_answer"])
        self.category = json_response["category"]

        async def callback(interaction):
            ans = ""
            await interaction.response.send_message(f"You answered: {ans}")

        for i in self.answers:
            try:
                i = urllib.parse.unquote(i)
            except Exception as e:
                print(e)
            button = Button(label=i, style=discord.ButtonStyle.green, row=1)
            button.callback = callback
            self.add_item(button)


    async def interaction_check(self, interaction) -> bool:
      if interaction.user != self.ctx.author:
          await interaction.response.send_message("This isnt for you",ephemeral=True)
          return False
      else:
          return True

class Trivia(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = "https://opentdb.com/api.php?amount=1"

    @commands.command()
    @commands.check(plugin_enabled)
    async def trivia(self, ctx, mode : str = None):

        if mode is not None and mode in ["easy", "medium", "hard"]:

            url = self.url + f"&difficulty={mode}" +"&type=multiple"
        else:
            url = self.url +"&type=multiple"
            
        url += "&encode=url3986"
        data = await get_url_json(url)
        data = data["results"][0]

        # decode that shit
        for key, value in data.items():
            if type(value) != list:
                data[key] = urllib.parse.unquote(value)
                continue
            for item, index in enumerate(value):
                value.remove(index)
                try:
                    value.append(urllib.parse.unquote(item))
                except Exception:
                    continue

        if data["difficulty"] == "easy":
            timeout = 10
        if data["difficulty"] == "medium":
            timeout = 15
        if data["difficulty"] == "hard":
            timeout = 20

        em = discord.Embed(
            title = data["question"],
            color = ctx.author.color,
            description= f"You have `{timeout}`s to answer this question"
        )
        em.set_author(icon_url=ctx.author.avatar.url, name=f"{ctx.author.name}'s Trivia:")
        em.add_field(name="Category:", value=f"`{data['category']}`")
        em.add_field(name="Difficulty:", value=f"`{(data['difficulty']).capitalize()}`")

        view = TriviaView(data, ctx)

        message = await ctx.send(embed=em, view=view)
        await asyncio.sleep(timeout)
        for i in view.children:
            i.disabled = True
        try:
            return await message.edit(view=view)
        except Exception:
            return



def setup(client):
    client.add_cog(Trivia(client))