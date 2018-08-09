from discord.ext import commands
import re

class Maths():
    """Some mathematical commands"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="Add two numbers together",
                      brief="Addition")
    async def add(self, left : float, right : float):
        await self.bot.say(round((left + right), 2))


    @commands.command(description="Calculates the square of a number",
                      brief="Squaring")
    async def square(self, number: float):
        squared_value = round((pow(number, 2)), 2)
        await self.bot.say(str(number) + "² = " + str(squared_value))


    @commands.command(description="Subtract two numbers",
                      brief="Subtraction")
    async def subtract(self, left: float, right: float):
        await self.bot.say(round((left - right), 2))


    @commands.command(description="Multiply two numbers",
                      brief="Multiplication")
    async def multiply(self, left: float, right: float):
        await self.bot.say(round((left * right), 2))


    @commands.command(description="Divide a number by another number",
                      brief="Division")
    async def divide(self, dividend: float, divisor: float):
        if divisor == 0:
            await self.bot.say('Division by 0 is not allowed.')
        else:
            await self.bot.say(round((dividend / divisor), 2))


    @commands.command(description="Calculate a percentage",
                      brief="Percentage")
    async def percentage(self, part: float, whole: float):
        if whole == 0:
            await self.bot.say("Can't have a percentage of an empty whole")
        else:
            await self.bot.say('{0:.2f}%'.format((part / whole) * 100))


    @commands.command(description="Calculate how much a percentage equates to",
                      brief="Percent of")
    async def percentof(self, percentage, whole: float):
        percentage_re = float(re.sub('[^0-9.]', '', percentage))
        await self.bot.say(round((percentage_re / 100) * whole, 2))


def setup(bot):
    bot.add_cog(Maths(bot))
