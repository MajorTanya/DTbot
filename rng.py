import random
import re

import discord
import rolldice
from discord.ext import commands


class RNG:
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


    @commands.command(description='Choose one of multiple choices.'
                                  'With options containing spaces, use double quotes like:\n'
                                  '+choose "Make Pizza" Fish "Go to the cafeteria"',
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


    @commands.command(pass_context=True,
                      description="Rolls a dice in NdN format. (1d6 is rolling a standard, six-sided die once. "
                                  "3d20 rolls a twenty-sided die three times.)\n\n"
                                  "Supports NdNx format for 'Drop Lowest' style. The x needs to be lowercase.\n"
                                  "(4d6x rolls 4 six-sided dice and removes the lowest roll from the sum.)\n"
                                  "Supports NdN + N format for adding modifiers.\n"
                                  "(1d12 + 2 rolls a 12-sided die once and adds 2 to the sum.)\n\n"
                                  "NdNx + N is supported. "
                                  "Does NOT currently support any other CritDice formats.",
                      brief="Rolls a die in NdN format")
    async def roll(self, ctx, *, dice):
        total = 0
        modification = ent_modif = ""
        try:
            result, explanation = rolldice.roll_dice("".join(dice))
            explanation = explanation.replace(",", ", ")

            if "x" in dice:
                explanation, *modification = explanation.split("] ", 1)
                if modification:
                    operator = re.search(r'([+|-])', str(modification).strip())
                    modifier = re.sub(r'[^0-9]', "", str(modification))
                    ent_modif = str(operator.group(1)) + str(modifier)
                explanation += "]"
                explanation = re.sub(r' ~~ ([0-9]+)', " ~~(\\1)~~", explanation).replace("]]", "]")
                result = re.sub(r' ~~(\([0-9]\))~~', "", explanation).strip('[]').split(', ')
                for i in result:
                    total = total + int(i)
                result = total
                if ent_modif:
                    result = eval(str(result) + ent_modif)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), title="Result: __" + str(result) + "__",
                                  description=str(explanation) + " " + str(modification).strip("[']"))
            embed.set_footer(text="Rolled " + dice)
            await self.bot.say(embed=embed)
        except rolldice.DiceGroupException as e:
            helper = self.bot.formatter.format_help_for(ctx, self.bot.get_command("roll"))
            for h in helper:
                em = discord.Embed(title="Format has to be NdN or NdNx or NdN+N or NdNx+N.",
                                   description=h.strip("```").replace('<', '[').replace('>', ']'),
                                   color=discord.Color.red())
                em.set_footer(text=str(e))
                await self.bot.say(embed=em)


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


    @commands.command(description="Play some French Roulette (bet optional)\n\n"
                                  "For a nicer overview of the distribution of numbers across the colors, use "
                                  "+show roulette\n\n"
                                  "Red:       1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36\n"
                                  "Black:     2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35\n"
                                  "No colour: 0\n\n"
                                  "Bet options: No Bet / Straight bet (Red 3) / Color Bet (Red) / Even/Odd Bet (Odd)"
                                  "\n\nUsage:\n+roulette OR +roulette Red 3 OR +roulette 0 OR +roulette Odd",
                      brief="Play some Roulette")
    async def roulette(self, *bet):
        black = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35)
        red = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
        randnum = random.randint(0, 36)
        if not randnum == 0:
            result_even = (randnum % 2) == 0
            if result_even:
                result_eo = "Even"
            else:
                result_eo = "Odd"
        else:
            result_even = None
            result_eo = None
        result_n = str(randnum)
        win_type = None
        if randnum not in black:
            if randnum not in red:
                result_n = "0"
                result_c = None
            else:
                result_c = "Red"
        else:
            result_c = "Black"

        if result_c:
            full_result_no_eo = result_c + " " + result_n
        else:
            full_result_no_eo = result_n
        if result_eo:
            full_result_eo = full_result_no_eo + " ({})".format(result_eo)
        else:
            full_result_eo = full_result_no_eo

        if bet:
            user_bet = ' '.join(bet).strip().lower()
            if "even" in user_bet:
                if result_even:
                    win_type = "n Even Bet"
                else:
                    win_type = None
            elif "odd" in user_bet:
                if result_even is False:
                    win_type = "n Odd Bet"
                else:
                    win_type = None

            else:
                user_bet_n = ''.join(x for x in user_bet if x.isdigit())
                if user_bet_n == '':
                    user_bet_n = None
                    user_bet_c = user_bet
                elif user_bet_n == '0':
                    user_bet_c = None
                else:
                    user_bet_c = user_bet.split(" ", 1)
                    user_bet_c = user_bet_c[0]

                if result_c:
                    if user_bet_c:
                        full_bet = user_bet_c + " " + str(user_bet_n)
                    else:
                        full_bet = user_bet_n

                    if user_bet_n:
                        if full_result_no_eo.lower() == full_bet:
                            win_type = " Straight Bet"
                    else:
                        if result_c.lower() == user_bet_c.lower():
                            win_type = " Bet on " + result_c
                else:
                    if full_result_no_eo == user_bet_n:
                        win_type = " Straight Bet"
            print(str(win_type))
            if win_type:
                message = full_result_eo + "\n**You win with a{}!**".format(win_type)
            else:
                message = full_result_eo + "\n**You lost!**"
        else:
            message = full_result_eo
        await self.bot.say(message)


    @commands.group(hidden=True,
                    pass_context=True,
                    description="")
    async def show(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @show.command(pass_context=True,
                  name="roulette",
                  description="")
    async def _roulette(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="Distribution of numbers and colors on the French Roulette table:\n")
        embed.set_image(url="https://i.imgur.com/jtMZJXR.png")
        await self.bot.say(embed=embed)


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


    @commands.command(description='Find out how shippable your ship is\n\nUsage:\n'
                                  '+ship The entire internet and pineapple on pizza',
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
