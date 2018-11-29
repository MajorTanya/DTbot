import random

import discord
from discord.ext import commands


class Misc():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="Try and see",
                      brief="Try and see")
    async def bitcoin(self):
        await self.bot.say('Have a bitcoin.')


    @commands.command(description="SAY BLESS YOU TO THE CAT",
                      brief="Say bless you to the cat")
    @commands.cooldown(3, 60, commands.BucketType.server)
    # cooldown of 60 seconds
    async def cat(self):
        await self.bot.say('<:sneezecat:472732802727804928> <:sneezecat:472732802727804928> <:sneezecat:472732802727804928> <:sneezecat:472732802727804928> <:sneezecat:472732802727804928>')


    @commands.command(description="The face of craziness",
                      brief="The face of craziness")
    @commands.cooldown(3, 60, commands.BucketType.server)
    # cooldown of 60 seconds
    async def crazy(self):
        await self.bot.say('<:crazy:476896897286799371> <:crazy:476896897286799371> <:crazy:476896897286799371> <:crazy:476896897286799371> <:crazy:476896897286799371>')


    @commands.command(description="Actually you can't",
                      brief="Kill yourself")
    async def kms(self):
        possible_responses = [
            'NO',
            'NEVER',
            'HOW ABOUT NO',
            'Need a hug?',
            'Yeah, sure. *If* you can do it in the next nanosecond.\nWell, you failed. Then my answer is no.',
            'NOPE',
            'What would you say if I told you that it is impossible'
            ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="A random quote from the server",
                      brief="Quote me")
    async def quote(self):
        possible_responses = [
                'https://i.imgur.com/60hKnCs.png',
                'https://i.imgur.com/pBGlIed.png',
                'https://i.imgur.com/N3TrhhH.png',
                'https://i.imgur.com/k2Ipuil.png',
                'https://i.imgur.com/ezJb1z1.png',
                'https://i.imgur.com/JXr2X90.png',
                'https://i.imgur.com/rlu9Iyc.png',
                'https://i.imgur.com/Iiwd3wR.png',
                'https://i.imgur.com/o9n988v.png',
                'https://i.imgur.com/HQW8qQM.png',
                'https://i.imgur.com/bdM5nsm.png',
                'https://i.imgur.com/KupYQlU.png',
                'https://i.imgur.com/QCU9WM5.png',
                'https://i.imgur.com/Z1ltrfi.png',
                'https://i.imgur.com/ffMEOLz.png',
                'https://i.imgur.com/Gg06uLg.png',
                'https://i.imgur.com/qX6yi7k.png',
                'https://i.imgur.com/jQuiT9Q.png',
                'https://i.imgur.com/WBay8cY.png',
                'https://i.imgur.com/HD7ZnrH.png',
                'https://i.imgur.com/w6UcH4w.png',
                'https://i.imgur.com/OXOsy2q.png',
                'https://i.imgur.com/IeMI9aW.png',
                'https://i.imgur.com/DQCSglA.png',
                'https://i.imgur.com/qmoirvy.png',
                'https://i.imgur.com/P7lxLp2.png',
                'https://i.imgur.com/sJoTstH.png',
                'https://i.imgur.com/zBWWip7.png',
                'https://i.imgur.com/e6i9Y2n.png',
                'https://i.imgur.com/7aYaV7K.png'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="A quote for you:" + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)
        # that quote
        if chosen == 'https://i.imgur.com/e6i9Y2n.png':
                await self.bot.say('<@287727207642693633>, this is for you.')


    @commands.command(description="IT'S JUST A REEE BRO",
                      brief="REEEEE")
    @commands.cooldown(3, 120, commands.BucketType.server)
    # cooldown of 2 minutes to prevent massive spams
    async def re(self):
        await self.bot.say('REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')


    @commands.command(hidden=True,
                      description="ZERO SPAM",
                      brief="ZERO TIME")
    async def zeroarmy(self):
        await self.bot.say('Zero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero')


def setup(bot):
    bot.add_cog(Misc(bot))
