import discord
import aiosqlite


class ClaimView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=500)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Claim", custom_id="b1")
    async def button1(self, button, interaction):
        button.style = discord.ButtonStyle.red
        button.label = "Claimed"
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("https://imgur.com/NQinKJB", ephemeral=True)

        count = 0

        async with aiosqlite.connect("database/main.db") as db:
            value = await db.execute("SELECT * FROM Other WHERE key=?", ('rickroll_count',))
            value = int((await value.fetchall())[0][1])
            count = str(value + 1)


            await db.execute("UPDATE Other Set value=? WHERE key=?", (count, 'rickroll_count',))
            await db.commit()
            
        await interaction.followup.send(f"You were the {count} person to get rick rolled", ephemeral=True)
        