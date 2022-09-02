from __future__ import annotations

import asyncio
import random

import discord
from discord.ext import commands

from DTbot import DTbot
from linklist import *


class Interaction(commands.Cog):
    """Commands which interact with others"""

    def __init__(self, bot: DTbot):
        self.bot = bot

    def make_embed(self, invoker_id: int, user: discord.Member | None, links: list[str] = None, self_tag_msg="",
                   other_tag_msg: str = "", no_tag_msg: str = "", self_tag_img: bool = True):
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

    @commands.command(description="Call someone a bad doggo",
                      brief="Call someone a bad doggo",
                      aliases=['shame', 'baddoggo'])
    @commands.bot_has_permissions(embed_links=True)
    async def baddog(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=baddog_links,
                                self_tag_msg=f"{user.mention} called themselves a bad dog. I think they just misspoke. "
                                             f"Because if they were a dog, they'd be a good one. A very good one.",
                                other_tag_msg=f"{user.mention}, you're being a very bad dog! {ctx.author.mention} is "
                                              f"disappointed in you!", self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Go full Tsundere and call someone a BAKA",
                      brief="Call someone a BAKA")
    @commands.bot_has_permissions(embed_links=True)
    async def baka(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=baka_links,
                                self_tag_msg=f"{user.mention} called themselves a baka? You're not a baka though, you're "
                                             f"adorable.",
                                other_tag_msg=f"{ctx.author.mention} called {user.mention} a baka. Are they a Tsundere?",
                                self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Bitch slaps someone",
                      brief="Bitch slaps someone")
    @commands.bot_has_permissions(embed_links=True)
    async def bitchslap(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=['https://i.imgur.com/bTGigCv.gif'],
                                self_tag_msg=f"{user.mention} tried to give themselves a mean bitch slap. All they "
                                             f"decide to do is rub their cheeks.",
                                other_tag_msg=f"{user.mention} got a bitch slap.", self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Bite someone",
                      brief="Bite someone")
    @commands.bot_has_permissions(embed_links=True)
    async def bite(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=bite_links,
                                self_tag_msg=f"{user.mention} thought about biting themselves. You're not you when "
                                             f"you're hungry, so how about a snack instead?",
                                other_tag_msg=f"{user.mention} got bitten by {ctx.author.mention}.", self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Kiss someone the non-romantic way",
                      brief="A non-romantic kiss")
    @commands.bot_has_permissions(embed_links=True)
    async def bkiss(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=bkiss_links,
                                self_tag_msg=f"{user.mention} kissed themselves in a non-romantic way. It's very "
                                             f"important to be happy about oneself, though self-love is even better!",
                                other_tag_msg=f"{user.mention} got kissed.")
        await ctx.send(embed=embed)

    @commands.command(description="Blush\nCan be given a reason",
                      brief="Blush")
    @commands.bot_has_permissions(embed_links=True)
    async def blush(self, ctx: commands.Context, *reason: str):
        message = f"{ctx.author.mention} blushed! How cute!"
        if reason:
            message = f"{ctx.author.mention} blushed because of {' '.join(reason)}! How cute!"
        embed = self.make_embed(ctx.author.id, ctx.author, links=blush_links, self_tag_msg=message)
        await ctx.send(embed=embed)

    @commands.command(description="Boop em good",
                      brief="Boop someone")
    @commands.bot_has_permissions(embed_links=True)
    async def boop(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=boop_links,
                                self_tag_msg=f"{user.mention} booped themselves. But they were such a cutie doing it "
                                             f"that we can't show it here.",
                                other_tag_msg=f"{user.mention} got booped.", self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Cage someone",
                      brief="Cage someone")
    @commands.bot_has_permissions(embed_links=True)
    async def cage(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=cage_links,
                                self_tag_msg=f"Just as {user.mention} tried to enter the cage, their friends surprised "
                                             f"them with a party. Hooray!", other_tag_msg=f"{user.mention} got caged.",
                                self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Choke em good",
                      brief="Choke someone")
    @commands.bot_has_permissions(embed_links=True)
    async def choke(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=choke_links,
                                self_tag_msg=f"{user.mention} wanted to choke themselves. They stopped when they "
                                             f"remembered their favorite food.",
                                other_tag_msg=f"{user.mention} was choked by {ctx.author.mention}.", self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Confess your feelings to someone",
                      brief="Confess your feelings to someone")
    @commands.bot_has_permissions(embed_links=True)
    async def confess(self, ctx: commands.Context, crush: discord.Member):
        if crush.id == ctx.author.id:
            embed = discord.Embed(colour=self.bot.dtbot_colour,
                                  description=f"{crush.mention} confessed their love for themselves! "
                                              f"Aww, what a great example of self-love.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=self.bot.dtbot_colour,
                                  description=f"{crush.mention}, you've been confessed to by {ctx.author.mention}! "
                                              f"\nWill you let the ship set sail or will you sink it before its "
                                              f"journey starts?" + u"\u26F5")
            message = await ctx.send(embed=embed)
            await message.add_reaction(u"\u2764")
            await message.add_reaction(u"\U0001F494")
            await asyncio.sleep(1)

            def check(reaction: discord.Reaction, user: discord.User):
                if user == crush and reaction.emoji == u"\u2764":
                    return True
                elif user == crush and reaction.emoji == u"\U0001F494":
                    return True
                else:
                    return False

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
                if check(reaction, user):
                    if reaction.emoji == u"\u2764":
                        await ctx.send(f"**{crush.display_name}** accepted **{ctx.author.display_name}'s** feelings! "
                                       f"The ship has set sail! Congratulations! :heart: :sailboat:")
                    if reaction.emoji == u"\U0001F494":
                        await ctx.send(f"**{crush.display_name}** rejected **{ctx.author.display_name}**! Don't worry, "
                                       f"I have ice cream buckets for you. :ice_cream: <:kannahug:461996510637326386>")

            except asyncio.TimeoutError:
                await ctx.channel.send(f"Looks like {crush.display_name} didn't respond to {ctx.author.display_name}'s "
                                       f"feelings. <:kannahug:461996510637326386>")

    @commands.command(description="Cry\nCan be given a reason",
                      brief="Cry")
    @commands.bot_has_permissions(embed_links=True)
    async def cry(self, ctx: commands.Context, *reason: str):
        message = f"{ctx.author.mention} is crying. Someone, comfort them. <:kannahug:461996510637326386>"
        if reason:
            message = f"{ctx.author.mention} is crying because of {' '.join(reason)}. Someone, comfort them. " \
                      f"<:kannahug:461996510637326386>"
        embed = self.make_embed(ctx.author.id, user=None, links=cry_links, no_tag_msg=message)
        await ctx.send(embed=embed)

    @commands.command(description="Cuddle someone",
                      brief="Cuddle someone")
    @commands.bot_has_permissions(embed_links=True)
    async def cuddle(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=cuddle_links,
                                self_tag_msg=f"{user.mention} cuddled themselves! They seem so happy about being here.",
                                other_tag_msg=f"{user.mention} got cuddled.")
        await ctx.send(embed=embed)

    @commands.command(description="Dance with someone. Mention multiple users for a big dance party",
                      brief="Dance with someone")
    @commands.bot_has_permissions(embed_links=True)
    async def dance(self, ctx: commands.Context, *target: str):
        if target:
            if ctx.message.mentions:
                if ctx.message.mentions[0].id == ctx.author.id and len(ctx.message.mentions) == 1:
                    message = f"{ctx.author.mention} started dancing by themselves! Everyone, come and join them! " \
                              f"DANCE PARTY!"
                else:
                    all_mentions = ""
                    for mentioned in ctx.message.mentions:
                        all_mentions += f"{mentioned.mention}, " if mentioned != ctx.author else ""
                    message = f"{ctx.author.mention} started dancing with {all_mentions.rstrip(', ')}."
            else:
                message = f"{ctx.author.mention} started dancing with {' '.join(target)}.".replace('with with', 'with')
        else:
            message = f"{ctx.author.mention} started dancing by themselves! Everyone, come and join them! DANCE PARTY!"
        embed = self.make_embed(ctx.author.id, user=None, links=dance_links, no_tag_msg=message)
        await ctx.send(embed=embed)

    @commands.command(description="Glomp someone",
                      brief="Glomp someone")
    @commands.bot_has_permissions(embed_links=True)
    async def glomp(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=glomp_links,
                                self_tag_msg=f"{user.mention} glomped themselves! Someone is very happy to see "
                                             f"themselves!",
                                other_tag_msg=f"{user.mention} got a glomp from {ctx.author.mention}.")
        await ctx.send(embed=embed)

    @commands.command(description="Hold someone's hand",
                      brief="Hold someone's hand",
                      aliases=['handhold', 'holdhand'])
    async def handholding(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=handholding_links,
                                self_tag_msg=f"{user.mention} tried to hold their own hand. Aww. Come here, I'll hold it "
                                             f"for you.",
                                other_tag_msg=f"{ctx.author.mention} is holding {user.mention}'s hand! How lewd!")
        await ctx.send(embed=embed)

    @commands.command(description="Hide yourself",
                      brief="Hide yourself")
    @commands.bot_has_permissions(embed_links=True)
    async def hide(self, ctx: commands.Context, *reason: str):
        message = f"{ctx.author.mention} is hiding. Are they embarrassed?"
        if reason:
            message = f"{ctx.author.mention} is hiding from {' '.join(reason)}."
        embed = self.make_embed(ctx.author.id, ctx.author, links=hide_links, self_tag_msg=message)
        await ctx.send(embed=embed)

    @commands.command(description="High five someone",
                      brief="High five someone")
    @commands.bot_has_permissions(embed_links=True)
    async def highfive(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=highfive_links,
                                self_tag_msg=f"{user.mention} gave themselves a high five! You go! Gotta congratulate "
                                             f"yourself when others don't.",
                                other_tag_msg=f"{user.mention} got a high five from {ctx.author.mention}.")
        await ctx.send(embed=embed)

    @commands.command(description="Hug someone",
                      brief="Hug someone")
    @commands.bot_has_permissions(embed_links=True)
    async def hug(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=hug_links,
                                self_tag_msg=f"{user.mention} hugged themselves! Hooray for self-appreciation!",
                                other_tag_msg=f"{user.mention} got hugged.")
        await ctx.send(embed=embed)

    @commands.command(description="KICK THEIR ASS\n\n(This is NOT a moderation command to kick a user from a server.)",
                      brief="Kick someone")
    @commands.bot_has_permissions(embed_links=True)
    async def kick(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=kick_links,
                                self_tag_msg=f"{user.mention} aimed to kick themselves. As they noticed, it's quite hard "
                                             f"to actually do. So they didn't and went to watch their favorite show.",
                                other_tag_msg=f"{user.mention} got kicked.", self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="What do you think it does",
                      brief="It's in the name")
    @commands.bot_has_permissions(embed_links=True)
    async def kill(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=None,
                                self_tag_msg=f"{user.mention} tried to kill themselves. Luckily, they changed their mind "
                                             f"and went to get food instead.",
                                other_tag_msg=f"{user.mention} got killed.")
        await ctx.send(embed=embed)

    @commands.command(description="Kiss someone",
                      brief="Kiss someone")
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=kiss_links,
                                self_tag_msg=f"{user.mention} gave themselves a kiss! Self-love is very important "
                                             f"after all.", other_tag_msg=f"{user.mention} got kissed.")
        await ctx.send(embed=embed)

    @commands.command(description="For something LEWD",
                      brief="LEWD")
    @commands.bot_has_permissions(embed_links=True)
    async def lewd(self, ctx: commands.Context, user: discord.Member = None):
        mention = "" if user is None else user.mention
        embed = self.make_embed(ctx.author.id, user=user, links=lewd_links,
                                self_tag_msg=f"Calling yourself out for being lewd, {mention}? How self-aware you "
                                             f"are. And yes. Why you gotta be so lewd?",
                                other_tag_msg=f"Why you gotta be so lewd, {mention}?",
                                no_tag_msg="Why you gotta be so lewd?")
        await ctx.send(embed=embed)

    @commands.command(description="Lick someone",
                      brief="Lick someone")
    @commands.bot_has_permissions(embed_links=True)
    async def lick(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=lick_links,
                                self_tag_msg=f"{user.mention} licked themselves. Maybe they are secretly a cat and value "
                                             f"personal hygiene?",
                                other_tag_msg=f"{ctx.author.mention} licked {user.mention}.", self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Notice someone",
                      brief="Notice someone")
    @commands.bot_has_permissions(embed_links=True)
    async def notice(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=None,
                                self_tag_msg=f"{user.mention} noticed themselves. Yes, you are here, and yes, it's "
                                             f"good you are.",
                                other_tag_msg=f"{user.mention} got noticed by {ctx.author.mention}.")
        await ctx.send(embed=embed)

    @commands.command(description="Give someone a head pat",
                      brief="Pat someone",
                      aliases=["headpat"])
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=pat_links,
                                self_tag_msg=f"{user.mention} patted themselves. They deserve all the pats!",
                                other_tag_msg=f"{user.mention} got a pat.")
        await ctx.send(embed=embed)

    @commands.command(description="Pat them on the back",
                      brief="Pat someone on the back",
                      aliases=["backpat"])
    async def patback(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=patback_links,
                                self_tag_msg=f"{user.mention} patted themselves on the back. Their flexibility is highly "
                                             f"impressive and they deserve a pat on the back already for being this "
                                             f"flexible.", other_tag_msg=f"{user.mention} got a pat on the back.")
        await ctx.send(embed=embed)

    @commands.command(description="Pinch someone's cheeks",
                      brief="Pinch someone's cheeks")
    @commands.bot_has_permissions(embed_links=True)
    async def pinch(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=pinch_links,
                                self_tag_msg=f"{user.mention} pinched their own cheeks. Maybe they wanted to check if "
                                             f"they were dreaming or not?",
                                other_tag_msg=f"{user.mention} got their cheeks pinched.")
        await ctx.send(embed=embed)

    @commands.command(description="Poke someone",
                      brief="Poke someone")
    @commands.bot_has_permissions(embed_links=True)
    async def poke(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=poke_links,
                                self_tag_msg=f"{user.mention} poked themselves. It wasn't hard at all, just a soft boop. "
                                             f"And they deserve a boop.", other_tag_msg=f"{user.mention} got poked.")
        await ctx.send(embed=embed)

    @commands.command(description="Pout\nCan be given a reason",
                      brief="Pout")
    @commands.bot_has_permissions(embed_links=True)
    async def pout(self, ctx: commands.Context, *reason: str):
        message = f"{ctx.author.mention} pouted! Ask them why."
        if reason:
            message = f"{ctx.author.mention} pouted! They said it's because of {' '.join(reason)}."
        embed = self.make_embed(ctx.author.id, ctx.author, links=pout_links, self_tag_msg=message)
        await ctx.send(embed=embed)

    @commands.command(description="Someone gonna get punched",
                      brief="Punch someone")
    @commands.bot_has_permissions(embed_links=True)
    async def punch(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=punch_links,
                                self_tag_msg=f"{user.mention} wanted to punch themselves. But they only lightly rubbed "
                                             f"their belly.", other_tag_msg=f"{user.mention} got punched.",
                                self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Salute someone\nCan be given a reason",
                      brief="Salute someone")
    @commands.bot_has_permissions(embed_links=True)
    async def salute(self, ctx: commands.Context, *reason: str):
        message = f"{ctx.author.mention} salutes."
        if reason:
            if ctx.author in ctx.message.mentions:
                message = f"{ctx.author.mention} saluted themselves. They must be really proud of what they did. And " \
                          f"I am proud of them too."
            else:
                message = f"{ctx.author.mention} saluted {' '.join(reason)}."
        embed = self.make_embed(ctx.author.id, ctx.author, links=salute_links, self_tag_msg=message)
        await ctx.send(embed=embed)

    @commands.command(description="Slap 'em hard",
                      brief="Slap someone")
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=slap_links,
                                self_tag_msg=f"{user.mention} tried to slap themselves. 'Twas but a gentle caressing.",
                                other_tag_msg=f"{user.mention} got slapped.", self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Be the smuggest of them all",
                      brief="Be smug")
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx: commands.Context):
        embed = self.make_embed(ctx.author.id, ctx.author, links=smug_links,
                                self_tag_msg=f"{ctx.author.mention} is being smug.")
        await ctx.send(embed=embed)

    @commands.command(description="Stab someone",
                      brief="Stab someone")
    @commands.bot_has_permissions(embed_links=True)
    async def stab(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=stab_links,
                                self_tag_msg=f"{user.mention} tried to stab themselves. Fortunately, their aim was off.",
                                other_tag_msg=f"{user.mention} got stabbed by {ctx.author.mention}.",
                                self_tag_img=False)
        await ctx.send(embed=embed)

    @commands.command(description="Tickle someone",
                      brief="Tickle someone")
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=tickle_links,
                                self_tag_msg=f"{user.mention} tickled themselves. They must be really ticklish if they "
                                             f"can do that!", other_tag_msg=f"{user.mention} got tickled.")
        await ctx.send(embed=embed)

    @commands.command(description="Wave at someone",
                      brief="Wave at someone")
    @commands.bot_has_permissions(embed_links=True)
    async def wave(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=wave_links,
                                self_tag_msg=f"{user.mention} waved at themselves. They seem incredibly happy and "
                                             f"energetic today. How cute!",
                                other_tag_msg=f"{ctx.author.mention} waved at {user.mention}.")
        await ctx.send(embed=embed)

    @commands.command(description="Whip someone (rather kinky)",
                      brief="Whip someone")
    @commands.bot_has_permissions(embed_links=True)
    async def whip(self, ctx: commands.Context, user: discord.Member):
        embed = self.make_embed(ctx.author.id, user=user, links=whip_links,
                                self_tag_msg=f"{user.mention} wants to whip themselves. They must be really kinky.",
                                other_tag_msg=f"Bow down, {user.mention}. Time to get whipped by {ctx.author.mention}!",
                                self_tag_img=False)
        await ctx.send(embed=embed)


async def setup(bot: DTbot):
    await bot.add_cog(Interaction(bot))
