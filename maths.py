import re

from nextcord.ext import commands


class Maths(commands.Cog):
    """Some mathematical commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Add two numbers together\n\nUsage:\n+add 19 50",
                      brief="Addition")
    async def add(self, ctx, left: float, right: float):
        await ctx.send(f'{left:g} + {right:g} = {round((left + right), 2):g}')

    @commands.command(description="Calculates the square of a number\n\nUsage:\n+square 11",
                      brief="Squaring")
    async def square(self, ctx, number: float):
        squared_value = round((pow(number, 2)), 2)
        await ctx.send(f'{number:g}² = {squared_value:g}')

    @commands.command(description="Subtract two numbers\n\nUsage:\n+subtract 99 30",
                      brief="Subtraction")
    async def subtract(self, ctx, left: float, right: float):
        await ctx.send(f'{left:g} - {right:g} = {round((left - right), 2):g}')

    @commands.command(description="Multiply two numbers\n\nUsage:\n+multiply 35 7",
                      brief="Multiplication")
    async def multiply(self, ctx, left: float, right: float):
        await ctx.send(f'{left:g} * {right:g} = {round((left * right), 2):g}')

    @commands.command(description="Divide a number by another number\n\nUsage:\n+divide 65 5",
                      brief="Division")
    async def divide(self, ctx, dividend: float, divisor: float):
        if divisor == 0:
            await ctx.send('Division by 0 is not allowed.')
        else:
            await ctx.send(f'{dividend:g} / {divisor:g} = {round((dividend / divisor), 2):g}')

    @commands.command(description="Calculate a percentage\n\nUsage: (Result: 25%)\n+percentage 15 60",
                      brief="Percentage")
    async def percentage(self, ctx, part: float, whole: float):
        if whole == 0:
            await ctx.send("Can't have a percentage of an empty whole")
        else:
            await ctx.send(f'{part:g} / {whole:g} = {part / whole:.2%}')

    @commands.command(description="Calculate how much a percentage equates to\n\nUsage: (Result: 15)\n+percentof 25 60",
                      brief="Percent of")
    async def percentof(self, ctx, percentage, whole: float):
        percentage_re = float(re.sub('[^0-9.]', '', percentage))
        await ctx.send(f'{percentage_re:g}% of {whole:g} = {round((percentage_re / 100) * whole, 2):g}')


def setup(bot):
    bot.add_cog(Maths(bot))
