import re

from discord.ext import commands


class Conversion:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True,
                      name='ck',
                      description='Convert temperature from °Celsius to Kelvin\n\nUsage:\n+ck 25',
                      brief='°C    > K',
                      aliases=['ctok'])
    async def _________ck(self, number):
        ck_value = round(float(number) + 273.15, 2)
        await self.bot.say(str(ck_value) + '°K')


    @commands.command(hidden=True,
                      name='kc',
                      description='Convert temperature from Kelvin to °Celsius\n\nUsage:\n+kc 298.15',
                      brief='K    > °C',
                      aliases=['ktoc'])
    async def _________kc(self, number):
        ck_value = round(float(number) - 273.15, 2)
        await self.bot.say(str(ck_value) + '°C')


    @commands.command(hidden=True,
                      name='kf',
                      description='Convert temperature from Kelvin to °Fahrenheit\n\nUsage:\n+kf 298.15',
                      brief='K    > °F',
                      aliases=['ktof'])
    async def ________kf(self, number):
        ck_value = round(float(number) * 9/5 - 459.67, 2)
        await self.bot.say(str(ck_value) + '°F')


    @commands.command(hidden=True,
                      name='fk',
                      description='Convert temperature from Kelvin to °Fahrenheit\n\nUsage:\n+fk 77',
                      brief='°F    > K',
                      aliases=['ftok'])
    async def ________fk(self, number):
        ck_value = round((float(number) + 459.67) * 5/9, 2)
        await self.bot.say(str(ck_value) + 'K')


    @commands.command(name='cf',
                      description='Convert temperature from °Celsius to °Fahrenheit\n\nUsage:\n+cf 25',
                      brief='°C    > °F',
                      aliases=['ctof'])
    async def _______cf(self, number):
        cf_value = round(float(number) * 1.8 + 32, 2)
        await self.bot.say(str(cf_value) + '°F')


    @commands.command(name='fc',
                      description='Convert temperature from °Fahrenheit to °Celsius\n\nUsage:\n+fc 77',
                      brief='°F    > °C',
                      aliases=['ftoc'])
    async def _______fc(self, number):
        fc_value = round((float(number) - 32) / 1.8, 2)
        await self.bot.say(str(fc_value) + '°C')


    @commands.command(name='cmin',
                      description='Convert from Centimeters to Inches\n\nUsage:\n+cmin 25.40',
                      brief='cm    > in',
                      aliases=['cmtoin'])
    async def ______cmin(self, number):
        cminch_value = round(float(number) * 0.393701, 2)
        await self.bot.say(str(cminch_value) + ' inch')


    @commands.command(name='incm',
                      description='Convert from Inches to Centimeters\n\nUsage:\n+incm 10',
                      brief='in    > cm',
                      aliases=['intocm'])
    async def ______incm(self, number):
        inchcm_value = round(float(number) * 2.54, 2)
        await self.bot.say(str(inchcm_value) + ' cm')


    @commands.command(name='ftm',
                      description='Convert from Feet to Meters\n\nUsage:\n+ftm 3.28',
                      brief='ft    > m',
                      aliases=['fttom'])
    async def _____ftm(self, number):
        ftm_value = round(float(number) * 0.3048, 2)
        await self.bot.say(str(ftm_value) + ' m')


    @commands.command(name='mft',
                      description='Convert from Meters to Feet\n\nUsage:\n+mft 1',
                      brief='m     > ft',
                      aliases=['mtoft'])
    async def _____mft(self, number):
        mft_value = round(float(number) / 0.3048, 2)
        await self.bot.say(str(mft_value) + ' ft')


    @commands.command(name='kglbs',
                      description='Convert from Kilograms to Pounds\n\nUsage:\n+kglbs 63.5',
                      brief='kg    > lbs',
                      aliases=['kgtolbs'])
    async def ____kglbs(self, number):
        kglbs_value = round(float(number) / 0.45359237, 2)
        await self.bot.say(str(kglbs_value) + ' lbs')


    @commands.command(name='lbskg',
                      description='Convert from Pounds to Kilograms\n\nUsage:\n+lbskg 140',
                      brief='lbs   > kg',
                      aliases=['lbstokg'])
    async def ____lbskg(self, number):
        lbskg_value = round(float(number) * 0.45359237, 2)
        await self.bot.say(str(lbskg_value) + ' kg')


    @commands.command(name='kmmi',
                      description='Convert from Kilometers to Miles\n\nUsage:\n+kmmi 128.75',
                      brief='km    > mi',
                      aliases=['kitomi'])
    async def ___kmmi(self, number):
        kmmi_value = round(float(number) * 0.621371, 2)
        await self.bot.say(str(kmmi_value) + ' mi')


    @commands.command(name='mikm',
                      description='Convert Miles to Kilometers\n\nUsage:\n+mikm 80',
                      brief='mi    > km',
                      aliases=['mitokm'])
    async def ___mikm(self, number):
        mikm_value = round(float(number) / 0.621371, 2)
        await self.bot.say(str(mikm_value) + ' km')


    @commands.command(name='ftinm',
                      description='Convert from mixed US Customary length units to Meters\n(no space between number and unit, if unit is given)\n\nUsage:\n+ftinm 6ft 2in\nOr:\n+ftinm 6 2\n',
                      brief='ft in > m',
                      aliases=['ftintom'])
    async def __ftinm(self, feet, inches):
        feet_int = re.sub("[^0-9]", '', feet)
        inches_int = re.sub('[^0-9]', '', inches)
        await self.bot.say(str(round((int(feet_int) * 0.3048) + (int(inches_int) * 0.0254), 2)) + "m")


    @commands.command(name='mftin',
                      description='Convert from Meters to mixed US Customary length units\n\nUsage:\n+mftin 1.88m \nOr:\n+mftin 1.88',
                      brief='m     > ft in',
                      aliases=['mtoftin'])
    async def __mftin(self, meters):
        meters_int = re.sub('[^0-9.]', '', meters)
        feetfrommeters = divmod(float(meters_int), 0.3048)
        inchesfrommeters = divmod(feetfrommeters[1], 0.0254)
        await self.bot.say(str(int(feetfrommeters[0])) + "ft " + str(int(inchesfrommeters[0])) + "in")


    @commands.command(name='flozml',
                      description='Convert from US Fluid Ounces to Milliliters\n\nUsage:\n+flozml 10',
                      brief='fl oz > ml',
                      aliases=['floztoml'])
    async def _flozml(self, number):
        ml_value = round(float(number) * 29.5735, 2)
        await self.bot.say(str(ml_value) + ' ml')


    @commands.command(name='mlfloz',
                      description='Convert from Milliliters to US Fluid Ounces\n\nUsage:\n+mlfloz 10',
                      brief='ml    > fl oz',
                      aliases=['mltofloz'])
    async def _mlfloz(self, number):
        floz_value = round(float(number) * 0.033814, 2)
        await self.bot.say(str(floz_value) + ' fl oz')


    @commands.command(name='gall',
                      description='Convert from US Gallons to Liters\n\nUsage:\n+gall 26.41',
                      brief='gal   > l',
                      aliases=['galtol'])
    async def gall(self, number):
        gal_value = round(float(number) * 3.785411784, 2)
        await self.bot.say(str(gal_value) + ' l')


    @commands.command(name='lgal',
                      description='Convert from Liters to US Gallons\n\nUsage:\n+lgal 100',
                      brief='l     > gal',
                      aliases=['ltogal'])
    async def lgal(self, number):
        l_value = round(float(number) * 0.2641720524, 2)
        await self.bot.say(str(l_value) + ' gal (US)')


def setup(bot):
    bot.add_cog(Conversion(bot))
