import discord
from discord import app_commands
from discord.ext import commands

from DTbot import DTbot
from util.utils import rint

CM_IN_INCH = 2.54
KM_IN_MI = 1.609344
M_IN_FT = 0.3048
KG_IN_LBS = 0.45359237
ML_IN_USFLOZ = 29.57353
L_IN_USGAL = 3.785411784


class Conversion(commands.Cog):
    """Convert units, especially Metric and US Customary / Imperial"""

    def __init__(self, bot: DTbot):
        self.bot = bot

    @app_commands.command(description="Converts °Celsius to °Fahrenheit")
    @app_commands.describe(celsius="The temperature in °C")
    async def cf(self, interaction: discord.Interaction, celsius: float):
        fahrenheit = rint(celsius * 1.8 + 32)
        await interaction.response.send_message(f'{rint(celsius)}°C = {fahrenheit}°F')

    @app_commands.command(description="Converts °Fahrenheit to °Celsius")
    @app_commands.describe(fahrenheit="The temperature in °F")
    async def fc(self, interaction: discord.Interaction, fahrenheit: float):
        celsius = rint((fahrenheit - 32) / 1.8)
        await interaction.response.send_message(f'{rint(fahrenheit)}°F = {celsius}°C')

    @app_commands.command(description="Converts Centimeters to Inches")
    @app_commands.describe(centimeters="The value in Centimeters")
    async def cmin(self, interaction: discord.Interaction, centimeters: float):
        inches = rint(centimeters / CM_IN_INCH)
        await interaction.response.send_message(f'{rint(centimeters)} cm  = {inches} inch')

    @app_commands.command(description="Converts Inches to Centimeters")
    @app_commands.describe(inches="The value in Inches")
    async def incm(self, interaction: discord.Interaction, inches: float):
        centimeters = rint(inches * CM_IN_INCH)
        await interaction.response.send_message(f'{rint(inches)} inch  = {centimeters} cm')

    @app_commands.command(description="Converts from Centimeters to Feet")
    @app_commands.describe(centimeters="The value in Centimeters")
    async def cmft(self, interaction: discord.Interaction, centimeters: float):
        feet = rint(centimeters / (M_IN_FT * 100))
        await interaction.response.send_message(f'{rint(centimeters)} cm = {feet} ft')

    @app_commands.command(description="Converts from Feet to Centimeters")
    @app_commands.describe(feet="The value in Feet")
    async def ftcm(self, interaction: discord.Interaction, feet: float):
        centimeters = rint(feet * (M_IN_FT * 100))
        await interaction.response.send_message(f'{rint(feet)} ft = {centimeters} cm')

    @app_commands.command(description="Converts from Feet to Meters")
    @app_commands.describe(feet="The value in Centimeters")
    async def ftm(self, interaction: discord.Interaction, feet: float):
        meters = rint(feet * M_IN_FT)
        await interaction.response.send_message(f'{rint(feet)} ft = {meters} m')

    @app_commands.command(description="Converts from Meters to Feet")
    @app_commands.describe(meters="The value in Meters")
    async def mft(self, interaction: discord.Interaction, meters: float):
        feet = rint(meters / M_IN_FT)
        await interaction.response.send_message(f'{rint(meters)} m = {feet} ft')

    @app_commands.command(description="Converts from mixed Feet and Inches to Meters")
    @app_commands.describe(feet="The Feet part of the value")
    @app_commands.describe(inches="The Inches part of the value")
    async def ftinm(self, interaction: discord.Interaction, feet: float, inches: float):
        meters = rint(feet * M_IN_FT) + rint(inches * (CM_IN_INCH / 100))
        await interaction.response.send_message(f'{rint(feet)} ft {rint(inches)} in = {meters} m')

    @app_commands.command(description="Converts from Meters to mixed Feet and Inches")
    @app_commands.describe(meters="The value in Meters")
    async def mftin(self, interaction: discord.Interaction, meters: float):
        divmodres = divmod(meters, M_IN_FT)
        inches = divmodres[1] / (CM_IN_INCH * 100)
        await interaction.response.send_message(f'{rint(meters)} m = {int(divmodres[0])} ft '
                                                f'{rint(inches)} in')

    @app_commands.command(description="Converts from Kilometers to Miles")
    @app_commands.describe(kilometers="The value in Kilometers")
    async def kmmi(self, interaction: discord.Interaction, kilometers: float):
        miles = rint(kilometers / KM_IN_MI)
        await interaction.response.send_message(f'{rint(kilometers)} km = {miles} mi')

    @app_commands.command(description="Converts from Miles to Kilometers")
    @app_commands.describe(miles="The value in Miles")
    async def mikm(self, interaction: discord.Interaction, miles: float):
        kilometers = rint(miles / KM_IN_MI)
        await interaction.response.send_message(f'{rint(miles)} mi = {kilometers} km')

    @app_commands.command(description="Converts from Kilograms to Pounds")
    @app_commands.describe(kilograms="The value in Kilograms")
    async def kglbs(self, interaction: discord.Interaction, kilograms: float):
        pounds = rint(kilograms / KG_IN_LBS)
        await interaction.response.send_message(f'{rint(kilograms)} kg = {pounds} lbs')

    @app_commands.command(description="Converts from Pounds to Kilograms")
    @app_commands.describe(pounds="The value in Pounds (lbs)")
    async def lbskg(self, interaction: discord.Interaction, pounds: float):
        kilograms = rint(pounds * KG_IN_LBS)
        await interaction.response.send_message(f'{rint(pounds)} lbs = {kilograms} kg')

    @app_commands.command(description="Converts from US Fluid Ounces to Milliliters")
    @app_commands.describe(floz="The value in US Fluid Ounces (fl oz)")
    async def flozml(self, interaction: discord.Interaction, floz: float):
        milliliters = rint(floz * ML_IN_USFLOZ)
        await interaction.response.send_message(f'{rint(floz)} fl oz (US) = {milliliters} mL')

    @app_commands.command(description="Converts from Milliliters to US Fluid Ounces")
    @app_commands.describe(milliliters="The value in Milliliters")
    async def mlfloz(self, interaction: discord.Interaction, milliliters: float):
        floz = rint(milliliters / ML_IN_USFLOZ)
        await interaction.response.send_message(f'{rint(milliliters)} mL = {floz} fl oz (US)')

    @app_commands.command(description="Converts from US Gallons to Liters")
    @app_commands.describe(gallons="The value in US Gallons")
    async def gall(self, interaction: discord.Interaction, gallons: float):
        liters = rint(gallons / L_IN_USGAL)
        await interaction.response.send_message(f'{rint(gallons)} gal (US) = {liters} L')

    @app_commands.command(description="Converts from Liters to US Gallons")
    @app_commands.describe(liters="The value in Liters")
    async def lgal(self, interaction: discord.Interaction, liters: float):
        gallons = rint(liters * L_IN_USGAL)
        await interaction.response.send_message(f'{rint(liters)} L = {gallons} gal (US)')


async def setup(bot: DTbot):
    await bot.add_cog(Conversion(bot))
