import discord
import datetime
import shlex
import aiohttp

colors = {
    "none" : None,
    "blue": discord.Color.blue(),
    "blurple": discord.Color.blurple(),
    "brand_green": discord.Color.brand_green(),
    "brand_red": discord.Color.brand_red(),
    "dark_blue": discord.Color.dark_blue(),
    "dark_gold": discord.Color.dark_gold(),
    "dark_gray": discord.Color.dark_gray(),
    "dark_green": discord.Color.dark_green(),
    "dark_grey": discord.Color.dark_grey(),
    "dark_magenta": discord.Color.dark_magenta(),
    "dark_orange": discord.Color.dark_orange(),
    "dark_purple": discord.Color.dark_purple(),
    "dark_red": discord.Color.dark_red(),
    "dark_teal": discord.Color.dark_teal(),
    "dark_theme": discord.Color.dark_theme(),
    "darker_gray": discord.Color.darker_gray(),
    "darker_grey": discord.Color.darker_grey(),
    "fuchsia": discord.Color.fuchsia(),
    "gold": discord.Color.gold(),
    "green": discord.Color.green(),
    "greyple": discord.Color.greyple(),
    "light_gray": discord.Color.light_gray(),
    "light_grey": discord.Color.light_grey(),
    "lighter_gray": discord.Color.lighter_gray(),
    "lighter_grey": discord.Color.lighter_grey(),
    "magenta": discord.Color.magenta(),
    "nitro_pink": discord.Color.nitro_pink(),
    "og_blurple": discord.Color.og_blurple(),
    "orange": discord.Color.orange(),
    "purple": discord.Color.purple(),
    "random": discord.Color.random(),
    "red": discord.Color.red(),
    "teal": discord.Color.teal(),
}

async def kwarg_to_embed(client, ctx, kwargs):

        colorlist = []
        for c in colors:
            colorlist.append(c)
            
        def wait_for_check(m):
            return m.author == ctx.author and m.channel == ctx.message.channel

        em = discord.Embed()
        em.timestamp = datetime.datetime.utcnow()

        kwargs = shlex.split(kwargs)
        args = {}

        for index in range(len(kwargs)):
            if index % 2 == 0:
                args[kwargs[index].lstrip("--")] = kwargs[index+1]
            index += 0

        channel = ctx.message.channel
        webhook_dict = {
                    "name" : None,
                    "avatar" : None,
                }

        for key, value in args.items():
            if key.lower() == "title":
                em.title = value
            elif key.lower() == "description" or key.lower() == "desc":
                em.description = value
            elif key.lower() == "channel":
                channel = await client.fetch_channel(int(value))
            elif key.lower() == "img" or key.lower() == "image":
                em.set_image(url=value)
            elif key.lower() == "color" or key.lower() == "colour":
                if value.lower() == "list" or value.lower() == "help":
                    return await ctx.send(", ".join(colorlist))
                if value.lower() not in colorlist:
                    await ctx.send("Color not found", delete_after=2)
                    em.color = ctx.author.color
                else:
                    em.color = colors[value.lower()]
            elif key.lower() == "fields":
                vint = False
                try:
                    int(value) 
                    vint= True
                except:
                    vint = False
                
                if vint is True:
                    for i in range(int(value)):
                        entername = await ctx.send("Enter Name:")
                        name = await client.wait_for("message", check=wait_for_check, timeout=300)
                        await name.delete()

                        entervalue = await ctx.send("Enter Value:")
                        value = await client.wait_for("message", check=wait_for_check, timeout=300)
                        await entername.delete()
                        await entervalue.delete()
                        await value.delete()

                        em.add_field(name=name.content, value=value.content, inline=False)
                        
            elif key.lower() in ["timestamp", "time"] and value.lower() in ["true", "yes"]:
                em.timestamp = datetime.datetime.now()

            elif key.lower() == "webhook_name":
                webhook_dict['name'] = value
            
            elif key.lower() == "webhook_avatar":
                webhook_dict['avatar'] = value

        if ctx.author.id != client.owner_id:
            em.set_footer(text=f"Message sent by {ctx.author.name}")
        
        name, avatar = None, None
        if webhook_dict["name"] is not None:
            name = webhook_dict["name"]
            
            if webhook_dict["avatar"] is not None:
                async with aiohttp.ClientSession() as session:
                    async with session.get(webhook_dict["avatar"]) as resp:
                        avatar = bytes(await resp.read())

            webhook = await channel.create_webhook(name=name, avatar=avatar)
            await webhook.send(embed=em)
            await webhook.delete()
            return None
        
        return [em, channel]
