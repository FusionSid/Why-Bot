import time
from typing import Optional

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from core.models import WhyBot
from core.models.tag import Tag
from core.helpers.views import TagInput
from core.helpers.checks import run_bot_checks
from core.utils.formatters import discord_timestamp


class Tags(commands.Cog):
    def __init__(self, client):
        self.client: WhyBot = client
        self.cog_check = run_bot_checks

    tags = SlashCommandGroup("tags", "Command related to the tags plugin")

    async def __get_tag_by_name(self, tag_name: str, guild_id: int) -> Optional[Tag]:
        tag = await self.client.db.fetch(
            "SELECT * FROM tags WHERE guild_id=$1 AND tag_name=$2",
            guild_id,
            tag_name,
        )
        if not len(tag):
            return None

        return Tag(*tag[0][1:])

    @tags.command()
    @commands.has_permissions(administrator=True)
    async def create(
        self,
        ctx: discord.ApplicationContext,
        name: str,
    ):
        tag_name = name.lower()

        # check
        if await self.__get_tag_by_name(tag_name, ctx.guild.id) is not None:
            return await ctx.respond(
                embed=discord.Embed(
                    title="Name Conflict!",
                    description="Tag with this name already exists!\nIf you want you can edit the tag with the </tags edit:0> command",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

        # get tags value
        input = TagInput(title="Tag Value")
        await ctx.send_modal(input)
        await input.wait()

        if input.value is None:
            return await ctx.respond(
                "Not creating tag as input was either None or invalid", ephemeral=True
            )

        # create tag
        await self.client.db.execute(
            """INSERT INTO tags (
                guild_id, tag_name, tag_value, tag_author, time_created
            ) VALUES ($1, $2, $3, $4, $5)""",
            ctx.guild.id,
            tag_name,
            input.value,
            ctx.author.name,
            int(time.time()),
        )

        await ctx.respond(
            "Tag Created Successfully! It can be viewed with the </tag:0> command\nIt will look like this:",
            embed=discord.Embed(
                title=tag_name, description=input.value, color=discord.Color.random()
            ),
        )

    @tags.command()
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx: discord.ApplicationContext, name: str):
        name = name.lower()
        if await self.__get_tag_by_name(name, ctx.guild.id) is None:
            return await ctx.respond(
                embed=discord.Embed(
                    title="Tag doesn't exist!",
                    description="Tag with this name does not exist!\nYou can check tags on this server with the </tags list:0> command or create one with </tags create:0>",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

        await self.client.db.execute(
            "DELETE FROM tags WHERE guild_id=$1 AND tag_name=$2", ctx.guild.id, name
        )
        await ctx.respond(
            embed=discord.Embed(
                title="Tag Deleted",
                description=f"Tag: `{name}` was successfuly deleted!",
                color=discord.Color.green(),
            )
        )

    @tags.command()
    async def list(self, ctx: discord.ApplicationContext):
        tags = await self.client.db.fetch(
            "SELECT * FROM tags WHERE guild_id=$1", ctx.guild.id
        )
        if not len(tags):
            return await ctx.respond(
                embed=discord.Embed(
                    title="Tags",
                    description="This guild has no tags\nCreate one with </tags create:0>",
                    color=discord.Color.random(),
                )
            )

        return await ctx.respond(
            embed=discord.Embed(
                title="Tags",
                description=", ".join(
                    map(lambda tag: f"`{tag[2]}`", tags)
                ),  # tag[2] = tag_name
                color=discord.Color.random(),
            )
        )

    @tags.command()
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx: discord.ApplicationContext, name: str):
        tag_name = name.lower()

        if await self.__get_tag_by_name(tag_name, ctx.guild.id) is None:
            return await ctx.respond(
                embed=discord.Embed(
                    title="Tag doesnt exist!",
                    description="Tag with this name does not exist!\nIf you want you can create the tag with the </tags create:0> command",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

        # get tags value
        input = TagInput(title="Tag New Value")
        await ctx.send_modal(input)
        await input.wait()

        if input.value is None:
            return await ctx.respond(
                "Not editing tag as input was either None or invalid", ephemeral=True
            )

        # create tag
        await self.client.db.execute(
            "UPDATE tags SET tag_value=$1 WHERE guild_id=$2 AND tag_name=$3",
            input.value,
            ctx.guild.id,
            tag_name,
        )

        await ctx.respond(
            "Tag Modified! It will now look like this:",
            embed=discord.Embed(
                title=tag_name, description=input.value, color=discord.Color.random()
            ),
        )

    @commands.slash_command()
    async def tag(self, ctx: discord.ApplicationContext, name: str):
        name = name.lower()
        tag = await self.__get_tag_by_name(name, ctx.guild.id)
        if tag is None:
            return await ctx.respond(
                embed=discord.Embed(
                    title="Tag doesn't exist!",
                    description="Tag with this name does not exist!\nYou can check tags on this server with the </tags list:0> command or create one with </tags create:0>",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

        timestamp = await discord_timestamp(tag.time_created, "ts")
        em = discord.Embed(
            title=tag.tag_name,
            description=f"{tag.tag_value}\n\nTag created: {timestamp}",
            color=discord.Color.random(),
        )
        em.set_footer(text=f"Tag created by {tag.tag_author}")
        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Tags(client))
