import discord

class LinkView(discord.ui.View):
    def __init__(self, link:str, label:str):
        """
        This function creates a view with a single button. The button has a link in it.

        Args:
        link (str) : The link the button will take you to
        label (str) : The label of the button
        """
        super().__init__(timeout=180)
        
        button = discord.ui.Button(style=discord.ButtonStyle.grey, label=label, url=link)

        self.add_item(button)
