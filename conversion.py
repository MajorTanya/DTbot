from discord.ext import commands

class Conversions():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description='Convert temperature from °Celsius to °Fahrenheit',
                      brief='°C > °F',
                      aliases=['ctof'])
    async def cf(self, number):
        cf_value = round(float(number) * 1.8 + 32, 2)
        await self.bot.say(str(cf_value) + '°F')


    @commands.command(description='Convert temperature from °Fahrenheit to °Celsius',
                      brief='°F > °C',
                      aliases=['ftoc'])
    async def fc(self, number):
        fc_value = round((float(number) - 32) / 1.8, 2)
        await self.bot.say(str(fc_value) + '°C')


    @commands.command(description='Convert from Centimeters to Inches',
                      brief='cm > in',
                      aliases=['cmtoin'])
    async def cminch(self, number):
        cminch_value = int(number) * 0.393701
        await self.bot.say(str(cminch_value) + ' inch')


    @commands.command(description='Convert from Inches to Centimeters',
                      brief='in > cm',
                      aliases=['intocm'])
    async def inchcm(self, number):
        inchcm_value = int(number) * 2.54
        await self.bot.say(str(inchcm_value) + ' cm')


    @commands.command(description='Convert from Feet to Meters',
                      brief='ft > m',
                      aliases=['fttom'])
    async def ftm(self, number):
        ftm_value = int(number) * 0.3048
        await self.bot.say(str(ftm_value) + ' m')


    @commands.command(description='Convert from Meters to Feet',
                      brief='m > ft',
                      aliases=['mtoft'])
    async def mft(self, number):
        mft_value = int(number) / 0.3048
        await self.bot.say(str(mft_value) + ' ft')


    @commands.command(description='Convert from Kilometers to Miles',
                      brief='km > mi',
                      aliases=['kitomi'])
    async def kmmi(self, number):
        kmmi_value = int(number) * 0.621371
        await self.bot.say(str(kmmi_value) + ' mi')


    @commands.command(description='Convert Miles to Kilometers',
                      brief='mi > km',
                      aliases=['mitokm'])
    async def mikm(self, number):
        mikm_value = int(number) / 0.621371
        await self.bot.say(str(mikm_value) + ' km')


def setup(bot):
    bot.add_cog(Conversions(bot))
