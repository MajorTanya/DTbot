from __future__ import annotations

import enum
import random
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from DTbot import DTbot

TCritDice = Literal["x", "X", "k", "K", ""]
TRollModTypes = Literal["+", "-", "*"]
TRollOptions = Literal["Drop lowest", "Drop highest", "Keep lowest", "Keep highest"]


class RollOptions(enum.StrEnum):
    DROP_LOWEST = "Drop lowest"
    DROP_HIGHEST = "Drop highest"
    KEEP_LOWEST = "Keep lowest"
    KEEP_HIGHEST = "Keep highest"

    @classmethod
    def from_roll_option_type(cls, typed_option: TRollOptions | None) -> RollOptions | None:
        return None if typed_option is None else RollOptions(typed_option)


option_to_critdice: dict[RollOptions | None, TCritDice] = {
    RollOptions.DROP_LOWEST: "x",
    RollOptions.DROP_HIGHEST: "X",
    RollOptions.KEEP_LOWEST: "k",
    RollOptions.KEEP_HIGHEST: "K",
    None: "",
}


class Rng(commands.Cog, name="RNG"):
    """Randomness-based commands, such as rolling dice"""

    def __init__(self, bot: DTbot):
        self.bot = bot

    @app_commands.command(name="8ball", description="Ask any questions and receive an answer from the Great Beyond")
    @app_commands.describe(_question="The question you wish to get answered")
    @app_commands.rename(_question="question")
    async def _eightball(self, interaction: discord.Interaction[DTbot], _question: str | None):
        # fmt: off
        possible_responses = [
            'Yes', 'Maybe', 'No', 'Probably', 'Nah', 'No way',
            'Nope', 'YES', 'Kind of', 'HELL NO', 'What if?',
            'It is certain.', 'Ask again later.',
            "Don't count on it", 'Without a doubt.',
            'Reply hazy, try again later',
        ]
        # fmt: on
        await interaction.response.send_message(random.choice(possible_responses))

    @app_commands.command(description="Let the bot pick one of up to 5 options for you")
    async def choose(
        self,
        interaction: discord.Interaction[DTbot],
        option1: str,
        option2: str,
        option3: str | None,
        option4: str | None,
        option5: str | None,
    ):
        choices = [choice for choice in [option1, option2, option3, option4, option5] if choice is not None]
        await interaction.response.send_message(f"I choose: __{random.choice(choices)}__")

    @app_commands.command(description="Flips a coin")
    async def coinflip(self, interaction: discord.Interaction[DTbot]):
        await interaction.response.send_message(random.choice(["Heads", "Tails"]))

    @app_commands.command(description="Roll dice")
    @app_commands.describe(num_of_dice="The number of dice to roll")
    @app_commands.describe(dice_sides="How many sides the die should have (enter 20 to roll a d20, etc.)")
    @app_commands.describe(options="Drop lowest roll / Drop highest / Keep lowest / Keep highest")
    @app_commands.describe(
        mod_type="What kind of modifier (+, -, *) to apply to the dice rolls (must specify `modifier` as well)",
    )
    @app_commands.describe(
        modifier="The modifier to add/subtract/multipy with the result (must specify `mod_type` as well)",
    )
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def roll(
        self,
        interaction: discord.Interaction[DTbot],
        num_of_dice: app_commands.Range[int, 1, 150],
        dice_sides: app_commands.Range[int, 1],
        options: TRollOptions | None,
        mod_type: TRollModTypes | None,
        modifier: int | None,
    ):
        if mod_type is not None and modifier is None:
            return await interaction.response.send_message(
                "When selecting a modifier type, please also provide the value for said modifier.",
                ephemeral=True,
            )
        elif mod_type is None and modifier is not None:
            return await interaction.response.send_message(
                "When entering a modifier, please also provide the modifier type.",
                ephemeral=True,
            )
        await interaction.response.defer()
        selected_mod_type = mod_type if mod_type is not None else ""
        modifier_value = modifier if modifier is not None else ""
        option = RollOptions.from_roll_option_type(options)

        dice = f"{num_of_dice}d{dice_sides}{option_to_critdice[option]} {selected_mod_type}{modifier_value}".strip()

        # dice rolling & modification based on https://pypi.org/project/py-rolldice/, which was used here before
        rolls = [random.randint(1, dice_sides) for _ in range(num_of_dice)]
        rolls.sort(reverse=option in (RollOptions.DROP_HIGHEST, RollOptions.KEEP_HIGHEST))

        dropped = []
        kept = rolls

        if option in (RollOptions.DROP_LOWEST, RollOptions.DROP_HIGHEST):
            dropped = rolls[:1]
            kept = rolls[1:]
        elif option in (RollOptions.KEEP_LOWEST, RollOptions.KEEP_HIGHEST):
            dropped = rolls[1:]
            kept = rolls[:1]

        total_rolled = sum(kept)

        match selected_mod_type:
            case "+":
                result = total_rolled + modifier_value if modifier_value != "" else 0
            case "-":
                result = total_rolled - modifier_value if modifier_value != "" else 0
            case "*":
                result = total_rolled * modifier_value if modifier_value != "" else 1
            case _:
                result = total_rolled

        kept_explanation = f"{"**Kept**: " if dropped else ""}{f'{kept}'}"
        dropped_explanation = f"\n\n*Dropped*: {f'{dropped}'}" if dropped else ""

        embed = discord.Embed(
            colour=DTbot.DTBOT_COLOUR,
            title=f"Result: __{result:,}__",
            description=f"{kept_explanation} {selected_mod_type}{modifier_value}{dropped_explanation}",
        )
        embed.set_footer(text=f"Rolled {dice}")
        await interaction.followup.send(embed=embed)

    @app_commands.command(description="Find out how shippable your ship is")
    @app_commands.describe(first="The first half of your ship")
    @app_commands.describe(second="The second half of your ship")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def ship(self, interaction: discord.Interaction[DTbot], first: str, second: str):
        shipping = random.random() * 100
        emote_choice = ":broken_heart:" if shipping < 50 else ":heart:"
        embed = discord.Embed(
            colour=DTbot.DTBOT_COLOUR,
            description=f"{first} and {second}? `{shipping:.2f}%` shippable. {emote_choice}",
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: DTbot):
    await bot.add_cog(Rng(bot))
