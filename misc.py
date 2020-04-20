import random

from discord.ext import commands
from discord.ext.commands import cooldown


class Misc(commands.Cog):
    """Miscellaneous commands for fun"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="SAY BLESS YOU TO THE CAT",
                      brief="Say bless you to the cat")
    @cooldown(3, 60, commands.BucketType.guild)
    async def cat(self, ctx):
        await ctx.send('<:sneezecat:472732802727804928> <:sneezecat:472732802727804928> '
                       '<:sneezecat:472732802727804928> <:sneezecat:472732802727804928> '
                       '<:sneezecat:472732802727804928>')

    @commands.command(description="For when you need to pay a lot of respects",
                      brief="Pay big Respects")
    async def bigf(self, ctx):
        await ctx.send('FFFFFFFFFFFFFFFFFFF\nFFFFFFFFFFFFFFFFFFF\nFFFFFFFFFF\nFFFFFFFFFF\nFFFFFFFFFFFFFFFFFFF\n'
                       'FFFFFFFFFFFFFFFFFFF\nFFFFFFFFFF\nFFFFFFFFFF\nFFFFFFFFFF\nFFFFFFFFFF')

    @commands.command(description="To Pay Respects",
                      brief="Pay Respects")
    async def f(self, ctx):
        await ctx.send('fffffffffffffff\nfffffff\nfffffffffffffff\nfffffff\nfffffff')

    @commands.command(description="Actually you can't",
                      brief="Kill yourself")
    async def kms(self, ctx):
        possible_responses = [
            'NO',
            'NEVER',
            'HOW ABOUT NO',
            'Need a hug? <:kannahug:461996510637326386>',
            'Yeah, sure. *If* you can do it in the next nanosecond.\nWell, you failed. Then my answer is no.',
            'NOPE',
            'What would you say if I told you that it is impossible',
            "Your pet wouldn't know why you didn't come home, so no.",
            "We would miss you, so don't."
        ]
        await ctx.send(random.choice(possible_responses))

    @commands.command(description="IT'S JUST A REEE BRO",
                      brief="REEEEE")
    @cooldown(3, 120, commands.BucketType.guild)
    async def re(self, ctx):
        await ctx.send('REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')


def setup(bot):
    bot.add_cog(Misc(bot))
