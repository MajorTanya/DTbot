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

    def make_embed(self, invoker_id: int, /, user: discord.User | discord.Member | None, links: list[str] = None,
                   self_tag_msg: str = "", other_tag_msg: str = "", no_tag_msg: str = "",
                   self_tag_img: bool = True) -> discord.Embed:
        chosen = random.choice(links) if links else ""
        markdown_link = f"\n\n[Image link]({chosen})" if links else ""
        embed = discord.Embed(colour=self.bot.dtbot_colour)
        if user:
            if user.id == invoker_id:
                embed.description = self_tag_msg
                if self_tag_img:
                    embed.description = embed.description + markdown_link
                    embed.set_image(url=f"{chosen}")
            else:
                embed.description = other_tag_msg + markdown_link
                embed.set_image(url=f"{chosen}")
        else:
            embed.description = no_tag_msg + markdown_link
            embed.set_image(url=f"{chosen}")
        return embed

    @app_commands.command(description="Go full Tsundere and call someone a BAKA")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to call a BAKA")
    async def baka(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=baka_links,
                                self_tag_msg=f"{user.mention} called themselves a baka? You're not a baka though, "
                                             f"you're adorable.",
                                other_tag_msg=f"{interaction.user.mention} called {user.mention} a baka. Are they a "
                                              f"Tsundere?",
                                self_tag_img=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Bitch slaps someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to bitchslap")
    async def bitchslap(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=['https://i.imgur.com/bTGigCv.gif'],
                                self_tag_msg=f"{user.mention} tried to give themselves a mean bitch slap. All they "
                                             f"decide to do is rub their cheeks.",
                                other_tag_msg=f"{user.mention} got a bitch slap.", self_tag_img=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Bite someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to bite")
    async def bite(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=bite_links,
                                self_tag_msg=f"{user.mention} thought about biting themselves. You're not you when "
                                             f"you're hungry, so how about a snack instead?",
                                other_tag_msg=f"{user.mention} got bitten by {interaction.user.mention}.",
                                self_tag_img=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Blush - Can be given a reason")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(reason="The reason you blushed")
    async def blush(self, interaction: discord.Interaction, reason: str | None):
        message = f"{interaction.user.mention} blushed! How cute!"
        if reason:
            message = f"{interaction.user.mention} blushed because of {reason}! How cute!"
        embed = self.make_embed(interaction.user.id, user=interaction.user, links=blush_links, self_tag_msg=message)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Boop em good")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user whose nose to boop")
    async def boop(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=boop_links,
                                self_tag_msg=f"{user.mention} booped themselves. But they were such a cutie doing it "
                                             f"that we can't show it here.",
                                other_tag_msg=f"{user.mention} got booped.", self_tag_img=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Choke em good")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to choke")
    async def choke(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=choke_links,
                                self_tag_msg=f"{user.mention} wanted to choke themselves. They stopped when they "
                                             f"remembered their favorite food.",
                                other_tag_msg=f"{user.mention} was choked by {interaction.user.mention}.",
                                self_tag_img=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Cry - Can be given a reason")
    @app_commands.checks.bot_has_permissions(embed_links=True, use_external_emojis=True)
    @app_commands.describe(reason="The reason why you're crying")
    async def cry(self, interaction: discord.Interaction, reason: str | None):
        message = f"{interaction.user.mention} is crying. Someone, comfort them. <:kannahug:461996510637326386>"
        if reason:
            message = f"{interaction.user.mention} is crying because of {reason}. Someone, comfort them. " \
                      f"<:kannahug:461996510637326386>"
        embed = self.make_embed(interaction.user.id, user=None, links=cry_links, no_tag_msg=message)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Cuddle someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to cuddle")
    async def cuddle(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=cuddle_links,
                                self_tag_msg=f"{user.mention} cuddled themselves! They seem so happy about being here.",
                                other_tag_msg=f"{user.mention} got cuddled.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Dance alone or with up to five other people.")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user1="Someone to dance with", user2="Someone to dance with", user3="Someone to dance with",
                           user4="Someone to dance with", user5="Someone to dance with")
    async def dance(self, interaction: discord.Interaction, user1: discord.Member | None,
                    user2: discord.Member | None, user3: discord.Member | None,
                    user4: discord.Member | None, user5: discord.Member | None):
        dancers = {user1, user2, user3, user4, user5}.difference({None})  # Remove None entry
        if len(dancers) == 0:
            msg = f'{interaction.user.mention} started dancing by themselves! Everyone, come and join them! ' \
                  f'DANCE PARTY!'
        else:
            msg = f'{interaction.user.mention} started dancing with {(d.mention + ", " for d in dancers)}'.rstrip(', ')
        embed = self.make_embed(interaction.user.id, user=None, links=dance_links, no_tag_msg=msg)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Hold someone's hand")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user whose hand to hold")
    async def handholding(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=handholding_links,
                                self_tag_msg=f"{user.mention} tried to hold their own hand. Aww. Come here, I'll hold "
                                             f"it for you.",
                                other_tag_msg=f"{interaction.user.mention} is holding {user.mention}'s hand! How lewd!")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Hide yourself")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(reason="The reason you're hiding")
    async def hide(self, interaction: discord.Interaction, reason: str | None):
        message = f"{interaction.user.mention} is hiding. Are they embarrassed?"
        if reason:
            message = f"{interaction.user.mention} is hiding from {reason}."
        embed = self.make_embed(interaction.user.id, interaction.user, links=hide_links, self_tag_msg=message)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="High five someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to high five")
    async def highfive(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=highfive_links,
                                self_tag_msg=f"{user.mention} gave themselves a high five! You go! Gotta congratulate "
                                             f"yourself when others don't.",
                                other_tag_msg=f"{user.mention} got a high five from {interaction.user.mention}.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Hug someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to hug")
    async def hug(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=hug_links,
                                self_tag_msg=f"{user.mention} hugged themselves! Hooray for self-appreciation!",
                                other_tag_msg=f"{user.mention} got hugged.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="KICK THEIR ASS - (NOT a moderation command to kick a user from a server.)")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to kick")
    async def kick(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=kick_links,
                                self_tag_msg=f"{user.mention} aimed to kick themselves. As they noticed, it's quite "
                                             f"hard to actually do. So they didn't and went to watch their favorite "
                                             f"show.",
                                other_tag_msg=f"{user.mention} got kicked.", self_tag_img=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="What do you think it does")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to kill")
    async def kill(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=None,
                                self_tag_msg=f"{user.mention} tried to kill themselves. Luckily, they changed their "
                                             f"mind and went to get food instead.",
                                other_tag_msg=f"{user.mention} got killed.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Kiss someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to kiss")
    async def kiss(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=kiss_links,
                                self_tag_msg=f"{user.mention} gave themselves a kiss! Self-love is very important "
                                             f"after all.",
                                other_tag_msg=f"{user.mention} got kissed.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Call out someone for being lewd")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to call out for being lewd")
    async def lewd(self, interaction: discord.Interaction, user: discord.Member | None):
        mention = user.mention if user is not None else ""
        embed = self.make_embed(interaction.user.id, user=user, links=lewd_links,
                                self_tag_msg=f"Calling yourself out for being lewd, {mention}? How self-aware you "
                                             f"are. And yes. Why you gotta be so lewd?",
                                other_tag_msg=f"Why you gotta be so lewd, {mention}?",
                                no_tag_msg="Why you gotta be so lewd?")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Lick someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to lick")
    async def lick(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=lick_links,
                                self_tag_msg=f"{user.mention} licked themselves. Maybe they are secretly a cat and "
                                             f"value personal hygiene?",
                                other_tag_msg=f"{interaction.user.mention} licked {user.mention}.", self_tag_img=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Give someone a headpat")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to headpat")
    async def pat(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=pat_links,
                                self_tag_msg=f"{user.mention} patted themselves. They deserve all the pats!",
                                other_tag_msg=f"{user.mention} got a pat.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Pat them on the back")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to give a pat on the back")
    async def patback(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=patback_links,
                                self_tag_msg=f"{user.mention} patted themselves on the back. Their flexibility is "
                                             f"highly impressive and they deserve a pat on the back already for being "
                                             f"this flexible.",
                                other_tag_msg=f"{user.mention} got a pat on the back.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Pinch someone's cheeks")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user whose cheeks to pinch")
    async def pinch(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=pinch_links,
                                self_tag_msg=f"{user.mention} pinched their own cheeks. Maybe they wanted to check if "
                                             f"they were dreaming or not?",
                                other_tag_msg=f"{user.mention} got their cheeks pinched.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Poke someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to poke")
    async def poke(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=poke_links,
                                self_tag_msg=f"{user.mention} poked themselves. It wasn't hard at all, just a soft "
                                             f"boop. And they deserve a boop.",
                                other_tag_msg=f"{user.mention} got poked.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Pout - Can be given a reason")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(reason="The reason you're pouting")
    async def pout(self, interaction: discord.Interaction, reason: str | None):
        message = f"{interaction.user.mention} pouted! Ask them why."
        if reason:
            message = f"{interaction.user.mention} pouted! They said it's because of {reason}."
        embed = self.make_embed(interaction.user.id, interaction.user, links=pout_links, self_tag_msg=message)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Salute someone - Can be given a reason")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user you're saluting")
    async def salute(self, interaction: discord.Interaction, user: discord.Member | discord.User | None):
        if user is None:
            message = f"{interaction.user.mention} salutes."
        elif user == interaction.user:
            message = f"{interaction.user.mention} saluted themselves. They must be really proud of what they did. " \
                      f"And I am proud of them too."
        else:
            message = f"{interaction.user.mention} saluted {user.mention}."
        embed = self.make_embed(interaction.user.id, interaction.user, links=salute_links, self_tag_msg=message)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Slap 'em hard")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to slap")
    async def slap(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=slap_links,
                                self_tag_msg=f"{user.mention} tried to slap themselves. 'Twas but a gentle caressing.",
                                other_tag_msg=f"{user.mention} got slapped.", self_tag_img=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Be the smuggest of them all")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(reason="The reason why you're being smug")
    async def smug(self, interaction: discord.Interaction, reason: str | None):
        message = f"{interaction.user.mention} is being smug."
        if reason:
            message = f"{interaction.user.mention} is being smug because of {reason}."
        embed = self.make_embed(interaction.user.id, user=None, links=smug_links, no_tag_msg=message)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Tickle someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to tickle")
    async def tickle(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=tickle_links,
                                self_tag_msg=f"{user.mention} tickled themselves. They must be really ticklish if they "
                                             f"can do that!",
                                other_tag_msg=f"{user.mention} got tickled.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Wave at someone")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to wave at")
    async def wave(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=wave_links,
                                self_tag_msg=f"{user.mention} waved at themselves. They seem incredibly happy and "
                                             f"energetic today. How cute!",
                                other_tag_msg=f"{interaction.user.mention} waved at {user.mention}.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Whip someone (rather kinky)")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.describe(user="The user to whip")
    async def whip(self, interaction: discord.Interaction, user: discord.Member):
        embed = self.make_embed(interaction.user.id, user=user, links=whip_links,
                                self_tag_msg=f"{user.mention} wants to whip themselves. They must be really kinky.",
                                other_tag_msg=f"Bow down, {user.mention}. Time to get whipped by "
                                              f"{interaction.user.mention}!",
                                self_tag_img=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Woop woop!")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def woop(self, interaction: discord.Interaction):
        chosen = random.choice(woop_links)
        embed = discord.Embed(colour=self.bot.dtbot_colour, description=f'[Image link]({chosen})')
        embed.set_image(url=f"{chosen}")
        await interaction.response.send_message(embed=embed)


async def setup(bot: DTbot):
    await bot.add_cog(Interaction(bot))
