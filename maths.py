import discord
from discord import app_commands
from discord.ext import commands

from DTbot import DTbot
from util.utils import rint


class Maths(commands.GroupCog):
    """Some mathematical commands"""

    def __init__(self, bot: DTbot):
        self.bot = bot

    @app_commands.command(description="Add two numbers together")
    async def add(self, interaction: discord.Interaction, first: float, second: float):
        first = rint(first, digits=3)
        second = rint(second, digits=3)
        result = rint(first + second, digits=3)
        await interaction.response.send_message(f"{first:,} + {second:,} = {result:,}")

    @app_commands.command(description="Subtract two numbers")
    async def subtract(self, interaction: discord.Interaction, first: float, second: float):
        first = rint(first, digits=3)
        second = rint(second, digits=3)
        result = rint(first - second, digits=3)
        await interaction.response.send_message(f"{first:,} - {second:,} = {result:,}")

    @app_commands.command(description="Multiply two numbers")
    async def multiply(self, interaction: discord.Interaction, first: float, second: float):
        first = rint(first, digits=3)
        second = rint(second, digits=3)
        result = rint(first * second, digits=3)
        await interaction.response.send_message(f"{first:,} * {second:,} = {result:,}")

    @app_commands.command(description="Divide a number by another number")
    async def divide(self, interaction: discord.Interaction, dividend: float, divisor: float):
        if divisor == 0:
            await interaction.response.send_message("Division by 0 is not allowed.", ephemeral=True)
        else:
            dividend = rint(dividend, digits=3)
            divisor = rint(divisor, digits=3)
            result = rint(dividend / divisor, digits=3)
            await interaction.response.send_message(f"{dividend:,} / {divisor:,} = {result:,}")

    @app_commands.command(description="Calculates the square of a number")
    async def square(self, interaction: discord.Interaction, number: float):
        number = rint(number, digits=3)
        result = rint(pow(number, 2), digits=3)
        await interaction.response.send_message(f"{number:,}² = {result:,}")

    @app_commands.command(description="Calculate a percentage (15 apples of 60? It's 25%)")
    async def percentage(self, interaction: discord.Interaction, part: float, whole: float):
        if whole == 0:
            await interaction.response.send_message("Can't have a percentage of an empty whole")
        else:
            part = rint(part, digits=3)
            whole = rint(whole, digits=3)
            result = rint(part / whole, digits=6)
            await interaction.response.send_message(f"{part:,} / {whole:,} = {result:,.2%}")

    @app_commands.command(description="Calculate how much a percentage equates to (25% of 60? It's 15)")
    async def percentof(self, interaction: discord.Interaction, percentage: float, whole: float):
        percentage = rint(percentage, digits=3)
        whole = rint(whole, digits=3)
        result = rint((percentage / 100) * whole, digits=3)
        await interaction.response.send_message(f"{percentage:,}% of {whole:,} = {result:,}")


async def setup(bot: DTbot):
    await bot.add_cog(Maths(bot))
