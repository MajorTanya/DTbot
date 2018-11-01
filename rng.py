import random
import re

import discord
from discord.ext import commands


class RNG():
    """Randomness commands"""

    def __init__(self, bot):
        self.bot = bot


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
                'Nope',
                'YES',
                'Kind of',
                'HELL NO'
                ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description='Choose one of multiple choices. With options containing spaces, use double quotes like:\n+choose "Make Pizza" Fish "Go to the cafeteria"',
                      brief='Let the bot decide for you',
                      aliases=['choice'])
    async def choose(self, *choices: str):
        await self.bot.say(random.choice(choices))


    @commands.command(description="Flips a coin",
                      brief="Flip a coin")
    async def coinflip(self):
        possible_responses = [
                'Heads',
                'Tails'
                ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description='Says something random',
                      brief='Says something random')
    async def random(self):
        possible_responses = [
                'Franxx',
                'Nope',
                'Mom',
                'Dead',
                'Heh',
                'No u',
                'Darling'
                ]
        await self.bot.say(random.choice(possible_responses))
    # D:YES I ONLY ADDED IT CUZ I WANTENTED TO ADD SOMETHING ABOUT DARLING IN THE FRANXX
    # D:TAKE ME TO COURT IF U WANT TO


    @commands.command(description="Rolls a dice in NdN format. (1d6 is rolling a standard, six-sided die once. 3d20 rolls a twenty-sided die three times.)",
                      brief="Rolls a die in NdN format")
    async def roll(self, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN.')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)


    @commands.command(description="It's Russian Roulette",
                      brief="Play some Russian Roulette",
                      aliases=['russianroulette', 'rusroulette'])
    async def rroulette(self):
        possible_responses = [
                'Dead',
                'Alive',
                'Alive',
                'Alive',
                'Alive'
                ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(pass_context=True,
                      brief="Play some Roulette",
                      description="Play some French Roulette (bet optional)\n\nRed:       1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36\nBlack:     2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35\nNo colour: 0\n\nUsage:\n+roulette OR +roulette Red 3 OR +roulette 0")
    async def roulette(self, ctx, bet=None):
        black = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35)
        red = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
        randnum = random.randint(0, 36)
        if randnum not in black:
            if randnum not in (red):
                result = "0"
            else:
                result = "Red " + str(randnum)
        else:
            result = "Black " + str(randnum)
        if bet is not None:
            if bet.lower() == result.lower():
                result = result + "\n**You win!**"
            else:
                result = result + "\n**You lose!**"
        await self.bot.say(result)


    @commands.command(description="Gives you a random scenario",
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
                'Rech got stepped on',
                "Exo tried to get banned but wasn't"
                ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description='Find out how shippable your ship is\n\nUsage:\n+ship The entire internet and pineapple on pizza',
                      brief='Ship things')
    async def ship(self, *ship):
        ship = ' '.join(ship)
        split = re.split(" and ", ship, 1, flags=re.IGNORECASE)
        shipping = random.random() * 100
        if shipping < 50:
            emote_choice = ":broken_heart:"
        else:
            emote_choice = ":heart:"
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="" + split[0] + " and " + split[1] + "? `{0:.2f}%` shippable. ".format(shipping) + emote_choice)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(RNG(bot))
