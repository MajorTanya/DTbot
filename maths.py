import random
from discord.ext import commands

class Maths():
    """Some mathematical commands"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="Add two numbers together",
                      brief="Addition")
    async def add(self, left : int, right : int):
        """Adds two numbers together."""
        await self.bot.say(left + right)


    @commands.command(description='Calculates the square of a whole number',
                      brief='Square a (whole) number')
    async def square(self, number):
        squared_value = pow(int(number), 2)
        await self.bot.say(str(number) + "² = " + str(squared_value))


    @commands.command(description="Subtract two numbers",
                      brief="Subtraction")
    async def subtract(self, left: int, right: int):
        await self.bot.say(left - right)


    @commands.command(description="Multiply two numbers",
                      brief="Multiplication")
    async def multiply(self, left: int, right: int):
        await self.bot.say(left * right)


    @commands.command(description="Divide a number by another number",
                      brief="Division")
    async def divide(self, dividend: int, divisor: int):
        if divisor == 0:
            await self.bot.say('Division by 0 is not allowed.')
        else:
            await self.bot.say(dividend / divisor)


    @commands.command(description="Calculate a percentage",
                      brief="Percentage")
    async def percentage(self, part: int, whole: int):
        if whole == 0:
            await self.bot.say("Can't have a percentage of an empty whole")
        else:
            await self.bot.say('{0:.2f}%'.format((part / whole * 100)))

def setup(bot):
    bot.add_cog(Maths(bot))
