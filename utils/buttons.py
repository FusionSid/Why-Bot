import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Option

class Paginator(View):
    def __init__(self, ctx, ems):
        super().__init__(timeout=10)
        self.ctx = ctx
        self.em = ems
        self.index = 0
    
    def add(self, embed):
        self.em.append(embed)
    
    @discord.ui.button(style=discord.ButtonStyle.green, emoji="⬅", custom_id="left")
    async def left(self, button, interaction):
        if self.index == 0:
            button = [x for x in self.children if x.custom_id=="left"][0]
            button.disabled = True
        else:
            button = [x for x in self.children if x.custom_id=="right"][0]
            button.disabled = False
            self.index -= 1
        em = self.em[self.index]
        await interaction.response.edit_message(view=self,embed=em)
    
    @discord.ui.button(style=discord.ButtonStyle.green, emoji="➡️", custom_id="right")
    async def right(self, button, interaction):
        if self.index == (len(self.em)-1):
            button = [x for x in self.children if x.custom_id=="right"][0]
            button.disabled = True
        else:
            button = [x for x in self.children if x.custom_id=="left"][0]
            button.disabled = False
            self.index += 1
        em = self.em[self.index]
        await interaction.response.edit_message(view=self,embed=em)
       
    async def interaction_check(self, interaction) -> bool:
      if interaction.user != self.ctx.author:
          await interaction.response.send_message("This isnt for you",ephemeral=True)
          return False
      else:
          return True