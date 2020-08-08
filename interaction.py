import asyncio
import random

import discord
from discord.ext import commands

from launcher import dtbot_colour
from linklist import *


class Interaction(commands.Cog):
    """Commands which interact with others"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Call someone a bad doggo",
                      brief="Call someone a bad doggo",
                      aliases=['shame', 'baddoggo'])
    @commands.bot_has_permissions(embed_links=True)
    async def baddog(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} called themselves a bad dog. I think they "
                                              f"just misspoke. Because if they were a dog, they'd be a good one. "
                                              f"A very good one.")
        else:
            chosen = random.choice(baddog_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention}, you're being a very bad dog! {ctx.author.mention} is "
                                              f"disappointed in you!\n\n[Image Link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Go full Tsundere and call someone a BAKA",
                      brief="Call someone a BAKA")
    @commands.bot_has_permissions(embed_links=True)
    async def baka(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} called themselves a baka? You're not a baka "
                                              f"though, you're adorable.")
        else:
            chosen = random.choice(baka_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} called {user.mention} a baka. Are they a "
                                              f"Tsundere? :thinking:\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Bitch slaps someone",
                      brief="Bitch slaps someone")
    @commands.bot_has_permissions(embed_links=True)
    async def bitchslap(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} tried to give themselves a mean bitch slap. "
                                              f"All they decide to do is rub their cheeks.")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got a bitch slap."
                                              f"\n\n[Image link](https://i.imgur.com/bTGigCv.gif)")
            embed.set_image(url="https://i.imgur.com/bTGigCv.gif")
        await ctx.send(embed=embed)

    @commands.command(description="Bite someone",
                      brief="Bite someone")
    @commands.bot_has_permissions(embed_links=True)
    async def bite(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} thought about biting themselves. "
                                              f"You're not you when you're hungry, so how about a snack instead?")
        else:
            chosen = random.choice(bite_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got bitten by {ctx.author.mention}."
                                              f"\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Kiss someone the non-romantic way",
                      brief="A non-romantic kiss")
    @commands.bot_has_permissions(embed_links=True)
    async def bkiss(self, ctx, user: discord.Member):
        chosen = random.choice(bkiss_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} kissed themselves in a non-romantic way. "
                                              f"It's very important to be happy about oneself, "
                                              f"though self-love is even better!\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got kissed.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Blush\nCan be given a reason",
                      brief="Blush")
    @commands.bot_has_permissions(embed_links=True)
    async def blush(self, ctx, *reason: str):
        chosen = random.choice(blush_links)
        if reason:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} blushed because of {' '.join(reason)}! "
                                              f"How cute!\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} blushed! How cute!\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Boop em good",
                      brief="Boop someone")
    @commands.bot_has_permissions(embed_links=True)
    async def boop(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} booped themselves. But they were such a cutie "
                                              f"doing it that we can't show it here.")
        else:
            chosen = random.choice(boop_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got booped.\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Cage someone",
                      brief="Cage someone")
    @commands.bot_has_permissions(embed_links=True)
    async def cage(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"Just as {ctx.author.mention} tried to enter the cage, their friends "
                                              f"surprised them with a party. Hooray!")
        else:
            chosen = random.choice(cage_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got caged.\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Choke em good",
                      brief="Choke someone")
    @commands.bot_has_permissions(embed_links=True)
    async def choke(self, ctx, user: discord.Member):
        chosen = random.choice(choke_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} wanted to choke themselves. They stopped when they "
                                              f"remembered their favorite food.")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} was choked by {ctx.author.mention}."
                                              f"\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Confess your feelings to someone",
                      brief="Confess your feelings to someone")
    @commands.bot_has_permissions(embed_links=True)
    async def confess(self, ctx, crush: discord.Member):
        if crush.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{crush.mention} confessed their love for themselves! "
                                              f"Aww, what a great example of self-love.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=dtbot_colour,
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
    async def cry(self, ctx, *reason: str):
        chosen = random.choice(cry_links)
        if reason:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} is crying because of {' '.join(reason)}. "
                                              f"Someone, comfort them. <:kannahug:461996510637326386>"
                                              f"\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} is crying. Someone, comfort them. "
                                              f"<:kannahug:461996510637326386>\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Cuddle someone",
                      brief="Cuddle someone")
    @commands.bot_has_permissions(embed_links=True)
    async def cuddle(self, ctx, user: discord.Member):
        chosen = random.choice(cuddle_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} cuddled themselves! They seem so happy about being here."
                                              f"\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got cuddled.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Dance with someone. Mention multiple users for a big dance party",
                      brief="Dance with someone")
    @commands.bot_has_permissions(embed_links=True)
    async def dance(self, ctx, *target: str):
        chosen = random.choice(dance_links)

        def alonedance(ctx):
            return discord.Embed(colour=dtbot_colour,
                                 description=f"{ctx.author.mention} started dancing by themselves! Everyone, come and "
                                             f"join them! DANCE PARTY!\n\n[Image link]({chosen})")

        if target:
            if ctx.message.mentions:
                if ctx.message.mentions[0].id == ctx.author.id:
                    embed = alonedance(ctx)
                else:
                    all_mentions = ""
                    i = 0
                    for _ in ctx.message.mentions:
                        all_mentions += f"{ctx.message.mentions[i].mention}, "
                        i = i + 1
                    embed = discord.Embed(colour=dtbot_colour,
                                          description=f"{ctx.author.mention} started dancing with "
                                                      f"{all_mentions.rstrip(', ')}.\n\n[Image link]({chosen})")
            else:
                description = f"{ctx.author.mention} started dancing with {' '.join(target)}.\n\n[Image link]({chosen})"
                embed = discord.Embed(colour=dtbot_colour,
                                      description=description.replace('with with', 'with'))
        else:
            embed = alonedance(ctx)
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Glomp someone",
                      brief="Glomp someone")
    @commands.bot_has_permissions(embed_links=True)
    async def glomp(self, ctx, user: discord.Member):
        chosen = random.choice(glomp_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} glomped themselves! Someone is very happy to see "
                                              f"themselves!\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got a glomp from {ctx.author.mention}."
                                              f"\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Hold someone's hand",
                      brief="Hold someone's hand",
                      aliases=['handhold', 'holdhand'])
    async def handholding(self, ctx, user: discord.Member):
        chosen = random.choice(handholding_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} tried to hold their own hand. Aww. Come here, I'll hold "
                                              f"it for you.\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} is holding {user.mention}'s hand! How lewd!"
                                              f"\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Hide yourself",
                      brief="Hide yourself")
    @commands.bot_has_permissions(embed_links=True)
    async def hide(self, ctx, *reason: str):
        chosen = random.choice(hide_links)
        if reason:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} is hiding from {' '.join(reason)}."
                                              f"\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} is hiding. Are they embarrassed?"
                                              f"\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="High five someone",
                      brief="High five someone")
    @commands.bot_has_permissions(embed_links=True)
    async def highfive(self, ctx, user: discord.Member):
        chosen = random.choice(highfive_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} gave themselves a high five! You go! Gotta "
                                              f"congratulate yourself when others don't.\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got a high five from {ctx.author.mention}."
                                              f"\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Hug someone",
                      brief="Hug someone")
    @commands.bot_has_permissions(embed_links=True)
    async def hug(self, ctx, user: discord.Member):
        chosen = random.choice(hug_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} hugged themselves! Hooray for self-appreciation!"
                                              f"\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got hugged.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="KICK THEIR ASS\n\n(This is NOT a moderation command to kick a user from a server.)",
                      brief="Kick someone")
    @commands.bot_has_permissions(embed_links=True)
    async def kick(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} aimed to kick themselves. As they noticed, it's "
                                              f"quite hard to actually do. So they didn't and went to watch their "
                                              f"favorite show.")
        else:
            chosen = random.choice(kick_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got kicked.\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="What do you think it does",
                      brief="It's in the name")
    @commands.bot_has_permissions(embed_links=True)
    async def kill(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} tried to kill themselves. Luckily, they changed "
                                              f"their mind and went to get food instead.")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got killed.")
        await ctx.send(embed=embed)

    @commands.command(description="Kiss someone",
                      brief="Kiss someone")
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx, user: discord.Member):
        chosen = random.choice(kiss_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} gave themselves a kiss! Self-love is very important "
                                              f"after all.\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got kissed.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="For something LEWD",
                      brief="LEWD")
    @commands.bot_has_permissions(embed_links=True)
    async def lewd(self, ctx, user: discord.Member = None):
        chosen = random.choice(lewd_links)
        if user:
            if user.id == ctx.author.id:
                embed = discord.Embed(colour=dtbot_colour,
                                      description=f"Calling yourself out for being lewd, **{user.mention}**? "
                                                  f"How self-aware you are. And yes. Why you gotta be so lewd?"
                                                  f"\n\n[Image link]({chosen})")
            else:
                embed = discord.Embed(colour=dtbot_colour,
                                      description=f"Why you gotta be so lewd, **{user.mention}**?"
                                                  f"\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"Why you gotta be so lewd?\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Lick someone",
                      brief="Lick someone")
    @commands.bot_has_permissions(embed_links=True)
    async def lick(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} licked themselves. Maybe they are secretly a "
                                              f"cat and value personal hygiene?")
        else:
            chosen = random.choice(lick_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} licked {user.mention}.\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Notice someone",
                      brief="Notice someone")
    @commands.bot_has_permissions(embed_links=True)
    async def notice(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} noticed themselves. Yes, you are here, and yes, "
                                              f"it's good you are.")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got noticed by {ctx.author.mention}.")
        await ctx.send(embed=embed)

    @commands.command(description="Give someone a head pat",
                      brief="Pat someone")
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx, user: discord.Member):
        chosen = random.choice(pat_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} patted themselves. They deserve all the pats!"
                                              f"\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got a pat.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Pat them on the back",
                      brief="Pat someone on the back",
                      aliases=["backpat"])
    async def patback(self, ctx, user: discord.Member):
        chosen = random.choice(patback_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} patted themselves on the back. Their flexibility is "
                                              f"highly impressive and they deserve a pat on the back already for "
                                              f"being this flexible.\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got a pat on the back.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Pinch someone's cheeks",
                      brief="Pinch someone's cheeks")
    @commands.bot_has_permissions(embed_links=True)
    async def pinch(self, ctx, user: discord.Member):
        chosen = random.choice(pinch_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} pinched their own cheeks. Maybe they wanted to check "
                                              f"if they were dreaming or not?\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got their cheeks pinched.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Poke someone",
                      brief="Poke someone")
    @commands.bot_has_permissions(embed_links=True)
    async def poke(self, ctx, user: discord.Member):
        chosen = random.choice(poke_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} poked themselves. It wasn't hard at all, just a soft "
                                              f"boop. And they deserve a boop.\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got poked.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Pout\nCan be given a reason",
                      brief="Pout")
    @commands.bot_has_permissions(embed_links=True)
    async def pout(self, ctx, *reason: str):
        chosen = random.choice(pout_links)
        if reason:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} pouted! They said it's because of "
                                              f"{' '.join(reason)}.\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} pouted! Ask them why.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Someone gonna get punched",
                      brief="Punch someone")
    @commands.bot_has_permissions(embed_links=True)
    async def punch(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} wanted to punch themselves. But they only "
                                              f"lightly rubbed their belly.")
        else:
            chosen = random.choice(punch_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got punched.\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Salute someone\nCan be given a reason",
                      brief="Salute someone")
    @commands.bot_has_permissions(embed_links=True)
    async def salute(self, ctx, *reason: str):
        chosen = random.choice(salute_links)
        if reason:
            if ctx.author in ctx.message.mentions:
                embed = discord.Embed(colour=dtbot_colour,
                                      description=f"{ctx.author.mention} saluted themselves. They must be really "
                                                  f"proud of what they did. And I am proud of them too.")
            else:
                embed = discord.Embed(colour=dtbot_colour,
                                      description=f"{ctx.author.mention} saluted {' '.join(reason)}.")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} salutes."
                                              f"\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Slap 'em hard",
                      brief="Slap someone")
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} tried to slap themselves. 'Twas but a gentle "
                                              f"caressing.")
        else:
            chosen = random.choice(slap_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got slapped.\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Be the smuggest of them all",
                      brief="Be smug")
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx):
        chosen = random.choice(smug_links)
        embed = discord.Embed(colour=dtbot_colour,
                              description=f"{ctx.author.mention} is being smug.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Stab someone",
                      brief="Stab someone")
    @commands.bot_has_permissions(embed_links=True)
    async def stab(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} tried to stab themselves. Fortunately, their "
                                              f"aim was off.")
        else:
            chosen = random.choice(stab_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got stabbed by {ctx.author.mention}."
                                              f"\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Tickle someone",
                      brief="Tickle someone")
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx, user: discord.Member):
        chosen = random.choice(tickle_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} tickled themselves. They must be really ticklish if "
                                              f"they can do that!\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{user.mention} got tickled.\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Wave at someone",
                      brief="Wave at someone")
    @commands.bot_has_permissions(embed_links=True)
    async def wave(self, ctx, user: discord.Member):
        chosen = random.choice(wave_links)
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} waved at themselves. They seem incredibly happy "
                                              f"and energetic today. How cute!\n\n[Image link]({chosen})")
        else:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} waved at {user.mention}."
                                              f"\n\n[Image link]({chosen})")
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)

    @commands.command(description="Whip someone (rather kinky)",
                      brief="Whip someone")
    @commands.bot_has_permissions(embed_links=True)
    async def whip(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"{ctx.author.mention} wants to whip themselves. They must be really "
                                              f"kinky.")
        else:
            chosen = random.choice(whip_links)
            embed = discord.Embed(colour=dtbot_colour,
                                  description=f"Bow down, {user.mention}. Time to get whipped by {ctx.author.mention}!"
                                              f"\n\n[Image link]({chosen})")
            embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Interaction(bot))
