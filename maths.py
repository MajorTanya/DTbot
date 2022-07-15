import re

from discord.ext import commands

from DTbot import DTbot
from util.utils import rint


class Maths(commands.Cog):
    """Some mathematical commands"""

    def __init__(self, bot: DTbot):
        self.bot = bot

    @commands.command(description="Add two numbers together\n\nUsage:\n+add 19 50",
                      brief="Addition")
    async def add(self, ctx: commands.Context, left: float, right: float):
        await ctx.send(f'{rint(left)} + {rint(right)} = {rint(left + right)}')

    @commands.command(description="Calculates the square of a number\n\nUsage:\n+square 11",
                      brief="Squaring")
    async def square(self, ctx: commands.Context, number: float):
        await ctx.send(f'{rint(number)}² = {rint(pow(number, 2))}')

    @commands.command(description="Subtract two numbers\n\nUsage:\n+subtract 99 30",
                      brief="Subtraction")
    async def subtract(self, ctx: commands.Context, left: float, right: float):
        await ctx.send(f'{rint(left)} - {rint(right)} = {rint(left - right)}')

    @commands.command(description="Multiply two numbers\n\nUsage:\n+multiply 35 7",
                      brief="Multiplication")
    async def multiply(self, ctx: commands.Context, left: float, right: float):
        await ctx.send(f'{rint(left)} * {rint(right)} = {rint(left * right)}')

    @commands.command(description="Divide a number by another number\n\nUsage:\n+divide 65 5",
                      brief="Division")
    async def divide(self, ctx: commands.Context, dividend: float, divisor: float):
        if divisor == 0:
            await ctx.send('Division by 0 is not allowed.')
        else:
            await ctx.send(f'{rint(dividend)} / {rint(divisor)} = {rint(dividend / divisor)}')

    @commands.command(description="Calculate a percentage\n\nUsage: (Result: 25%)\n+percentage 15 60",
                      brief="Percentage")
    async def percentage(self, ctx: commands.Context, part: float, whole: float):
        if whole == 0:
            await ctx.send("Can't have a percentage of an empty whole")
        else:
            await ctx.send(f'{rint(part)} / {rint(whole)} = {part / whole:.2%}')

    @commands.command(description="Calculate how much a percentage equates to\n\nUsage: (Result: 15)\n+percentof 25 60",
                      brief="Percent of")
    async def percentof(self, ctx: commands.Context, percentage, whole: float):
        percentage_re = float(re.sub('[^0-9.]', '', percentage))
        await ctx.send(f'{rint(percentage_re)}% of {rint(whole)} = {rint((percentage_re / 100) * whole)}')


async def setup(bot: DTbot):
    await bot.add_cog(Maths(bot))
