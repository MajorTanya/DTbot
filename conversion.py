import re

from nextcord.ext import commands


class Conversion(commands.Cog):
    """Convert units, especially Metric and US Customary / Imperial"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True,
                      description='Convert temperature from °Celsius to Kelvin\n\nUsage:\n+ck 25  (Returns 298.15K)',
                      brief='°C > K',
                      aliases=['ctok'])
    async def ck(self, ctx, celsius):
        celsius = ('-' if celsius[0] == '-' else '') + re.sub('[^0-9.]+', '', celsius)
        ck_value = round(float(celsius) + 273.15, 2)
        await ctx.send(f'{round(float(celsius), 2)}°C = {ck_value}K')

    @commands.command(hidden=True,
                      description='Convert temperature from Kelvin to °Celsius\n\nUsage:\n+kc 298.15 (Returns 25.0°C)',
                      brief='K > °C',
                      aliases=['ktoc'])
    async def kc(self, ctx, kelvin):
        kelvin = ('-' if kelvin[0] == '-' else '') + re.sub('[^0-9.]+', '', kelvin)
        ck_value = round(float(kelvin) - 273.15, 2)
        await ctx.send(f'{round(float(kelvin), 2)}K = {ck_value}°C')

    @commands.command(hidden=True,
                      description='Convert temperature from Kelvin to °Fahrenheit\n\nUsage:\n+kf 298.15 '
                                  '(Returns 77.0°F)',
                      brief='K > °F',
                      aliases=['ktof'])
    async def kf(self, ctx, kelvin):
        kelvin = ('-' if kelvin[0] == '-' else '') + re.sub('[^0-9.]', '', kelvin)
        ck_value = round(float(kelvin) * 9 / 5 - 459.67, 2)
        await ctx.send(f'{round(float(kelvin), 2)}K = {ck_value}°F')

    @commands.command(hidden=True,
                      description='Convert temperature from Kelvin to °Fahrenheit\n\nUsage:\n+fk 77 (Returns 298.15K)',
                      brief='°F > K',
                      aliases=['ftok'])
    async def fk(self, ctx, fahrenheit):
        fahrenheit = ('-' if fahrenheit[0] == '-' else '') + re.sub('[^0-9.]', '', fahrenheit)
        ck_value = round((float(fahrenheit) + 459.67) * 5 / 9, 2)
        await ctx.send(f'{round(float(fahrenheit), 2)}°F = {ck_value}K')

    @commands.command(description='Convert temperature from °Celsius to °Fahrenheit\n\nUsage:\n+cf 25 (Returns 77.0°F)',
                      brief='°C > °F',
                      aliases=['ctof'])
    async def cf(self, ctx, celsius):
        celsius = ('-' if celsius[0] == '-' else '') + re.sub('[^0-9.]', '', celsius)
        cf_value = round(float(celsius) * 1.8 + 32, 2)
        await ctx.send(f'{round(float(celsius), 2)}°C = {cf_value}°F')

    @commands.command(description='Convert temperature from °Fahrenheit to °Celsius\n\nUsage:\n+fc 77 (Returns 25.0°C)',
                      brief='°F > °C',
                      aliases=['ftoc'])
    async def fc(self, ctx, fahrenheit):
        fahrenheit = ('-' if fahrenheit[0] == '-' else '') + re.sub('[^0-9.]', '', fahrenheit)
        fc_value = round((float(fahrenheit) - 32) / 1.8, 2)
        await ctx.send(f'{round(float(fahrenheit), 2)}°F = {fc_value}°C')

    @commands.command(description='Convert from Centimeters to Inches\n\nUsage:\n+cmin 25.40 (Returns 10.0 inch)',
                      brief='cm > in',
                      aliases=['cmtoin'])
    async def cmin(self, ctx, centimeters):
        centimeters = ('-' if centimeters[0] == '-' else '') + re.sub('[^0-9.]', '', centimeters)
        cminch_value = round(float(centimeters) * 0.393701, 2)
        await ctx.send(f'{round(float(centimeters), 2)} cm  = {cminch_value} inch')

    @commands.command(description='Convert from Inches to Centimeters\n\nUsage:\n+incm 10 (Returns 25.4 cm)',
                      brief='in > cm',
                      aliases=['intocm'])
    async def incm(self, ctx, inches):
        inches = ('-' if inches[0] == '-' else '') + re.sub('[^0-9.]', '', inches)
        inchcm_value = round(float(inches) * 2.54, 2)
        await ctx.send(f'{round(float(inches), 2)} inch = {inchcm_value} cm')

    @commands.command(description='Convert from Centimeters to Feet\n\nUsage:\n+cmft 91.44 (Returns 3 ft)',
                      brief='cm > ft',
                      aliases=['cmtoft'])
    async def cmft(self, ctx, centimeters):
        centimeters = ('-' if centimeters[0] == '-' else '') + re.sub('[^0-9.]', '', centimeters)
        cmft_value = round(float(centimeters) / 30.48, 2)
        await ctx.send(f'{round(float(centimeters), 2)} cm = {cmft_value} ft')

    @commands.command(description='Convert from Feet to Centimeters\n\nUsage:\n+cmft 3 (Returns 91.44 cm)',
                      brief='ft > cm',
                      aliases=['fttocm'])
    async def ftcm(self, ctx, feet):
        feet = ('-' if feet[0] == '-' else '') + re.sub('[^0-9.]', '', feet)
        ftcm_value = round(float(feet) * 30.48, 2)
        await ctx.send(f'{round(float(feet), 2)} ft = {ftcm_value} cm')

    @commands.command(description='Convert from Feet to Meters\n\nUsage:\n+ftm 3.28 (Returns 1.0 m)',
                      brief='ft > m',
                      aliases=['fttom'])
    async def ftm(self, ctx, feet):
        feet = ('-' if feet[0] == '-' else '') + re.sub('[^0-9.]', '', feet)
        ftm_value = round(float(feet) * 0.3048, 2)
        await ctx.send(f'{round(float(feet), 2)} ft = {ftm_value} m')

    @commands.command(description='Convert from Meters to Feet\n\nUsage:\n+mft 1 (Returns 3.28 ft)',
                      brief='m > ft',
                      aliases=['mtoft'])
    async def mft(self, ctx, meters):
        meters = ('-' if meters[0] == '-' else '') + re.sub('[^0-9.]', '', meters)
        mft_value = round(float(meters) / 0.3048, 2)
        await ctx.send(f'{round(float(meters), 2)} m = {mft_value} ft')

    class FtinmConv(commands.Converter):
        def __init__(self, ft, inch):
            self.feet = float(ft)
            self.inches = float(inch)

        async def convert(self, ctx, argument):
            argument1, argument2 = argument, 0
            if "\'" in argument or '\"' in argument or "ft" in argument.lower() or "in" in argument.lower():
                if "\'" in argument and '\"' in argument:
                    argument1 = argument.split("\'")[0]
                    argument2 = argument.split("\'")[1].split('\"')[0]
                elif "\'" in argument and '\"' not in argument:
                    argument1, argument2 = argument.split("\'")
                elif '\"' in argument and "\'" not in argument:
                    argument1, argument2 = argument.split('\"')
                if "ft" in argument1.lower():
                    argument1, argument2 = argument1.lower().split("ft")
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

    @commands.command(description='Convert from mixed US Customary length units to Meters\n(no space between number '
                                  'and unit, if unit is given)\n\nUsage (spaces between feet and inches optional):\n'
                                  '+ftinm 6ft 2in | +ftinm 6ft2in\nOr:\n+ftinm 6\' 2\" | +ftinm 6\'2\"\nOr:\n+ftinm 6 2'
                                  '\n(Return 1.88m)\n',
                      brief='ft in > m',
                      aliases=['ftintom'])
    async def ftinm(self, ctx, *, feet_inches: FtinmConv(0, 0)):
        # send default values so still stored old ones don't get delivered
        if isinstance(feet_inches.feet, float) and isinstance(feet_inches.inches, float):
            await ctx.send(f'{round(float(feet_inches.feet), 2)} ft {round(float(feet_inches.inches))} in = '
                           f'{round((feet_inches.feet * 0.3048) + (feet_inches.inches * 0.0254), 2)} m')

    @commands.command(description='Convert from Meters to mixed US Customary length units\n\nUsage:\n+mftin 1.88m \n '
                                  'Or:\n+mftin 1.88 (Return 6 ft 2.0 in)',
                      brief='m > ft in',
                      aliases=['mtoftin'])
    async def mftin(self, ctx, meters):
        meters = ('-' if meters[0] == '-' else '') + re.sub('[^0-9.]', '', meters)
        feetfrommeters = divmod(float(meters), 0.3048)
        inchesfrommeters = feetfrommeters[1] / 0.0254
        await ctx.send(f'{round(float(meters), 2)} m = {int(feetfrommeters[0])} ft {round(inchesfrommeters, 1)} in')

    @commands.command(name='kmmi',
                      description='Convert from Kilometers to Miles\n\nUsage:\n+kmmi 128.75 (Returns 80.0 mi)',
                      brief='km > mi',
                      aliases=['kitomi', 'kmm'])
    async def kmmi(self, ctx, kilometers):
        kilometers = ('-' if kilometers[0] == '-' else '') + re.sub('[^0-9.]', '', kilometers)
        kmmi_value = round(float(kilometers) * 0.621371, 2)
        await ctx.send(f'{round(float(kilometers), 2)} km = {kmmi_value} mi')

    @commands.command(description='Convert Miles to Kilometers\n\nUsage:\n+mikm 80 (Returns 128.75 km)',
                      brief='mi > km',
                      aliases=['mitokm', 'mkm'])
    async def mikm(self, ctx, miles):
        miles = ('-' if miles[0] == '-' else '') + re.sub('[^0-9.]', '', miles)
        mikm_value = round(float(miles) / 0.621371, 2)
        await ctx.send(f'{round(float(miles))} mi = {mikm_value} km')

    @commands.command(description='Convert from Kilograms to Pounds\n\nUsage:\n+kglbs 70 (Returns 154.32 lbs)',
                      brief='kg > lbs',
                      aliases=['kgtolbs'])
    async def kglbs(self, ctx, kilograms):
        kilograms = ('-' if kilograms[0] == '-' else '') + re.sub('[^0-9.]', '', kilograms)
        kglbs_value = round(float(kilograms) / 0.45359237, 2)
        await ctx.send(f'{round(float(kilograms), 2)} kg = {kglbs_value} lbs')

    @commands.command(description='Convert from Pounds to Kilograms\n\nUsage:\n+lbskg 154.32 (Returns 70.0 kg)',
                      brief='lbs   > kg',
                      aliases=['lbstokg'])
    async def lbskg(self, ctx, pounds):
        pounds = ('-' if pounds[0] == '-' else '') + re.sub('[^0-9.]', '', pounds)
        lbskg_value = round(float(pounds) * 0.45359237, 2)
        await ctx.send(f'{round(float(pounds), 2)} lbs = {lbskg_value} kg')

    @commands.command(description='Convert from US Fluid Ounces to Milliliters\n\nUsage:\n+flozml 10 '
                                  '(Returns 395.74 ml)',
                      brief='fl oz > ml',
                      aliases=['floztoml'])
    async def flozml(self, ctx, floz):
        floz = ('-' if floz[0] == '-' else '') + re.sub('[^0-9.]', '', floz)
        ml_value = round(float(floz) * 29.5735, 2)
        await ctx.send(f'{round(float(floz), 2)} fl oz = {ml_value} ml')

    @commands.command(description='Convert from Milliliters to US Fluid Ounces\n\nUsage:\n+mlfloz 395.74 '
                                  '(Returns 10.0 fl oz)',
                      brief='ml > fl oz',
                      aliases=['mltofloz'])
    async def mlfloz(self, ctx, milliliters):
        milliliters = ('-' if milliliters[0] == '-' else '') + re.sub('[^0-9.]', '', milliliters)
        floz_value = round(float(milliliters) * 0.033814, 2)
        await ctx.send(f'{round(float(milliliters))} ml = {floz_value} fl oz')

    @commands.command(description='Convert from US Gallons to Liters\n\nUsage:\n+gall 26.42 (Returns 100 l)',
                      brief='gal > l',
                      aliases=['galtol'])
    async def gall(self, ctx, gallons):
        gallons = ('-' if gallons[0] == '-' else '') + re.sub('[^0-9.]', '', gallons)
        gal_value = round(float(gallons) * 3.785411784, 2)
        await ctx.send(f'{round(float(gallons))} gal (US) = {gal_value} l')

    @commands.command(description='Convert from Liters to US Gallons\n\nUsage:\n+lgal 100 (Returns 26.42 gal (US))',
                      brief='l > gal',
                      aliases=['ltogal'])
    async def lgal(self, ctx, liters):
        liters = ('-' if liters[0] == '-' else '') + re.sub('[^0-9.]', '', liters)
        l_value = round(float(liters) * 0.2641720524, 2)
        await ctx.send(f'{round(float(liters))} l = {l_value} gal (US)')


def setup(bot):
    bot.add_cog(Conversion(bot))
