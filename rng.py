import random
import re

import nextcord
import rolldice
from nextcord.ext import commands


def roulettecolourfinder(n, black):
    if n == 0:
        return "0"
    return f"Black {n}" if n in black else f"Red {n}"


class Rng(commands.Cog, name='RNG'):
    """Randomness-based commands, such as rolling dice"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball',
                      description="Answers a yes/no question.",
                      brief="Answers from the beyond.")
    async def _eightball(self, ctx):
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
            'HELL NO',
            'What if?',
            'It is certain.',
            'Ask again later.',
            'Don\'t count on it',
            'Without a doubt.',
            'Replay hazy, try again later'
        ]
        await ctx.send(random.choice(possible_responses))

    @commands.command(description='Choose one of multiple choices. '
                                  'With options containing spaces, use double quotes like:\n'
                                  '+choose "Make Pizza" Fish "Go to the cafeteria"',
                      brief='Let the bot decide for you',
                      aliases=['choice'])
    async def choose(self, ctx, *choices: str):
        try:
            await ctx.send(random.choice(choices))
        except IndexError:
            await ctx.send('You have to provide me with something to actually choose from though...')

    @commands.command(description="Flips a coin",
                      brief="Flip a coin")
    async def coinflip(self, ctx):
        await ctx.send(random.choice(['Heads', 'Tails']))

    @commands.command(description="Rolls dice in NdN format. (1d6 is rolling a standard, six-sided die once. "
                                  "3d20 rolls three twenty-sided dice.)\n\nSupported formats:\n"
                                  "- NdNx: Drop the Lowest Roll from the result. The x needs to be lowercase.\n"
                                  "- NdNX: Drop the Highest Roll from the result. The X needs to be uppercase.\n"
                                  "- NdNk: Keep only the Lowest Roll for the result. The k needs to be lowercase.\n"
                                  "- NdNK: Keep only the Highest Roll for the result. The K needs to be uppercase.\n"
                                  "(4d6x rolls 4 six-sided dice and removes the lowest roll from the sum.)\n\n"
                                  "- NdN +/-/* n: Adds n to/ Subtracts n from/ Multiplies n with the result.\n"
                                  "(1d12 + 2 rolls a 12-sided die once and adds 2 to the result)\n"
                                  "(5d8 * 3 rolls five 8-sided dice and multiplies the result by three)\n\n"
                                  "NdNx/X/k/K +/-/* n is supported (pick one of each).\n"
                                  "(6d4X - 5 rolls 6 4-sided dice, drops the highest result, and then subtracts 5 "
                                  "from the sum of the remaining rolls)\n"
                                  "Does NOT support any other CritDice formats.",
                      brief="Rolls dice in NdN format")
    @commands.bot_has_permissions(embed_links=True)
    async def roll(self, ctx, *, dice):
        total_rolled = 0
        full_mod = ""
        try:
            group = re.match(r'^(\d*)d(\d+)', dice, re.IGNORECASE)
            if group is None:
                raise commands.BadArgument("Could not detect NdN pattern for dice. Refer to the command help for info"
                                           "on the NdN syntax.")
            num_of_dice, type_of_dice = int(group[1]) if group[1] != '' else 1, int(group[2])
            if num_of_dice > 150:
                await ctx.send(f"Too many dice to roll. Maximum number of dice allowed is 150. "
                               f"(You wanted {num_of_dice}.)")
            _, explanation = rolldice.roll_dice(''.join(dice))
            # py-rolldice miscalculates the result when using x/X flag, so we calculate our own result
            dice_rolled = f"{num_of_dice}d{type_of_dice}"
            mode = re.search(rf'((?<={dice_rolled}).)', dice, re.IGNORECASE)
            mode = "" if mode is None or mode.group(1).lower() not in {'k', 'x'} else mode.group(1)
            explanation, *modification = explanation.replace(",", ", ").split("]", 1)
            explanation += "]"
            explanation = re.sub(r' ~~ ([0-9, ]+)', " ~~(\\1)~~", explanation).replace("]]", "]")

            if str(modification) != "['']":
                mod = str(modification).strip("[']").split(" ", 3)
                # we only care about the first modification because handling several is a headache for now
                operator, modifier, full_mod = mod[1], mod[2], mod[1] + mod[2]
            kept_dice = re.sub(r' ~~(\([0-9, ]*\))~~', "", explanation).strip('[]').split(', ')

            try:
                for i in kept_dice:
                    total_rolled += int(i)
            except ValueError:
                raise commands.BadArgument("Unsupported operation")  # user probably used NdN a/s/m n or something

            result = eval(str(total_rolled) + full_mod) if full_mod else total_rolled
            embed = nextcord.Embed(colour=self.bot.dtbot_colour, title=f"Result: __{result}__",
                                   description=f"{explanation} {full_mod}")
            embed.set_footer(text=f"Rolled {dice_rolled}{mode}{full_mod}")
            await ctx.send(embed=embed)

        except rolldice.DiceGroupException as e:
            self.bot.help_command.context = ctx
            usage = self.bot.help_command.get_command_signature(command=ctx.command)
            em = nextcord.Embed(title="Dice have to be in proper NdN format",
                                description=f"{ctx.command.description}\n\n{usage.replace('<', '[').replace('>', ']')}",
                                colour=self.bot.dtbot_colour)
            em.set_footer(text=str(e))
            await ctx.channel.send(embed=em)

    @commands.command(description="It's Russian Roulette with a 5-barrel revolver. One chamber is loaded. Good luck.",
                      brief="Play some Russian Roulette",
                      aliases=['russianroulette', 'rusroulette'])
    async def rroulette(self, ctx):
        await ctx.send(random.choices(['Alive', 'Dead'], [0.8, 0.2])[0])

    @commands.command(description="Play some French Roulette (bet optional)\n\n"
                                  "For a nicer overview of the distribution of numbers across the colours, use "
                                  "+show roulette\n\n"
                                  "Red:       1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36\n"
                                  "Black:     2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35\n"
                                  "No colour: 0\n\n"
                                  "Bet options: No Bet / Straight bet (Red 3) / Colour Bet (Red) / Even/Odd Bet (Odd)"
                                  "\n\nUsage:\n+roulette OR +roulette Red 3 OR +roulette 0 OR +roulette Odd",
                      brief="Play some Roulette")
    async def roulette(self, ctx, *bet):
        result_eo = result_c = win_type = ""
        black = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35)
        # red = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
        result_n = random.randint(0, 36)

        if result_n == 0:
            endresult = f"{result_n}"
        else:
            result_iseven = (result_n % 2) == 0
            result_eo = "Even" if result_iseven else "Odd"
            result_c = "Black" if result_n in black else "Red"
            endresult = f"{result_c} {result_n} ({result_eo})"

        if bet:
            bet_n = ''.join(x for x in bet if x.isdigit())
            bet = ' '.join(bet).lower()
            try:
                bet_n = int(bet_n)
            except ValueError:
                pass
            if result_n == bet_n:
                # no number has a variable colour, so it doesn't matter if the user mentions a colour in their bet,
                # we award them a Straight Bet with or without a colour in the bet if they guess the number
                win_type = f" Straight Bet on {roulettecolourfinder(bet_n, black)}"
            elif result_eo.lower() in bet:
                win_type = f"n {result_eo} Bet"
            elif result_c.lower() in bet:
                win_type = f" Bet on {result_c}"

            endresult = f"{endresult}\n**You win with a{win_type}!**" if win_type else f"{endresult}\n**You lost!**"
        await ctx.send(endresult)

    @commands.group(hidden=True,
                    description="")
    @commands.bot_has_permissions(embed_links=True)
    async def show(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @show.command(name="roulette",
                  description="")
    async def _roulette(self, ctx):
        embed = nextcord.Embed(colour=self.bot.dtbot_colour,
                               description="Distribution of numbers and colours on the French Roulette table:\n")
        embed.set_image(url="https://i.imgur.com/jtMZJXR.png")
        await ctx.send(embed=embed)

    @commands.command(description='Find out how shippable your ship is\nNeeds to include "and" between ship items.'
                                  '\n\nUsage:\n+ship The entire internet and pineapple on pizza',
                      brief='Ship things')
    @commands.bot_has_permissions(embed_links=True)
    async def ship(self, ctx, *ship):
        ship = ' '.join(ship)
        ship = re.split(" and ", ship, 1, flags=re.IGNORECASE)
        shipping = random.random() * 100
        emote_choice = ":broken_heart:" if shipping < 50 else ":heart:"
        embed = nextcord.Embed(colour=self.bot.dtbot_colour,
                               description=f"{ship[0]} and {ship[1]}? `{shipping:.2f}%` shippable. {emote_choice}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Rng(bot))
