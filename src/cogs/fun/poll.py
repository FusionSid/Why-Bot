import asyncio
import time as pytime

import discord
from discord.utils import get
from discord.ext import commands

from core.models import WhyBot
from core.helpers.checks import run_bot_checks
from core.utils.formatters import discord_timestamp


class Poll(commands.Cog):
    def __init__(self, client: WhyBot):
        self.client = client
        self.cog_check = run_bot_checks

    @commands.slash_command(description="Makes a Yah or Nah poll")
    @commands.guild_only()
    async def yesorno(self, ctx, message: str):
        msg = await ctx.respond(
            embed=discord.Embed(
                title="Yah or Nah?", description=message, color=ctx.author.color
            )
        )
        msg = await msg.original_message()
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.slash_command()
    @commands.guild_only()
    async def poll(
        self,
        ctx,
        title: str,
        choice1: str,
        choice2: str,
        choice3: str = None,
        choice4: str = None,
        choice5: str = None,
        choice6: str = None,
        choice7: str = None,
        choice8: str = None,
        choice9: str = None,
        choice10: str = None,
        end_poll_in: str = None,
    ):
        await ctx.defer()
        options = [
            i
            for i in [
                choice1,
                choice2,
                choice3,
                choice4,
                choice5,
                choice6,
                choice7,
                choice8,
                choice9,
                choice10,
            ]
            if i is not None
        ]
        numbers = {
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
            10: "🔟",
        }
        reactions_todo = []
        desc = ""
        for index, option in enumerate(options):
            emoji = numbers[index + 1]
            desc += f"\n{emoji} {option}"
            reactions_todo.append(emoji)

        em = discord.Embed(
            title=f'{ctx.author.name} asks: "{title}"',
            description=desc,
            color=discord.Color.random(),
        )

        if end_poll_in is not None:
            if end_poll_in.isnumeric():
                time = int(end_poll_in)
            else:
                seconds_per_unit = {"m": 60, "h": 3600, "d": 86400, "w": 604800}
                try:
                    time = int(end_poll_in[:-1]) * seconds_per_unit[end_poll_in[-1]]
                    if time > 604800:
                        return await ctx.respond(
                            "Poll failed to be created"
                            f" {self.client.get_why_emojies['redcross']}\nTime can not"
                            " be longer than a week",
                            ephemeral=True,
                        )
                except ValueError:
                    return await ctx.respond(
                        "Poll failed to be created"
                        f" {self.client.get_why_emojies['redcross']}\nThe format code"
                        " was not found",
                        ephemeral=True,
                    )

            timern = pytime.time()

            em.add_field(
                name="Voting ends in:",
                value=await discord_timestamp(int(timern + time), "ts"),
            )

        message = await ctx.send(embed=em)
        await ctx.respond(
            f"Poll created successfuly {self.client.get_why_emojies['checkmark']}",
            ephemeral=True,
        )
        for reaction in reactions_todo:
            await message.add_reaction(reaction)

        if end_poll_in is None:
            return

        await asyncio.sleep(time)

        message_later = await ctx.channel.fetch_message(message.id)
        results = {}
        for i in reactions_todo:
            reaction = get(message_later.reactions, emoji=i)
            count = reaction.count - 1
            results[i] = f"{count} vote{'s' if count > 1 else ''}"

        results = "\n".join([f"{key} got {value}" for key, value in results.items()])
        embed = discord.Embed(
            title=f'Poll results for: "{title}"',
            description=f"**Votes:**\n {results}",
            color=ctx.author.color,
        )
        embed.set_footer(text="Voting is closed")
        try:
            await message.clear_reactions()
        except discord.HTTPException:
            pass
        return await message.edit(embed=embed)


def setup(client):
    client.add_cog(Poll(client))
