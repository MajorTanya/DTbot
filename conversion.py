import re

from discord.ext import commands


class Conversion(commands.Cog):
    """Convert units, especially Metric and US Customary / Imperial"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True,
                      name='ck',
                      description='Convert temperature from °Celsius to Kelvin\n\nUsage:\n+ck 25  (Returns 298.15K)',
                      brief='°C    > K',
                      aliases=['ctok'])
    async def _________ck(self, ctx, celsius):
        celsius = re.sub("[^0-9.]", '', celsius)
        ck_value = round(float(celsius) + 273.15, 2)
        await ctx.send(f'{ck_value}K')

    @commands.command(hidden=True,
                      name='kc',
                      description='Convert temperature from Kelvin to °Celsius\n\nUsage:\n+kc 298.15 (Returns 25.0°C)',
                      brief='K    > °C',
                      aliases=['ktoc'])
    async def _________kc(self, ctx, kelvin):
        kelvin = re.sub("[^0-9.]", '', kelvin)
        ck_value = round(float(kelvin) - 273.15, 2)
        await ctx.send(f'{ck_value}°C')

    @commands.command(hidden=True,
                      name='kf',
                      description='Convert temperature from Kelvin to °Fahrenheit\n\nUsage:\n+kf 298.15 '
                                  '(Returns 77.0°F)',
                      brief='K    > °F',
                      aliases=['ktof'])
    async def ________kf(self, ctx, kelvin):
        kelvin = re.sub("[^0-9.]", '', kelvin)
        ck_value = round(float(kelvin) * 9 / 5 - 459.67, 2)
        await ctx.send(f'{ck_value}°F')

    @commands.command(hidden=True,
                      name='fk',
                      description='Convert temperature from Kelvin to °Fahrenheit\n\nUsage:\n+fk 77 (Returns 298.15K)',
                      brief='°F    > K',
                      aliases=['ftok'])
    async def ________fk(self, ctx, fahrenheit):
        fahrenheit = re.sub("[^0-9.]", '', fahrenheit)
        ck_value = round((float(fahrenheit) + 459.67) * 5 / 9, 2)
        await ctx.send(f'{ck_value}K')

    @commands.command(name='cf',
                      description='Convert temperature from °Celsius to °Fahrenheit\n\nUsage:\n+cf 25 (Returns 77.0°F)',
                      brief='°C    > °F',
                      aliases=['ctof'])
    async def _______cf(self, ctx, celsius):
        celsius = re.sub("[^0-9.]", '', celsius)
        cf_value = round(float(celsius) * 1.8 + 32, 2)
        await ctx.send(f'{cf_value}°F')

    @commands.command(name='fc',
                      description='Convert temperature from °Fahrenheit to °Celsius\n\nUsage:\n+fc 77 (Returns 25.0°C)',
                      brief='°F    > °C',
                      aliases=['ftoc'])
    async def _______fc(self, ctx, fahrenheit):
        fahrenheit = re.sub("[^0-9.]", '', fahrenheit)
        fc_value = round((float(fahrenheit) - 32) / 1.8, 2)
        await ctx.send(f'{fc_value}°C')

    @commands.command(name='cmin',
                      description='Convert from Centimeters to Inches\n\nUsage:\n+cmin 25.40 (Returns 10.0 inch)',
                      brief='cm    > in',
                      aliases=['cmtoin'])
    async def ______cmin(self, ctx, centimeters):
        centimeters = re.sub("[^0-9.]", '', centimeters)
        cminch_value = round(float(centimeters) * 0.393701, 2)
        await ctx.send(f'{cminch_value} inch')

    @commands.command(name='incm',
                      description='Convert from Inches to Centimeters\n\nUsage:\n+incm 10 (Returns 25.4 cm)',
                      brief='in    > cm',
                      aliases=['intocm'])
    async def ______incm(self, ctx, inches):
        inches = re.sub("[^0-9.]", '', inches)
        inchcm_value = round(float(inches) * 2.54, 2)
        await ctx.send(f'{inchcm_value} cm')

    @commands.command(name='ftm',
                      description='Convert from Feet to Meters\n\nUsage:\n+ftm 3.28 (Returns 1.0 m)',
                      brief='ft    > m',
                      aliases=['fttom'])
    async def _____ftm(self, ctx, feet):
        feet = re.sub("[^0-9.]", '', feet)
        ftm_value = round(float(feet) * 0.3048, 2)
        await ctx.send(f'{ftm_value} m')

    @commands.command(name='mft',
                      description='Convert from Meters to Feet\n\nUsage:\n+mft 1 (Returns 3.28 ft)',
                      brief='m     > ft',
                      aliases=['mtoft'])
    async def _____mft(self, ctx, meters):
        meters = re.sub("[^0-9.]", '', meters)
        mft_value = round(float(meters) / 0.3048, 2)
        await ctx.send(f'{mft_value} ft')

    class FtinmConv(commands.Converter):
        def __init__(self, ft, inch):
            self.feet = float(ft)
            self.inches = float(inch)

        async def convert(self, ctx, argument):
            argument1, argument2 = argument, 0
            if "\'" in argument or '\'' in argument or "ft" in argument.lower() or "in" in argument.lower():
                if "\'" in argument and '\"' in argument:
                    argument1 = argument.split("\'")[0]
                    argument2 = argument.split("\'")[1].split('\"')[0]
                elif "\'" in argument and '\"' not in argument:
                    argument1, argument2 = argument.split("\'")
                elif '\"' in argument and "\'" not in argument:
                    argument1, argument2 = argument.split('\"')
                if "ft" in argument1.lower():
                    argument1 = argument1.lower().split("ft")[0]
                    if not argument2:
                        argument2 = argument1.lower().split("ft")[1]
                if "in" in argument2.lower():
                    argument2 = argument2.split("in")[0]
            else:
                try:  # assume that a space separates feet and inches
                    argument1, argument2 = argument.split(" ")
                except:
                    pass
            try:
                self.feet = float(argument1)
                self.inches = float(argument2)
            except ValueError:
                raise commands.BadArgument("Only e.g. `6\' 2\"` or `6ft 2in` or `6 2` are valid input formats.")
            return self

    @commands.group(name='ftinm',
                    description='Convert from mixed US Customary length units to Meters\n(no space between number '
                                'and unit, if unit is given)\n\nUsage (spaces between feet and inches optional):\n'
                                '+ftinm 6ft 2in | +ftinm 6ft2in\nOr:\n+ftinm 6\' 2\" | +ftinm 6\'2\"\nOr:\n+ftinm 6 2'
                                '\n(Return 1.88m)\n',
                    brief='ft in > m',
                    aliases=['ftintom'])
    async def ____ftinm(self, ctx, *, feet_inches: FtinmConv(0, 0)):
        # send default values so still stored old ones don't get delivered
        if isinstance(feet_inches.feet, float) and isinstance(feet_inches.inches, float):
            await ctx.send(f"{round((feet_inches.feet * 0.3048) + (feet_inches.inches * 0.0254), 2)} m")

    @commands.command(name='mftin',
                      description='Convert from Meters to mixed US Customary length units\n\nUsage:\n+mftin 1.88m \n '
                                  'Or:\n+mftin 1.88 (Return 6 ft 2.0 in)',
                      brief='m     > ft in',
                      aliases=['mtoftin'])
    async def ____mftin(self, ctx, meters):
        meters = re.sub('[^0-9.]', '', meters)
        feetfrommeters = divmod(float(meters), 0.3048)
        inchesfrommeters = feetfrommeters[1] / 0.0254
        await ctx.send(f"{int(feetfrommeters[0])} ft {round(inchesfrommeters, 1)} in")

    @commands.command(name='kmmi',
                      description='Convert from Kilometers to Miles\n\nUsage:\n+kmmi 128.75 (Returns 80.0 mi)',
                      brief='km    > mi',
                      aliases=['kitomi'])
    async def ___kmmi(self, ctx, kilometers):
        kilometers = re.sub("[^0-9.]", '', kilometers)
        kmmi_value = round(float(kilometers) * 0.621371, 2)
        await ctx.send(f'{kmmi_value} mi')

    @commands.command(name='mikm',
                      description='Convert Miles to Kilometers\n\nUsage:\n+mikm 80 (Returns 128.75 km)',
                      brief='mi    > km',
                      aliases=['mitokm'])
    async def ___mikm(self, ctx, miles):
        miles = re.sub("[^0-9.]", '', miles)
        mikm_value = round(float(miles) / 0.621371, 2)
        await ctx.send(f'{mikm_value} km')

    @commands.command(name='kglbs',
                      description='Convert from Kilograms to Pounds\n\nUsage:\n+kglbs 70 (Returns 154.32 lbs)',
                      brief='kg    > lbs',
                      aliases=['kgtolbs'])
    async def __kglbs(self, ctx, kilograms):
        kilograms = re.sub("[^0-9.]", '', kilograms)
        kglbs_value = round(float(kilograms) / 0.45359237, 2)
        await ctx.send(f'{kglbs_value} lbs')

    @commands.command(name='lbskg',
                      description='Convert from Pounds to Kilograms\n\nUsage:\n+lbskg 154.32 (Returns 70.0 kg)',
                      brief='lbs   > kg',
                      aliases=['lbstokg'])
    async def __lbskg(self, ctx, pounds):
        pounds = re.sub("[^0-9.]", '', pounds)
        lbskg_value = round(float(pounds) * 0.45359237, 2)
        await ctx.send(f'{lbskg_value} kg')

    @commands.command(name='flozml',
                      description='Convert from US Fluid Ounces to Milliliters\n\nUsage:\n+flozml 10 '
                                  '(Returns 395.74 ml)',
                      brief='fl oz > ml',
                      aliases=['floztoml'])
    async def _flozml(self, ctx, floz):
        floz = re.sub("[^0-9.]", '', floz)
        ml_value = round(float(floz) * 29.5735, 2)
        await ctx.send(f'{ml_value} ml')

    @commands.command(name='mlfloz',
                      description='Convert from Milliliters to US Fluid Ounces\n\nUsage:\n+mlfloz 395.74 '
                                  '(Returns 10.0 fl oz)',
                      brief='ml    > fl oz',
                      aliases=['mltofloz'])
    async def _mlfloz(self, ctx, milliliters):
        milliliters = re.sub("[^0-9.]", '', milliliters)
        floz_value = round(float(milliliters) * 0.033814, 2)
        await ctx.send(f'{floz_value} fl oz')

    @commands.command(name='gall',
                      description='Convert from US Gallons to Liters\n\nUsage:\n+gall 26.42 (Returns 100 l)',
                      brief='gal   > l',
                      aliases=['galtol'])
    async def gall(self, ctx, gallons):
        gallons = re.sub("[^0-9.]", '', gallons)
        gal_value = round(float(gallons) * 3.785411784, 2)
        await ctx.send(f'{gal_value} l')

    @commands.command(name='lgal',
                      description='Convert from Liters to US Gallons\n\nUsage:\n+lgal 100 (Returns 26.42 gal (US))',
                      brief='l     > gal',
                      aliases=['ltogal'])
    async def lgal(self, ctx, liters):
        liters = re.sub("[^0-9.]", '', liters)
        l_value = round(float(liters) * 0.2641720524, 2)
        await ctx.send(f'{l_value} gal (US)')


def setup(bot):
    bot.add_cog(Conversion(bot))
