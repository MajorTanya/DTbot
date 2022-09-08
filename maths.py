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
    async def add(self, interaction: discord.Interaction, left: float, right: float):
        await interaction.response.send_message(f'{rint(left):g} + {rint(right):g} = {rint(left + right)}')

    @app_commands.command(description="Calculates the square of a number")
    async def square(self, interaction: discord.Interaction, number: float):
        await interaction.response.send_message(f'{rint(number)}² = {rint(pow(number, 2))}')

    @app_commands.command(description="Subtract two numbers")
    async def subtract(self, interaction: discord.Interaction, first: float, second: float):
        await interaction.response.send_message(f'{rint(first)} - {rint(second)} = {rint(first - second)}')

    @app_commands.command(description="Multiply two numbers")
    async def multiply(self, interaction: discord.Interaction, first: float, second: float):
        await interaction.response.send_message(f'{rint(first)} * {rint(second)} = {rint(first * second)}')

    @app_commands.command(description="Divide a number by another number")
    async def divide(self, interaction: discord.Interaction, dividend: float, divisor: float):
        if divisor == 0:
            await interaction.response.send_message('Division by 0 is not allowed.', ephemeral=True)
        else:
            await interaction.response.send_message(f'{rint(dividend)} / {rint(divisor)} = {rint(dividend / divisor)}')

    @app_commands.command(description="Calculate a percentage (15 apples of 60? It's 25%)")
    async def percentage(self, interaction: discord.Interaction, part: float, whole: float):
        if whole == 0:
            await interaction.response.send_message("Can't have a percentage of an empty whole")
        else:
            await interaction.response.send_message(f'{rint(part)} / {rint(whole)} = {rint(part / whole, 4):.2%}')

    @app_commands.command(description="Calculate how much a percentage equates to (25% of 60? It's 15)")
    async def percentof(self, interaction: discord.Interaction, percentage: float, whole: float):
        await interaction.response.send_message(f'{rint(percentage)}% of {rint(whole)}'
                                                f' = {rint((percentage / 100) * whole)}')


async def setup(bot: DTbot):
    await bot.add_cog(Maths(bot))
