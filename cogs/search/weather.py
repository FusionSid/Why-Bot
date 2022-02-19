import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import datetime
from utils import get_url_json, plugin_enabled

load_dotenv()

class Dropdown(discord.ui.Select):
    def __init__(self, embeds):
        self.embeds = embeds
        options = [
            discord.SelectOption(label="General", description="Weather"),
            discord.SelectOption(label="Temperature", description="Temperature info"),
            discord.SelectOption(label="Info", description="More info on weather"),
            discord.SelectOption(label="Sunrise/Sunset", description="Sunrise and sunset"),
        ]

        super().__init__(
            placeholder="More Info...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "General":
            em = self.embeds[0]
        elif self.values[0] == "Temperature":
            em = self.embeds[1]
        elif self.values[0] == "Info":
            em = self.embeds[2]
        elif self.values[0] == "Sunrise/Sunset":
            em = self.embeds[3]
        await interaction.response.edit_message(embed=em)


class DropdownView(discord.ui.View):
    def __init__(self, embeds):
        super().__init__(timeout=100)
        self.add_item(Dropdown(embeds))

async def get_weather_data(city):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = os.environ['WEATHER']
    
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"

    data = await get_url_json(url)

    return data

async def format_weather_data(data):
    weather = data['weather'][0]
    main = data['main']
    info = data['sys']
    name = data['name']

    em1 = discord.Embed(
        title = "Weather Info:",
        description="General",
        color = discord.Color.random()
    )

    em1.add_field(
        name = "City:",
        value = name
    )
    
    em1.add_field(
        name = "Country:",
        value = info['country']
    )

    em1.add_field(
        name = "Weather Type:",
        value = weather['main']
    )

    em2 = discord.Embed(
        title   = "Weather Info:",
        description="Temperature",
        color = discord.Color.random()
    )

    em2.add_field(
        name = "Temperature:",
        value = f"{round(main['temp'])}°"    
    )

    em2.add_field(
        name = "Min/Max",
        value = f"{round(main['temp_min'])}° | {round(main['temp_max'])}°"
    )

    em2.add_field(
        name = "Feels Like:",
        value = f"{round(main['feels_like'])}°"
    )

    em3 = discord.Embed(
        title = "Weather Info:",
        description="Info",
        color = discord.Color.random()
    )

    em3.add_field(name="Wind Speed:", value=str(data['wind']['speed'])+"m/s")
    em3.add_field(name="Wind Direction:", value=str(data['wind']["deg"])+"°")
    em3.add_field(name="Pressure:", value=str(main['pressure'])+"hPa")
    em3.add_field(name="Humidity:", value=str(main["humidity"])+"%")

    em4 = discord.Embed(
        title = "Weather Info:",
        description="Sunrise/Sunset",
        color = discord.Color.random()
    )

    em4.add_field(
        name = "Sunrise:",
        value=f"<t:{info['sunrise']}:R>"
    )

    em4.add_field(
        name = "Sunset:",
        value=f"<t:{info['sunset']}:R>"
    )

    em1.timestamp = datetime.datetime.now()
    em2.timestamp = datetime.datetime.now()
    em3.timestamp = datetime.datetime.now()
    em4.timestamp = datetime.datetime.now()

    return [em1, em2, em3, em4]

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.command(usage = "weather [city]", description = "Get weather", help = "Gets the weather for a city", extras={"category": "Search"})
    @commands.check(plugin_enabled)
    async def weather(self, ctx, *, city):
        data = await get_weather_data(city)
        embeds = await format_weather_data(data)
        view = DropdownView(embeds)
        await ctx.send(embed=embeds[0], view=view)


def setup(client):
    client.add_cog(Weather(client))

