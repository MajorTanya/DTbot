import asyncio
import random

import discord
from discord.ext import commands

from linklist import *


class Interaction:
    """Commands which interact with others"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True,
                      description="Call someone a bad doggo",
                      brief="Call someone a bad doggo",
                      aliases=['shame', 'baddog'])
    async def baddoggo(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} called themselves a bad doggo. I think they just misspoke. Because if they were a doggo, they'd be a good one. A very good one.".format(ctx.message.author.mention))
        else:
            chosen = random.choice(baddoggo_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + ", you're being a very bad dog! {} is disappointed in you!".format(ctx.message.author.mention) + "\n\n[Image Link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Go full Tsundere and call someone a BAKA",
                      brief="Call someone a BAKA")
    async def baka(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} called themselves a baka? You're not a baka though, you're adorable.".format(ctx.message.author.mention))
        else:
            chosen = random.choice(baka_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} called {} a baka. Are they a Tsundere? :thinking:".format(ctx.message.author.mention, user.mention) + "\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Bitch slaps someone",
                      brief="Bitch slaps someone")
    async def bitchslap(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} tried to give themselves a mean bitch slap. All they decide to do is rub their cheeks.".format(ctx.message.author.mention))
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got a bitch slap.".format(user.mention) + "\n\n[Image link](https://i.imgur.com/bTGigCv.gif)")
            embed.set_image(url="https://i.imgur.com/bTGigCv.gif")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Bite someone",
                      brief="Bite someone")
    async def bite(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} thought about biting themselves. You're not you when you're hungry, so how about a snack instead?".format(ctx.message.author.mention))
        else:
            chosen = random.choice(bite_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got bitten by {}.".format(user.mention, ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Kiss someone the non-romantic way",
                      brief="A non-romantic kiss")
    async def bkiss(self, ctx, user: discord.Member):
        chosen = random.choice(bkiss_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} kissed themselves in a non-romantic way. It's very important to be happy about oneself, though self-love is even better!".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got kissed.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Blush\nCan be given a reason",
                      brief="Blush")
    async def blush(self, ctx, *reason: str):
        chosen = random.choice(blush_links)
        if reason:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} blushed because of ".format(ctx.message.author.mention) + ' '.join(reason) + "! How cute!\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} blushed! How cute!".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Boop em good",
                      brief="Boop someone")
    async def boop(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} booped themselves. But they were such a cutie doing it that we can't show it here.".format(ctx.message.author.mention))
        else:
            chosen = random.choice(boop_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got booped.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Cage someone",
                      brief="Cage someone")
    async def cage(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="Just as {} tried to enter the cage, their friends surprised them with a party. Hooray!".format(ctx.message.author.mention))
        else:
            chosen = random.choice(cage_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got caged.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Choke em good",
                      brief="Choke someone")
    async def choke(self, ctx, user: discord.Member):
        chosen = random.choice(choke_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} wanted to choke themselves. They stopped when they remembered their favorite food.".format(user.mention))
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} was choked by {}.".format(user.mention, ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Confess your feelings to someone",
                      brief="Confess your feelings to someone")
    async def confess(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} confessed their love for themselves! Aww, what a great example of self-love.".format(user.mention))
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + ", you've been confessed to by {}!".format(ctx.message.author.mention) + "\nWill you let the ship set sail or will you sink it before its journey starts? " + u"\u26F5")
            message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(message, u"\u2764")
            await self.bot.add_reaction(message, u"\U0001F494")
            await asyncio.sleep(1)

            def check(reaction):
                e = str(reaction.emoji)
                return e.startswith((u"\u2764", u"\U0001F494"))

            response = await self.bot.wait_for_reaction(message=message, check=check)

            if response.user.id == user.id:
                if response.reaction.emoji == u"\u2764":
                    await self.bot.say("**{0.user.display_name}** accepted **{1}'s** feelings! The ship has set sail! Congratulations! :heart: :sailboat:".format(response, ctx.message.author.display_name))
                elif response.reaction.emoji == u"\U0001F494":
                    await self.bot.say("**{0.user.display_name}** rejected **{1}**! Don't worry, I have ice cream buckets for you. :ice_cream: <:kannahug:461996510637326386>".format(response, ctx.message.author.display_name))
                else:
                    return
            else:
                return


    @commands.command(pass_context=True,
                      description="Cry\nCan be given a reason",
                      brief="Cry")
    async def cry(self, ctx, *reason: str):
        chosen = random.choice(cry_links)
        if reason:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(ctx.message.author.mention) + " is crying because of " + ' '.join(reason) + ". Someone, comfort them. <:kannahug:461996510637326386>\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(ctx.message.author.mention) + " is crying. Someone, comfort them. <:kannahug:461996510637326386>\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Cuddle someone",
                      brief="Cuddle someone")
    async def cuddle(self, ctx, user: discord.Member):
        chosen = random.choice(cuddle_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} cuddled themselves! They seem so happy about being here.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got cuddled.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Dance with someone",
                      brief="Dance with someone")
    async def dance(self, ctx, *target: str):
        chosen = random.choice(dance_links)
        if target:
            if ctx.message.mentions:
                if ctx.message.mentions[0].id == ctx.message.author.id:
                    embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} started dancing by themselves! Everyone, come and join them! DANCE PARTY!".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
                else:
                    embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(ctx.message.author.mention) + " started dancing with {}".format(ctx.message.mentions[0].mention) + ".\n\n[Image link](" + chosen + ")")
            else:
                embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} started dancing by themselves! Everyone, come and join them! DANCE PARTY!".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} started dancing by themselves! Everyone, come and join them! DANCE PARTY!".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Glomp someone",
                      brief="Glomp someone")
    async def glomp(self, ctx, user: discord.Member):
        chosen = random.choice(glomp_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} glomped themselves! Someone is very happy to see themselves!".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + " got a glomp from {}.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Hold someone's hand",
                      brief="Hold someone's hand",
                      aliases=['handhold', 'holdhand'])
    async def handholding(self, ctx, user: discord.Member):
        chosen = random.choice(handholding_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} tried to hold their own hand. Aww. Come here, I'll hold it for you.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(ctx.message.author.mention) + " is holding {}'s hand! How lewd!".format(user.mention) + "\n\n[Image Link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Hide yourself",
                      brief="Hide yourself")
    async def hide(self, ctx, *reason: str):
        chosen = random.choice(hide_links)
        if reason:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(ctx.message.author.mention) + " is hiding from " + ' '.join(reason) + ".\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(ctx.message.author.mention) + " is hiding. Are they embarrassed?\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="High five someone",
                      brief="High five someone",
                      aliases=['5'])
    async def highfive(self, ctx, user: discord.Member):
        chosen = random.choice(highfive_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} gave themselves a high five! You go! Gotta congratulate yourself when others don't.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + " got a high five from {}.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Hug someone",
                      brief="Hug someone")
    async def hug(self, ctx, user: discord.Member):
        chosen = random.choice(hug_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} hugged themselves! Hooray for self-appreciation!".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got hugged.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="KICK THEIR ASS\n\n(This is NOT a moderation command to kick a user from a server.)",
                      brief="Kick someone")
    async def kick(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} aimed to kick themselves. As they noticed, it's quite hard to actually do. So they didn't and went to watch their favorite show.".format(ctx.message.author.mention))
        else:
            chosen = random.choice(kick_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got kicked.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="What do you think it does",
                      brief="It's in the name")
    async def kill(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} tried to kill themselves. Luckily, they changed their mind and went to get food instead.".format(ctx.message.author.mention))
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got killed.".format(user.mention))
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Kiss someone",
                      brief="Kiss someone")
    async def kiss(self, ctx, user: discord.Member):
        chosen = random.choice(kiss_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} gave themselves a kiss! Self-love is very important after all.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got kissed.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="For something LEWD",
                      brief="LEWD")
    async def lewd(self, ctx, user: discord.Member = None):
        chosen = random.choice(lewd_links)
        if user:
            if user.id == ctx.message.author.id:
                embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="Calling yourself out for being lewd, **{}**? How self-aware you are. And yes. Why you gotta be so lewd?".format(user.mention) + "\n\n[Image link](" + chosen + ")")
            else:
                embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="Why you gotta be so lewd, **{}**?".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
                embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="Why you gotta be so lewd?\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Lick someone",
                      brief="Lick someone")
    async def lick(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} licked themselves. Maybe they are secretly a cat and value personal hygiene?".format(ctx.message.author.mention))
        else:
            chosen = random.choice(lick_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{0} licked {1}.".format(ctx.message.author.mention, user.mention) + "\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Notice someone",
                      brief="Notice someone")
    async def notice(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} noticed themselves. Yes, you are here, and yes, it's good you are.".format(ctx.message.author.mention))
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{0} got noticed by {1}.".format(user.mention, ctx.message.author.mention))
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Pat someone",
                      brief="Pat someone")
    async def pat(self, ctx, user: discord.Member):
        chosen = random.choice(pat_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} patted themselves. They deserve all the pats!".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got a pat.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Pat them on the back",
                      brief="Pat someone on the back",
                      aliases=["backpat"])
    async def patback(self, ctx, user: discord.Member):
        chosen = random.choice(patback_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} patted themselves on the back. Their flexibility is highly impressive and they deserve a pat on the back already for being this flexible.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got a pat on the back.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Pinch someone's cheeks",
                      brief="Pinch someone's cheeks")
    async def pinch(self, ctx, user: discord.Member):
        chosen = random.choice(pinch_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} pinched their own cheeks. Maybe they wanted to check if they were dreaming or not?".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got their cheeks pinched.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Poke someone",
                      brief="Poke someone")
    async def poke(self, ctx, user: discord.Member):
        chosen = random.choice(poke_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} poked themselves. It wasn't hard at all, just a soft boop. And they deserve a boop.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got poked.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Pout\nCan be given a reason",
                      brief="Pout")
    async def pout(self, ctx, *reason: str):
        chosen = random.choice(pout_links)
        if reason:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} pouted! They said it's because of ".format(ctx.message.author.mention) + ' '.join(reason) + ".\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} pouted! Ask them why.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Someone gonna get punched",
                      brief="Punch someone")
    async def punch(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} wanted to punch themselves. But they only lightly rubbed their belly.".format(ctx.message.author.mention))
        else:
            chosen = random.choice(punch_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got punched.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Salute someone\nCan be given a reason",
                      brief="Salute someone")
    async def salute(self, ctx, *reason: str):
        chosen = random.choice(salute_links)
        if reason:
            if ctx.message.author in ctx.message.mentions:
                embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} saluted themselves. They must be really proud of what they did. And I am proud of them too.".format(ctx.message.author.mention))
            else:
                embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} saluted ".format(ctx.message.author.mention) + ' '.join(reason) + ".")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} saluted someone or something. Ask them about it.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Slap 'em hard",
                      brief="Slap someone")
    async def slap(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} tried to slap themselves. 'Twas but a gentle caressing.".format(ctx.message.author.mention))
        else:
            chosen = random.choice(slap_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got slapped.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Be the smuggest of them all",
                      brief="Be smug")
    async def smug(self, ctx):
        chosen = random.choice(smug_links)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} is being smug.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Stab someone",
                      brief="Stab someone")
    async def stab(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} tried to stab themselves. Fortunately, their aim was off.".format(ctx.message.author.mention))
        else:
            chosen = random.choice(stab_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + " got stabbed by {}.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Tickle someone",
                      brief="Tickle someone")
    async def tickle(self, ctx, user: discord.Member):
        chosen = random.choice(tickle_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} tickled themselves. They must be really ticklish if they can do that!".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got tickled.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Wave at someone",
                      brief="Wave at someone")
    async def wave(self, ctx, user: discord.Member):
        chosen = random.choice(wave_links)
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} waved at themselves. They seem incredibly happy and energetic today. How cute!".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        else:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} waved at {}.".format(ctx.message.author.mention, user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Whip someone (rather kinky)",
                      brief="Whip someone")
    async def whip(self, ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} wants to whip themselves. They must be really kinky.".format(ctx.message.author.mention))
        else:
            chosen = random.choice(whip_links)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="Bow down, {}.".format(user.mention) + " Time for a whipping!\n\n[Image link](" + chosen + ")")
            embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Interaction(bot))
