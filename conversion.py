from discord.ext import commands
import re

class Conversion():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True,
                      name='ck',
                      description='Convert temperature from °Celsius to Kelvin',
                      brief='°C    > K',
                      aliases=['ctok'])
    async def _______ck(self, number):
        ck_value = round(float(number) + 273.15, 2)
        await self.bot.say(str(ck_value) + '°K')


    @commands.command(hidden=True,
                      name='kc',
                      description='Convert temperature from Kelvin to °Celsius',
                      brief='K    > °C',
                      aliases=['ktoc'])
    async def _______kc(self, number):
        ck_value = round(float(number) - 273.15, 2)
        await self.bot.say(str(ck_value) + '°C')


    @commands.command(hidden=True,
                      name='kf',
                      description='Convert temperature from Kelvin to °Fahrenheit',
                      brief='K    > °F',
                      aliases=['ktof'])
    async def ______kf(self, number):
        ck_value = round(float(number) * 9/5 - 459.67, 2)
        await self.bot.say(str(ck_value) + '°F')


    @commands.command(hidden=True,
                      name='fk',
                      description='Convert temperature from Kelvin to °Fahrenheit',
                      brief='°F    > K',
                      aliases=['ftok'])
    async def ______fk(self, number):
        ck_value = round((float(number) + 459.67) * 5/9, 2)
        await self.bot.say(str(ck_value) + 'K')


    @commands.command(name='cf',
                      description='Convert temperature from °Celsius to °Fahrenheit',
                      brief='°C    > °F',
                      aliases=['ctof'])
    async def _____cf(self, number):
        cf_value = round(float(number) * 1.8 + 32, 2)
        await self.bot.say(str(cf_value) + '°F')


    @commands.command(name='fc',
                      description='Convert temperature from °Fahrenheit to °Celsius',
                      brief='°F    > °C',
                      aliases=['ftoc'])
    async def _____fc(self, number):
        fc_value = round((float(number) - 32) / 1.8, 2)
        await self.bot.say(str(fc_value) + '°C')


    @commands.command(name='cmin',
                      description='Convert from Centimeters to Inches',
                      brief='cm    > in',
                      aliases=['cmtoin'])
    async def ____cmin(self, number):
        cminch_value = round(float(number) * 0.393701, 2)
        await self.bot.say(str(cminch_value) + ' inch')


    @commands.command(name='incm',
                      description='Convert from Inches to Centimeters',
                      brief='in    > cm',
                      aliases=['intocm'])
    async def ____incm(self, number):
        inchcm_value = round(float(number) * 2.54, 2)
        await self.bot.say(str(inchcm_value) + ' cm')


    @commands.command(name='ftm',
                      description='Convert from Feet to Meters',
                      brief='ft    > m',
                      aliases=['fttom'])
    async def ___ftm(self, number):
        ftm_value = round(float(number) * 0.3048, 2)
        await self.bot.say(str(ftm_value) + ' m')


    @commands.command(name='mft',
                      description='Convert from Meters to Feet',
                      brief='m     > ft',
                      aliases=['mtoft'])
    async def ___mft(self, number):
        mft_value = round(float(number) / 0.3048, 2)
        await self.bot.say(str(mft_value) + ' ft')


    @commands.command(name='kglbs',
                      description='Convert from Kilograms to Pounds',
                      brief='kg    > lbs',
                      aliases=['kgtolbs'])
    async def __kglbs(self, number):
        kglbs_value = round(float(number) / 0.45359237, 2)
        await self.bot.say(str(kglbs_value) + ' lbs')


    @commands.command(name='lbskg',
                      description='Convert from Pounds to Kilograms',
                      brief='lbs   > kg',
                      aliases=['lbstokg'])
    async def __lbskg(self, number):
        lbskg_value = round(float(number) * 0.45359237, 2)
        await self.bot.say(str(lbskg_value) + ' kg')


    @commands.command(name='kmmi',
                      description='Convert from Kilometers to Miles',
                      brief='km    > mi',
                      aliases=['kitomi'])
    async def _kmmi(self, number):
        kmmi_value = round(float(number) * 0.621371, 2)
        await self.bot.say(str(kmmi_value) + ' mi')


    @commands.command(name='mikm',
                      description='Convert Miles to Kilometers',
                      brief='mi    > km',
                      aliases=['mitokm'])
    async def _mikm(self, number):
        mikm_value = round(float(number) / 0.621371, 2)
        await self.bot.say(str(mikm_value) + ' km')


    @commands.command(description='Convert from mixed US Customary length units to meters\n(no space between number and unit, if unit is given)\n\nUsage:\n+ftinm 6ft 2in\nOr:\n+ftinm 6 2\n',
                      brief='ft in > m',
                      aliases=['ftintom'])
    async def ftinm(self, feet, inches):
        feet_int = re.sub("[^0-9]", '', feet)
        inches_int = re.sub('[^0-9]', '', inches)
        await self.bot.say(str(round((int(feet_int) * 0.3048) + (int(inches_int) * 0.0254), 2)) + "m")


    @commands.command(description='Convert from meters to mixed US Customary length units\n\nUsage:\n+mftin 1.88m \nOr:\n+mftin 1.88',
                      brief='m     > ft in',
                      aliases=['mtoftin'])
    async def mftin(self, meters):
        meters_int = re.sub('[^0-9.]', '', meters)
        feetfrommeters = divmod(float(meters_int), 0.3048)
        inchesfrommeters = divmod(feetfrommeters[1], 0.0254)
        await self.bot.say(str(int(feetfrommeters[0])) + "ft " + str(int(inchesfrommeters[0])) + "in")


def setup(bot):
    bot.add_cog(Conversion(bot))
