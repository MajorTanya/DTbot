import re

from discord.ext import commands


class Maths():
    """Some mathematical commands"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="Add two numbers together\n\nUsage:\n+add 19 50",
                      brief="Addition")
    async def add(self, left: float, right: float):
        await self.bot.say(round((left + right), 2))


    @commands.command(description="Calculates the square of a number\n\nUsage:\n+square 11",
                      brief="Squaring")
    async def square(self, number: float):
        squared_value = round((pow(number, 2)), 2)
        await self.bot.say(str(number) + "² = " + str(squared_value))


    @commands.command(description="Subtract two numbers\n\nUsage:\n+subtract 99 30",
                      brief="Subtraction")
    async def subtract(self, left: float, right: float):
        await self.bot.say(round((left - right), 2))


    @commands.command(description="Multiply two numbers\n\nUsage:\n+multiply 35 7",
                      brief="Multiplication")
    async def multiply(self, left: float, right: float):
        await self.bot.say(round((left * right), 2))


    @commands.command(description="Divide a number by another number\n\nUsage:\n+divide 65 5",
                      brief="Division")
    async def divide(self, dividend: float, divisor: float):
        if divisor == 0:
            await self.bot.say('Division by 0 is not allowed.')
        else:
            await self.bot.say(round((dividend / divisor), 2))


    @commands.command(description="Calculate a percentage\n\nUsage: (Result: 25%)\n+percentage 15 60",
                      brief="Percentage")
    async def percentage(self, part: float, whole: float):
        if whole == 0:
            await self.bot.say("Can't have a percentage of an empty whole")
        else:
            await self.bot.say('{0:.2f}%'.format((part / whole) * 100))


    @commands.command(description="Calculate how much a percentage equates to\n\nUsage: (Result: 15)\n+percentof 25 60",
                      brief="Percent of")
    async def percentof(self, percentage, whole: float):
        percentage_re = float(re.sub('[^0-9.]', '', percentage))
        await self.bot.say(round((percentage_re / 100) * whole, 2))


def setup(bot):
    bot.add_cog(Maths(bot))
