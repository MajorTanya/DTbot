import random
import re
import typing

import discord
import rolldice
from discord import app_commands
from discord.ext import commands

from DTbot import DTbot

TRouletteBets = typing.Literal['Straight (e.g. Red 3)', 'Colour (Red/Black)', 'Even/Odd', 'High (19-36)/Low (1-18)']
TRollModTypes = typing.Literal['+', '-', '*']
TRollOptions = typing.Literal['Drop lowest', 'Drop highest', 'Keep lowest', 'Keep highest']

roulette_bet_types = {'Straight (e.g. Red 3)': 'straight', 'Colour (Red/Black)': 'colour', 'Even/Odd': 'parity',
                      'High (19-36)/Low (1-18)': 'hilo'}
black = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35)
red = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
black_choices = [app_commands.Choice(name=f'Black {num}', value=f'Black {num}') for num in black]
red_choices = [app_commands.Choice(name=f'Red {num}', value=f'Red {num}') for num in red]
colour_choices = [app_commands.Choice(name='Red', value='Red'), app_commands.Choice(name='Black', value='Black')]
parity_choices = [app_commands.Choice(name='Even', value='Even'), app_commands.Choice(name='Odd', value='Odd')]
hilo_choices = [app_commands.Choice(name='High (19-36)', value='High'),
                app_commands.Choice(name='Low (1-18)', value='Low')]

roll_options = {'Drop lowest': 'x', 'Drop highest': 'X', 'Keep lowest': 'k', 'Keep highest': 'K', None: ''}


def roulettecolourfinder(n: str | int):
    try:
        n = int(n)
    except ValueError:
        return 'invalid'
    return '0' if n == 0 else f'Black {n}' if n in black else f'Red {n}' if n in red else 'invalid'


def is_valid_bet(bet_type: str, bet: str):
    digits = ''
    try:
        bet_type = roulette_bet_types[bet_type]
    except KeyError:
        return False
    match bet_type:
        case 'straight':
            if 'red' in bet.lower() or 'black' in bet.lower() or '0' == bet.lower():
                digits = bet.lower().removeprefix('red ').removeprefix('black ')
            if digits.isdigit() and roulettecolourfinder(digits) != 'invalid':
                return True
            return False
        case 'colour':
            return bet.lower() == 'black' or bet.lower() == 'red'
        case 'parity':
            return bet.lower() == 'even' or bet.lower() == 'odd'
        case 'hilo':
            return bet.lower() == 'high' or bet.lower() == 'low'
        case _:
            return False


class Rng(commands.Cog, name='RNG'):
    """Randomness-based commands, such as rolling dice"""

    def __init__(self, bot: DTbot):
        self.bot = bot

    @app_commands.command(name='8ball', description='Ask any questions and receive an answer from the Great Beyond')
    @app_commands.describe(_question='The question you wish to get answered')
    @app_commands.rename(_question='question')
    async def _eightball(self, interaction: discord.Interaction, _question: str | None):
        possible_responses = [
            'Yes', 'Maybe', 'No', 'Probably', 'Nah', 'No way',
            'Nope', 'YES', 'Kind of', 'HELL NO', 'What if?',
            'It is certain.', 'Ask again later.',
            "Don't count on it", 'Without a doubt.',
            'Reply hazy, try again later'
        ]
        await interaction.response.send_message(random.choice(possible_responses))

    @app_commands.command(description='Let the bot pick one of up to 5 options for you')
    async def choose(self, interaction: discord.Interaction, option1: str, option2: str, option3: str | None,
                     option4: str | None, option5: str | None):
        choices = [choice for choice in [option1, option2, option3, option4, option5] if choice is not None]
        await interaction.response.send_message(f'I choose: __{random.choice(choices)}__')

    @app_commands.command(description='Flips a coin')
    async def coinflip(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(['Heads', 'Tails']))

    roulette = app_commands.Group(name='roulette', description='Play at a French Roulette table')

    @roulette.command(description='Try and guess the result of a Roulette spin')
    @app_commands.describe(bet_type='The type of bet you want to make')
    @app_commands.describe(bet='The bet you want to make')
    @app_commands.rename(bet_type='type')
    async def bet(self, interaction: discord.Interaction, bet_type: TRouletteBets, bet: str):
        if not is_valid_bet(bet_type, bet):
            return await interaction.response.send_message(f'Invalid Bet for the selected bet type. Please choose a '
                                                           f'bet from the suggested options.', ephemeral=True)
        number = random.randint(0, 36)
        result = roulettecolourfinder(number)
        won = False
        try:
            match roulette_bet_types[bet_type]:
                case 'straight':
                    won = result == bet
                case 'colour':
                    won = ('Black' in result and 'black' == bet.lower()) or ('Red' in result and 'red' == bet.lower())
                case 'parity':
                    won = (number % 2 == 0 and 'even' in bet.lower()) or (number % 2 != 0 and 'odd' in bet.lower())
                case 'hilo':
                    won = (19 <= number <= 36 and 'high' in bet.lower()) or (1 <= number <= 18 and 'low' in bet.lower())
        except KeyError:
            pass
        await interaction.response.send_message(f'Roulette landed on {result}.\nYou **{"won" if won else "lost"}** '
                                                f'with your bet on {bet}.')

    @bet.autocomplete('bet')
    async def bet_autocomplete(self, interaction: discord.Interaction, current: str):
        bet_type = roulette_bet_types[interaction.namespace['type']]
        choices: list[app_commands.Choice] = []
        match bet_type:
            case 'straight':
                choices = [choice for choice in red_choices if current.lower() in choice.name.lower()]
                choices += [choice for choice in black_choices if current.lower() in choice.name.lower()]
                if '0' in current.lower():
                    choices += [app_commands.Choice(name='0', value='0')]
            case 'colour':
                choices = [choice for choice in colour_choices if current.lower() in choice.name.lower()]
            case 'parity':
                choices = [choice for choice in parity_choices if current.lower() in choice.name.lower()]
            case 'hilo':
                choices = [choice for choice in hilo_choices if current.lower() in choice.name.lower()]
        return choices[:25]

    @roulette.command(description='Spin the Roulette wheel without guessing the result')
    async def spin(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Roulette landed on {roulettecolourfinder(random.randint(0, 36))}')

    @roulette.command(description='Show the distribution of numbers of a French Roulette Table')
    async def table(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=self.bot.dtbot_colour,
                              description='Distribution of numbers and colours on the French Roulette table:\n'
                                          '0 is counted as neither Red nor Black.')
        embed.set_image(url='https://i.imgur.com/jtMZJXR.png')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description='Russian Roulette with a 5-barrel revolver. One chamber is loaded. Good luck.')
    async def russianroulette(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choices(['Alive', 'Dead'], [0.8, 0.2])[0])

    @app_commands.command(description='Roll dice')
    @app_commands.describe(num_of_dice='The number of dice to roll')
    @app_commands.describe(dice_sides='How many sides the die should have (enter 20 to roll a d20, etc.)')
    @app_commands.describe(options='Drop lowest roll / Drop highest / Keep lowest / Keep highest')
    @app_commands.describe(mod_type='What kind of modifier (+, -, *) to apply to the dice rolls (must specify '
                                    '`modifier` as well)')
    @app_commands.describe(modifier='The modifier to add/subtract/multipy with the result (must specify `mod_type` as '
                                    'well)')
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def roll(self, interaction: discord.Interaction, num_of_dice: app_commands.Range[int, 1, 150],
                   dice_sides: app_commands.Range[int, 1], options: TRollOptions | None, mod_type: TRollModTypes | None,
                   modifier: int | None):
        if mod_type is not None and modifier is None:
            return await interaction.response.send_message('When selecting a modifier type, please also provide the '
                                                           'value for said modifier.', ephemeral=True)
        elif mod_type is None and modifier is not None:
            return await interaction.response.send_message('When entering a modifier, please also provide the modifier '
                                                           'type.', ephemeral=True)
        await interaction.response.defer()
        mod_type = mod_type if mod_type is not None else ''
        modifier = modifier if modifier is not None else ''
        dice = f'{num_of_dice}d{dice_sides}{roll_options[options]} {mod_type}{modifier}'
        _, explanation = rolldice.roll_dice(''.join(dice))
        # py-rolldice miscalculates the result when using x/X flag, so we calculate our own result
        explanation, _ = explanation.replace(',', ', ').split(']', 1)
        explanation += ']'
        explanation = re.sub(r' ~~ ([\d, ]+)', ' ~~(\\1)~~', explanation).replace(']]', ']')
        kept_dice = re.sub(r' ~~(\([\d, ]*\))~~', '', explanation).strip('[]').split(', ')

        total_rolled = sum(int(die) for die in kept_dice if die.isdigit())

        match mod_type:
            case '+':
                result = total_rolled + modifier
            case '-':
                result = total_rolled - modifier
            case '*':
                result = total_rolled * modifier
            case _:
                result = total_rolled
        embed = discord.Embed(colour=self.bot.dtbot_colour, title=f'Result: __{result}__',
                              description=f'{explanation} {mod_type}{modifier if modifier is not None else ""}')
        embed.set_footer(text=f'Rolled {dice}')
        await interaction.followup.send(embed=embed)

    @app_commands.command(description='Find out how shippable your ship is')
    @app_commands.describe(first='The first half of your ship')
    @app_commands.describe(second='The second half of your ship')
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def ship(self, interaction: discord.Interaction, first: str, second: str):
        shipping = random.random() * 100
        emote_choice = ':broken_heart:' if shipping < 50 else ':heart:'
        embed = discord.Embed(colour=self.bot.dtbot_colour,
                              description=f'{first} and {second}? `{shipping:.2f}%` shippable. {emote_choice}')
        await interaction.response.send_message(embed=embed)


async def setup(bot: DTbot):
    await bot.add_cog(Rng(bot))
