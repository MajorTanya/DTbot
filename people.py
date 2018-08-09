import discord
from discord.ext import commands
import random

class People():
    """Signature things we have said"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="Something Berend says a lot",
                      brief="THE BEREND THING")
    async def berend(self):
        await self.bot.say('I am watching porn.')


    @commands.command(description="Something Demon says a lot",
                      brief="THE DEMON THING",
                      aliases=['angel'])
    async def demon(self):
        possible_responses = [
            'Fucking bitch boy',
            'I may or may not have a problem'
            ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Eins says a lot",
                      brief="THE EINS THING",
                      aliases=['lewis'])
    async def eins(self):
        possible_responses = [
                'Toastie-chan is my waifu :heart:',
                'I will lewd all of you'
                ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Exo says a lot",
                      brief="THE EXO THING")
    async def exo(self):
        possible_responses = [
                'Mom',
                'Senpai'
                ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something that Fichtenschweif says a lot",
                      brief="THE FICHTE THING",
                      aliases=['fichtenschweif'])
    async def fichte(self):
        await self.bot.say('Women are superior')


    @commands.command(description="Something Ian says a lot",
                      brief="THE IAN THING",
                      aliases=['ridley'])
    async def ian(self):
        await self.bot.say('XD')


    @commands.command(description="Something Joey says a lot",
                      brief="THE JOEY THING",
                      aliases=['shadow'])
    async def joey(self):
        await self.bot.say('<.<\n>.>\n<.>\n>.<')


    @commands.command(description="Something Josh says a lot",
                      brief="THE JOSH THING")
    async def josh(self):
        await self.bot.say('Remove kebab')


    @commands.command(description="Something Kami says a lot",
                      brief="THE KAMI THING")
    async def kami(self):
        await self.bot.say('???')


    @commands.command(description="Something Nishi says a lot",
                      brief="THE NISHI THING",
                      aliases=['nisher', 'nishnish'])
    async def nishi(self):
        await self.bot.say('I will peg Berend, Zero, Shaggy, Rech, Fichte, Josh, Ian, and Eins.')


    @commands.command(description="Something Neo says a lot",
                      brief="THE NEO THING")
    async def neo(self):
        await self.bot.say('Poof')


    @commands.command(description="Something Nobody says a lot",
                      brief="THE NOBODY THING",
                      aliases=['noby'])
    async def nobody(self):
        await self.bot.say('I HATE DUCKS\n:duck: :duck: :duck: :duck: :duck:')


    @commands.command(description="Something Rech says a lot",
                      brief="THE RECH THING")
    async def rech(self):
        await self.bot.say('SIT ON MY FACE!')


    @commands.command(description="Something Sophie says a lot",
                      brief="THE SOPHIE THING")
    async def sophie(self):
        await self.bot.say('You have been diagnosed with the gay')


    @commands.command(description="Something Shaggy says a lot",
                      brief="THE SHAGGY THING")
    async def shaggy(self):
        await self.bot.say('Heh')


    @commands.command(description="Something Sam says a lot",
                      brief="THE SAM THING")
    async def sam(self):
        await self.bot.say('Howdy')


    @commands.command(description="Something Tanya says a lot",
                      brief="THE TANYA THING")
    async def tanya(self):
        await self.bot.say('Hurt Nishi and I will kill you.\n<:kuu:476895536679616533> <:kuu:476895536679616533> <:kuu:476895536679616533> <:kuu:476895536679616533> <:kuu:476895536679616533>')


    @commands.command(description="Something Toasted says a lot",
                      brief="THE TOASTED THING")
    async def toasted(self):
        await self.bot.say(':egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg:')


    @commands.command(description="Something Zero says a lot",
                      brief="THE ZERO THING")
    async def zero(self):
        await self.bot.say('Even if I drink all the water in the universe, I will still be thirsty.')


def setup(bot):
    bot.add_cog(People(bot))
