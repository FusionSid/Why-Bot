import discord

async def update_activity(client):
    await client.change_presence(activity=discord.Game(f"On {len(client.guilds)} servers! | ?help"))

async def get_log_channel(self, ctx):
    data = await self.client.get_db()
    if data[str(ctx.guild.id)]['log_channel'] is None:
        return None
    channel = data[str(ctx.guild.id)]['log_channel']
    return await self.client.fetch_channel(channel)