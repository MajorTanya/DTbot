import random
import discord
import asyncio
from discord.ext import commands
from DTbot import bot
from linklist import baddoggo_links, bkiss_links, blush_links, cage_links, cuddle_links, glomp_links, handholding_links, highfive_links, hug_links, kiss_links, pat_links, pinch_links, poke_links, punch_links, slap_links, stab_links, whip_links

class Interaction():
    """Commands which interact with others"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True,
                      description='Call someone a bad doggo',
                      brief='Call someone a bad doggo',
                      aliases=['shame', 'baddog'])
    async def baddoggo(self, ctx, user: discord.Member):
        possible_responses = baddoggo_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + ", you're being a very bad dog! {} is disappointed in you!".format(ctx.message.author.mention) + "\n\n[Image Link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Bitch slaps someone",
                      brief="Bitch slaps someone",
                      aliases=['Bitchslap'])
    async def bitchslap(self, ctx, user: discord.Member):
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got a bitch slap.".format(user.mention) + "\n\n[Image link](https://i.imgur.com/bTGigCv.gif)")
        embed.set_image(url="https://i.imgur.com/bTGigCv.gif")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Kiss someone the non-romantic way",
                      brief="A non-romantic kiss")
    async def bkiss(self, ctx, user: discord.Member):
        possible_responses = bkiss_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got kissed.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Blush",
                      brief="Blush")
    async def blush(self, ctx):
        possible_responses = blush_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} blushed! How cute!".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Cuddle someone",
                      brief="Cuddle someone")
    async def cuddle(self, ctx, user: discord.Member):
        possible_responses = cuddle_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got cuddled.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Cage someone",
                      brief="Cage someone")
    async def cage(self, ctx, user: discord.Member):
        possible_responses = cage_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got caged.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description='Confess your feelings to someone',
                      brief='Confess your feelings to someone')
    async def confess(self, ctx, user: discord.Member):
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + ", you've been confessed to by {}!".format(ctx.message.author.mention) + "\nWill you let the ship set sail or will you sink it before its journey starts? " + u"\u26F5")
        message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(message, u"\u2764")
        await self.bot.add_reaction(message, u"\U0001F494")
        await asyncio.sleep(1)
        
        def check(reaction, user):
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
                      description="Glomp someone",
                      brief="Glomp someone")
    async def glomp(self, ctx, user: discord.Member):
        possible_responses = glomp_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + " got a glomp from {}.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Hold someone's hand",
                      brief="Hold someone's hand",
                      aliases=['handhold', 'holdhand'])
    async def handholding(self, ctx, user: discord.Member):
        possible_responses = handholding_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(ctx.message.author.mention) + " is holding {}'s hand! How lewd!".format(user.mention) + "\n\n[Image Link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="High five someone",
                      brief="High five someone",
                      aliases=['5'])
    async def highfive(self, ctx, user: discord.Member):
        possible_responses = highfive_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + " got a high five from {}.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Hug someone",
                      brief="Hug someone")
    async def hug(self, ctx, user: discord.Member):
        possible_responses = hug_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got hugged.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="What do you think it does",
                      brief="It's in the name")
    async def kill(self, ctx, user: discord.Member):
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got killed.".format(user.mention))
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Kiss someone",
                      brief="Kiss someone")
    async def kiss(self, ctx, user: discord.Member):
        possible_responses = kiss_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got kissed.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="For something LEWD",
                      brief="LEWD")
    async def lewd(self, ctx, user: discord.Member = None):
        if user:
                await self.bot.say('Why you gotta be so lewd, **{}**?'.format(user.display_name))
        else:
                await self.bot.say('Why you gotta be so lewd?')


    @commands.command(pass_context=True,
                      description="Pat someone",
                      brief="Pat someone")
    async def pat(self, ctx, user: discord.Member):
        possible_responses = pat_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got a pat.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Pinch someone's cheeks",
                      brief="Pinch someone's cheeks")
    async def pinch(self, ctx, user: discord.Member):
        possible_responses = pinch_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got their cheeks pinched.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Poke someone",
                      brief="Poke someone")
    async def poke(self, ctx, user: discord.Member):
        possible_responses = poke_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got poked.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Someone gonna get punched",
                      brief="Punch club")
    async def punch(self, ctx, user: discord.Member):
        possible_responses = punch_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got punched.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Slap 'em hard",
                      brief="Slap someone")
    async def slap(self, ctx, user: discord.Member):
        possible_responses = slap_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got slapped.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Stab someone",
                      brief="Stab someone")
    async def stab(self, ctx, user: discord.Member):
        possible_responses = stab_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + " got stabbed by {}.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Whip someone",
                      brief="Whip someone")
    async def whip(self, ctx, user: discord.Member):
        possible_responses = whip_links
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="Bow down, {}.".format(user.mention) + " Time for a whipping!\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Interaction(bot))
