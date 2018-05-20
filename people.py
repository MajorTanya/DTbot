import discord
from discord.ext import commands

class People():
    """Signature things we have said"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Something Berend says a lot",
                      brief="THE BEREND THING",
                      aliases=['Berend'])
    async def berend(self):
        await self.bot.say('I am watching porn.')


    @commands.command(description="Something Demon says a lot",
                      brief="THE DEMON THING",
                      aliases=['Demon'])
    async def demon(self):
        await self.bot.say('Fucking bitch')


    @commands.command(description="Something Exo says a lot",
                      brief="THE EXO THING",
                      aliases=['Exo'])
    async def exo(self):
        possible_responses = [
                'Mom',
                'Major'
                ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Ian says a lot",
                      brief="THE IAN THING",
                      aliases=['Ian'])
    async def ian(self):
        await self.bot.say('XD')


    @commands.command(description="Something Joey says a lot",
                      brief="THE JOEY THING",
                      aliases=['Joey', 'shadow', 'Shadow'])
    async def joey(self):
        await self.bot.say('<.<\n>.>\n<.>\n>.<')


    @commands.command(description="Something Josh says a lot",
                      brief="THE JOSH THING",
                      aliases=['Josh'])
    async def josh(self):
        await self.bot.say('Remove kebab')


    @commands.command(description="Something Kami says a lot",
                      brief="THE KAMI THING",
                      aliases=['Kami'])
    async def kami(self):
        await self.bot.say('???')


    @commands.command(description="Something Momiji says a lot",
                      brief="THE MOMIJI THING",
                      aliases=['Momiji'])
    async def momiji(self):
        await self.bot.say('Bunch of weaklings')


    @commands.command(description="Something Nishi says a lot",
                      brief="THE NISHI THING",
                      aliases=['Nishi', 'Nisher', 'nisher', 'Nishnish', 'nishnish'])
    async def nishi(self):
        await self.bot.say('I will peg Berend, Zero, Shaggy, Rech, Fichte, and Josh.')


    @commands.command(description="Something Neo says a lot",
                      brief="THE NEO THING",
                      aliases=['Neo'])
    async def neo(self):
        await self.bot.say('Poof')


    @commands.command(description="Something Rech says a lot",
                      brief="THE RECH THING",
                      aliases=['Rech'])
    async def rech(self):
        await self.bot.say('SIT ON MY FACE!')


    @commands.command(description="Something Sophie says a lot",
                      brief="THE SOPHIE THING",
                      aliases=['Sophie'])
    async def sophie(self):
        await self.bot.say('You have been diagnosed with the gay')


    @commands.command(description="Something Shaggy says a lot",
                      brief="THE SHAGGY THING",
                      aliases=['Shaggy'])
    async def shaggy(self):
        await self.bot.say('Heh')


    @commands.command(description="Something Sam says a lot",
                      brief="THE SAM THING",
                      aliases=['Sam'])
    async def sam(self):
        await self.bot.say('Howdy')


    @commands.command(description="Something Tanya says a lot",
                      brief="THE TANYA THING",
                      aliases=['Tanya'])
    async def tanya(self):
        await self.bot.say('Hurt Nishi and I will kill you.\n<:kuu:347272585568059393> <:kuu:347272585568059393> <:kuu:347272585568059393> <:kuu:347272585568059393> <:kuu:347272585568059393>')


    @commands.command(description="Something Toasted says a lot",
                      brief="THE TOASTED THING",
                      aliases=['Toasted'])
    async def toasted(self):
        await self.bot.say(':egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg:')


    @commands.command(description="Something White said that one time",
                      brief="THE WHITE THING",
                      aliases=['White'])
    async def white(self):
        await self.bot.say('The voices in your head never end.')


    @commands.command(description="Something Zero says a lot",
                      brief="THE ZERO THING",
                      aliases=['Zero'])
    async def zero(self):
        await self.bot.say('Even if I drink all the water in the universe, I will still be thirsty.')


def setup(bot):
    bot.add_cog(People(bot))
