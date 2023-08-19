import random

import discord
from discord import app_commands
from discord.ext import commands

from DTbot import DTbot
from linklist import *


class Interaction(commands.Cog):
    """Commands which interact with others"""

    def __init__(self, bot: DTbot):
        self.bot = bot

    @app_commands.command(description="Go full Tsundere and call someone a BAKA")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to call a BAKA")
    async def baka(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} called themselves a baka? You're not a baka though, you're adorable."
        other_msg = f"{interaction.user.mention} called {user.mention} a baka. Are they a Tsundere?"
        embed = make_embed(
            interaction.user.id,
            baka_links,
            target=user,
            self_tag_msg=self_msg,
            other_tag_msg=other_msg,
            img_on_self_tag=False,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Blush - Can be given a reason")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(reason="The reason you blushed")
    async def blush(self, interaction: discord.Interaction, reason: str | None):
        msg = f"{interaction.user.mention} blushed{f' because of {reason}' if reason else ''}! How cute!"
        embed = make_embed(interaction.user.id, blush_links, no_tag_msg=msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Boop em good")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user whose nose to boop")
    async def boop(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} booped themselves. But they were such a cutie doing it that we can't show it here."
        other_msg = f"{user.mention} got booped."
        embed = make_embed(
            interaction.user.id,
            boop_links,
            target=user,
            self_tag_msg=self_msg,
            other_tag_msg=other_msg,
            img_on_self_tag=False,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Cry - Can be given a reason")
    @app_commands.checks.bot_has_permissions(embed_links=True, use_external_emojis=True)
    @app_commands.describe(reason="The reason why you're crying")
    async def cry(self, interaction: discord.Interaction, reason: str | None):
        added = f" because of {reason}" if reason else ""
        msg = f"{interaction.user.mention} is crying{added}. Someone, comfort them. <:kannahug:461996510637326386>"
        embed = make_embed(interaction.user.id, cry_links, no_tag_msg=msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Cuddle someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to cuddle")
    async def cuddle(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} cuddled themselves! They seem so happy about being here."
        other_msg = f"{user.mention} got cuddled."
        embed = make_embed(
            interaction.user.id,
            cuddle_links,
            target=user,
            self_tag_msg=self_msg,
            other_tag_msg=other_msg,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Dance alone or with up to five other people.")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(
        user1="Someone to dance with",
        user2="Someone to dance with",
        user3="Someone to dance with",
        user4="Someone to dance with",
        user5="Someone to dance with",
    )
    async def dance(
        self,
        interaction: discord.Interaction,
        user1: discord.Member | None,
        user2: discord.Member | None,
        user3: discord.Member | None,
        user4: discord.Member | None,
        user5: discord.Member | None,
    ):
        # Remove None and Invoker by set difference, type ignored because set difference isn't analysed
        dancers: set[Member] = {user1, user2, user3, user4, user5}.difference({None, interaction.user})  # type: ignore
        msg = f"{interaction.user.mention} started dancing by themselves! Everyone, come and join them! DANCE PARTY!"
        if len(dancers) > 0:
            res = ", and ".join(c.mention for c in dancers)
            # "user1 and user2" with only two dancers, else "user1, user2[, ...], and userN"
            res = res.replace(", and ", " and ") if len(dancers) == 2 else res.replace(", and ", ", ", len(dancers) - 2)
            msg = f"{interaction.user.mention} started dancing with {res}!"
        embed = make_embed(interaction.user.id, dance_links, target=None, no_tag_msg=msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Hold someone's hand")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user whose hand to hold")
    async def handholding(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} tried to hold their own hand. Aww. Come here, I'll hold it for you."
        other_msg = f"{interaction.user.mention} is holding {user.mention}'s hand! How lewd!"
        embed = make_embed(
            interaction.user.id,
            handholding_links,
            target=user,
            self_tag_msg=self_msg,
            other_tag_msg=other_msg,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Hide yourself")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(reason="The reason you're hiding")
    async def hide(self, interaction: discord.Interaction, reason: str | None):
        added = ". Are they embarrassed?" if not reason else f" from {reason}."
        msg = f"{interaction.user.mention} is hiding{added}"
        embed = make_embed(interaction.user.id, hide_links, no_tag_msg=msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="High five someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to high five")
    async def highfive(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} gave themselves a high five! You go! Gotta congratulate yourself when others don't."
        other_msg = f"{user.mention} got a high five from {interaction.user.mention}."
        embed = make_embed(
            interaction.user.id,
            highfive_links,
            target=user,
            self_tag_msg=self_msg,
            other_tag_msg=other_msg,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Hug someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to hug")
    async def hug(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} hugged themselves! Hooray for self-appreciation!"
        other_msg = f"{user.mention} got hugged."
        embed = make_embed(interaction.user.id, hug_links, target=user, self_tag_msg=self_msg, other_tag_msg=other_msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Kiss someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to kiss")
    async def kiss(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} gave themselves a kiss! Self-love is very important after all."
        other_msg = f"{user.mention} got kissed."
        embed = make_embed(interaction.user.id, kiss_links, target=user, self_tag_msg=self_msg, other_tag_msg=other_msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Lick someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to lick")
    async def lick(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} licked themselves. Maybe they are secretly a cat and value personal hygiene?"
        other_msg = f"{interaction.user.mention} licked {user.mention}."
        embed = make_embed(
            interaction.user.id,
            lick_links,
            target=user,
            self_tag_msg=self_msg,
            other_tag_msg=other_msg,
            img_on_self_tag=False,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Give someone a headpat")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to headpat")
    async def pat(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} patted themselves. They deserve all the pats!"
        other_msg = f"{user.mention} got a pat."
        embed = make_embed(interaction.user.id, pat_links, target=user, self_tag_msg=self_msg, other_tag_msg=other_msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Pat them on the back")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to give a pat on the back")
    async def patback(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = (
            f"{user.mention} patted themselves on the back. Their flexibility is highly impressive and they "
            f"deserve a pat on the back already for being this flexible."
        )
        other_msg = f"{user.mention} got a pat on the back."
        embed = make_embed(
            interaction.user.id,
            patback_links,
            target=user,
            self_tag_msg=self_msg,
            other_tag_msg=other_msg,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Pinch someone's cheeks")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user whose cheeks to pinch")
    async def pinch(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} pinched their own cheeks. Maybe they wanted to check if they were dreaming or not?"
        other_msg = f"{user.mention} got their cheeks pinched."
        embed = make_embed(
            interaction.user.id,
            pinch_links,
            target=user,
            self_tag_msg=self_msg,
            other_tag_msg=other_msg,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Poke someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to poke")
    async def poke(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} poked themselves. It wasn't hard at all, just a soft boop. And they deserve a boop."
        other_msg = f"{user.mention} got poked."
        embed = make_embed(interaction.user.id, poke_links, target=user, self_tag_msg=self_msg, other_tag_msg=other_msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Pout - Can be given a reason")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(reason="The reason you're pouting")
    async def pout(self, interaction: discord.Interaction, reason: str | None):
        added = f"They said it's because of {reason}." if reason else "Ask them why."
        msg = f"{interaction.user.mention} pouted! {added}"
        embed = make_embed(interaction.user.id, pout_links, no_tag_msg=msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Salute someone - Can be given a reason")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user you're saluting")
    async def salute(self, interaction: discord.Interaction, user: discord.Member | discord.User | None):
        if user is None:
            msg = f"{interaction.user.mention} salutes."
        elif user == interaction.user:
            msg = (
                f"{interaction.user.mention} saluted themselves. They must be really proud of what they did. And "
                f"I am proud of them too."
            )
        else:
            msg = f"{interaction.user.mention} saluted {user.mention}."
        embed = make_embed(interaction.user.id, salute_links, no_tag_msg=msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Slap 'em hard")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to slap")
    async def slap(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} tried to slap themselves. 'Twas but a gentle caressing."
        other_msg = f"{user.mention} got slapped."
        embed = make_embed(
            interaction.user.id,
            slap_links,
            target=user,
            self_tag_msg=self_msg,
            other_tag_msg=other_msg,
            img_on_self_tag=False,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Be the smuggest of them all")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(reason="The reason why you're being smug")
    async def smug(self, interaction: discord.Interaction, reason: str | None):
        msg = f"{interaction.user.mention} is being smug{f' because of {reason}' if reason else ''}."
        embed = make_embed(interaction.user.id, smug_links, no_tag_msg=msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Tickle someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to tickle")
    async def tickle(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} tickled themselves. They must be really ticklish if they can do that!"
        other_msg = f"{user.mention} got tickled."
        embed = make_embed(
            interaction.user.id,
            tickle_links,
            target=user,
            self_tag_msg=self_msg,
            other_tag_msg=other_msg,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Wave at someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to wave at")
    async def wave(self, interaction: discord.Interaction, user: discord.Member):
        self_msg = f"{user.mention} waved at themselves. They seem incredibly happy and energetic today. How cute!"
        other_msg = f"{interaction.user.mention} waved at {user.mention}."
        embed = make_embed(interaction.user.id, wave_links, target=user, self_tag_msg=self_msg, other_tag_msg=other_msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Woop woop!")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def woop(self, interaction: discord.Interaction):
        embed = make_embed(interaction.user.id, woop_links)
        await interaction.response.send_message(embed=embed)


def make_embed(
    invoker_id: int,
    links: list[str] | None = None,
    /,
    target: discord.User | discord.Member | None = None,
    self_tag_msg: str = "",
    other_tag_msg: str = "",
    no_tag_msg: str = "",
    img_on_self_tag: bool = True,
) -> discord.Embed:
    is_self_tag = target is not None and (target.id == invoker_id)
    description = self_tag_msg if is_self_tag else other_tag_msg if target else no_tag_msg

    embed = discord.Embed(colour=DTbot.DTBOT_COLOUR, description=description)
    if (is_self_tag and not img_on_self_tag) or links is None:
        return embed

    chosen = random.choice(links)
    embed.description = f"{embed.description}" + (f"\n\n" if description else "") + f"[Image link]({chosen})"
    embed.set_image(url=f"{chosen}")
    return embed


async def setup(bot: DTbot):
    await bot.add_cog(Interaction(bot))
