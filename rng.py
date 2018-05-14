import random
from discord.ext import commands

class RNG():
    """Randomness commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, dice : str):
        """Rolls a dice in NdN format. (1d6 is rolling a standard, six-sided dice once. 3d20 roll a twenty-sided dice three times.)"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)


    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, *choices : str):
        """Chooses between multiple choices."""
        await self.bot.say(random.choice(choices))


    @commands.command(description="It's Russian Roulette",
                      brief="Play some Russian Roulette",
                      aliases=['russianroulette'])
    async def roulette(self):
        possible_responses = [
                'Dead',
                'Alive',
                'Alive',
                'Alive',
                'Alive'
                ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(name='8ball',
                      description="Answers a yes/no question.",
                      brief="Answers from the beyond.")
    async def _eightball(self):
        possible_responses = [
                'Yes',
                'Maybe',
                'No',
                'Probably',
                'Nah',
                'No way',
                'Nope'
                ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Flips a coin",
                      brief="Flip a coin")
    async def coinflip(self):
        possible_responses = [
                'Heads',
                'Tails'
                ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="WOW YOU MUST BE DUMB TO NOT GET THAT",
                      brief="Gives you a random scenario")
    async def scenario(self):
        possible_responses = [
                'Nishi now owns the server',
                'Zero sold you for a plane',
                'Berend made you watch bad porn',
                'Tanya killed you for hurting Nishi',
                'Josh removed a kebab',
                'You got hacked',
                '<.<',
                'Nishi just took over the world',
                'Cutie Joey got his cheeks pinched',
                'Rech got stepped on'
                ]
        await self.bot.say(random.choice(possible_responses))


def setup(bot):
    bot.add_cog(RNG(bot))
