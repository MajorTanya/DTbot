import random

from discord.ext import commands


class People:
    """Signature things we have said"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Something Ava says a lot",
                      brief="THE AVA THING")
    async def ava(self):
        possible_responses = [
            '> I like headpats',
            '> im like \n> h\n> ok',
            '> <:happy:622247543690100745>'
        ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Berend says a lot",
                      brief="THE BEREND THING")
    async def berend(self):
        possible_responses = [
            '> I am watching porn.',
            '> I will rape your ears'
            ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Demon says a lot",
                      brief="THE DEMON THING",
                      aliases=['angel'])
    async def demon(self):
        possible_responses = [
            '> Fucking bitch boy',
            '> I may or may not have a problem'
            ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Eins says a lot",
                      brief="THE EINS THING",
                      aliases=['lewis'])
    async def eins(self):
        possible_responses = [
            '> Toastie-chan is my waifu :heart:',
            '> I will lewd all of you'
            ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Exo says a lot",
                      brief="THE EXO THING")
    async def exo(self):
        possible_responses = [
            '> Mom',
            '> Senpai'
            ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Faye says a lot",
                      brief="THE FAYE THING")
    async def faye(self):
        possible_responses = [
            '> Angel is a cutie',
            '> Should I pinch Angel?',
            '> wut whyyyyyy'
        ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something that Fichtenschweif says a lot",
                      brief="THE FICHTE THING",
                      aliases=['fichtenschweif', 'fishy', 'fishytails'])
    async def fichte(self):
        possible_responses = [
            '> Women are superior',
            '> Life is meaningless'
        ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Holo says a lot",
                      brief="THE HOLO THING")
    async def holo(self):
        possible_responses = [
            '> uwu',
            '> ams fooding',
            '> Hecc'
        ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Ian says a lot",
                      brief="THE IAN THING",
                      aliases=['ridley'])
    async def ian(self):
        await self.bot.say('> XD')


    @commands.command(name='iter',
                      description="Something Iter says a lot",
                      brief="THE ITER THING")
    async def user_iter(self):
        await self.bot.say("> I want to go to Demon's dungeon :3")


    @commands.command(description="Something Joey says a lot",
                      brief="THE JOEY THING",
                      aliases=['shadow'])
    async def joey(self):
        await self.bot.say('> <.<\n> >.>\n> <.>\n> >.<')


    @commands.command(description="Something Josh says a lot",
                      brief="THE JOSH THING")
    async def josh(self):
        await self.bot.say('> Remove kebab')


    @commands.command(description="Something Kami says a lot",
                      brief="THE KAMI THING")
    async def kami(self):
        await self.bot.say('> ???')


    @commands.command(description="Something Neo says a lot",
                      brief="THE NEO THING")
    async def neo(self):
        await self.bot.say('> Poof')


    @commands.command(description="Something Nishi says a lot",
                      brief="THE NISHI THING",
                      aliases=['nisher', 'nishnish'])
    async def nishi(self):
        possible_responses = [
            '> I will peg Berend, Zero, Shaggy, Rech, Fichte, Josh, Ian, and Eins.',
            '> I will take over every server'
            ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Nobody says a lot",
                      brief="THE NOBODY THING",
                      aliases=['noby'])
    async def nobody(self):
        await self.bot.say('> I HATE DUCKS\n:duck: :duck: :duck: :duck: :duck:')


    @commands.command(description="Something Rech says a lot",
                      brief="THE RECH THING")
    async def rech(self):
        await self.bot.say('> SIT ON MY FACE!')


    @commands.command(description="Something Sam says a lot",
                      brief="THE SAM THING")
    async def sam(self):
        await self.bot.say('> Howdy')


    @commands.command(description="Something Shaggy says a lot",
                      brief="THE SHAGGY THING")
    async def shaggy(self):
        await self.bot.say('> Heh')


    @commands.command(description="Something Sophie says a lot",
                      brief="THE SOPHIE THING")
    async def sophie(self):
        await self.bot.say('> You have been diagnosed with the gay')


    @commands.command(description="Something Tanya says a lot",
                      brief="THE TANYA THING")
    async def tanya(self):
        possible_responses = [
            '> I am an Elder Eldritch Being',
            '> Time for another political overdose',
            '> I am _literally_ a gazillion years old',
			'> Hurt Nishi and I will kill you.\n<:kuu:476895536679616533> <:kuu:476895536679616533> <:kuu:476895536679616533> <:kuu:476895536679616533> <:kuu:476895536679616533>'
        ]
        await self.bot.say(random.choice(possible_responses))


    @commands.command(description="Something Toasted says a lot",
                      brief="THE TOASTED THING")
    async def toasted(self):
        await self.bot.say('> :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg: :egg:')


    @commands.command(description="Something Zero says a lot",
                      brief="THE ZERO THING")
    async def zero(self):
        possible_responses = [
            '> Even if I drink all the water in the universe, I will still be thirsty.',
            "> It's not illegal if you don't get caught"
            ]
        await self.bot.say(random.choice(possible_responses))


def setup(bot):
    bot.add_cog(People(bot))
