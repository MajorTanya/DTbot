import random
import re
import typing

import discord
import rolldice
from discord import app_commands
from discord.ext import commands

from DTbot import DTbot

TRollModTypes = typing.Literal["+", "-", "*"]
TRollOptions = typing.Literal["Drop lowest", "Drop highest", "Keep lowest", "Keep highest"]

roll_options = {"Drop lowest": "x", "Drop highest": "X", "Keep lowest": "k", "Keep highest": "K", None: ""}


class Rng(commands.Cog, name="RNG"):
    """Randomness-based commands, such as rolling dice"""

    def __init__(self, bot: DTbot):
        self.bot = bot

    @app_commands.command(name="8ball", description="Ask any questions and receive an answer from the Great Beyond")
    @app_commands.describe(_question="The question you wish to get answered")
    @app_commands.rename(_question="question")
    async def _eightball(self, interaction: discord.Interaction, _question: str | None):
        # fmt: off
        possible_responses = [
            'Yes', 'Maybe', 'No', 'Probably', 'Nah', 'No way',
            'Nope', 'YES', 'Kind of', 'HELL NO', 'What if?',
            'It is certain.', 'Ask again later.',
            "Don't count on it", 'Without a doubt.',
            'Reply hazy, try again later'
        ]
        # fmt: on
        await interaction.response.send_message(random.choice(possible_responses))

    @app_commands.command(description="Let the bot pick one of up to 5 options for you")
    async def choose(
        self,
        interaction: discord.Interaction,
        option1: str,
        option2: str,
        option3: str | None,
        option4: str | None,
        option5: str | None,
    ):
        choices = [choice for choice in [option1, option2, option3, option4, option5] if choice is not None]
        await interaction.response.send_message(f"I choose: __{random.choice(choices)}__")

    @app_commands.command(description="Flips a coin")
    async def coinflip(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(["Heads", "Tails"]))

    @app_commands.command(description="Roll dice")
    @app_commands.describe(num_of_dice="The number of dice to roll")
    @app_commands.describe(dice_sides="How many sides the die should have (enter 20 to roll a d20, etc.)")
    @app_commands.describe(options="Drop lowest roll / Drop highest / Keep lowest / Keep highest")
    @app_commands.describe(
        mod_type="What kind of modifier (+, -, *) to apply to the dice rolls (must specify `modifier` as well)"
    )
    @app_commands.describe(
        modifier="The modifier to add/subtract/multipy with the result (must specify `mod_type` as well)"
    )
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def roll(
        self,
        interaction: discord.Interaction,
        num_of_dice: app_commands.Range[int, 1, 150],
        dice_sides: app_commands.Range[int, 1],
        options: TRollOptions | None,
        mod_type: TRollModTypes | None,
        modifier: int | None,
    ):
        if mod_type is not None and modifier is None:
            return await interaction.response.send_message(
                "When selecting a modifier type, please also provide the value for said modifier.", ephemeral=True
            )
        elif mod_type is None and modifier is not None:
            return await interaction.response.send_message(
                "When entering a modifier, please also provide the modifier type.", ephemeral=True
            )
        await interaction.response.defer()
        mod_type = mod_type if mod_type is not None else ""
        modifier = modifier if modifier is not None else ""
        dice = f"{num_of_dice}d{dice_sides}{roll_options[options]} {mod_type}{modifier}".strip()
        _, explanation = rolldice.roll_dice(dice)
        # py-rolldice miscalculates the result when using x/X flag, so we calculate our own result
        explanation, _ = explanation.replace(",", ", ").split("]", 1)
        explanation += "]"
        explanation = re.sub(r" ~~ ([\d, ]+)", " ~~(\\1)~~", explanation).replace("]]", "]")
        kept_dice = re.sub(r" ~~(\([\d, ]*\))~~", "", explanation).strip("[]").split(", ")

        total_rolled = sum(int(die) for die in kept_dice if die.isdigit())

        match mod_type:
            case "+":
                result = total_rolled + modifier
            case "-":
                result = total_rolled - modifier
            case "*":
                result = total_rolled * modifier
            case _:
                result = total_rolled
        embed = discord.Embed(
            colour=DTbot.DTBOT_COLOUR,
            title=f"Result: __{result}__",
            description=f"{explanation} {mod_type}{modifier if modifier is not None else ''}",
        )
        embed.set_footer(text=f"Rolled {dice}")
        await interaction.followup.send(embed=embed)

    @app_commands.command(description="Find out how shippable your ship is")
    @app_commands.describe(first="The first half of your ship")
    @app_commands.describe(second="The second half of your ship")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def ship(self, interaction: discord.Interaction, first: str, second: str):
        shipping = random.random() * 100
        emote_choice = ":broken_heart:" if shipping < 50 else ":heart:"
        embed = discord.Embed(
            colour=DTbot.DTBOT_COLOUR,
            description=f"{first} and {second}? `{shipping:.2f}%` shippable. {emote_choice}",
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: DTbot):
    await bot.add_cog(Rng(bot))
