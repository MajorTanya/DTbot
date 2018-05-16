from discord.ext import commands

class VC():
    def __init__(self, bot):
        self.bot = bot

#    Commands go here, pay attention to the indentation, and don't forget to make every command take the 'self' argument (see example)
#    @commands.command(description="Try and see",
#                      brief="Try and see")
#    async def bitcoin(self):
#        await self.bot.say('Have a bitcoin.')
#    As you can see, the normally empty bitcoin now take a 'self' argument.
#    Every command in a submodule needs this, and the "await bot.say(xyz)" needs to be converted to a "await self.bot.say(xyz)
#    Also, if a command takes more than 0 arguments, it looks like this:
#
#    @commands.command(pass_context=True,
#                      description="Bitch slaps someone",
#                      brief="Bitch slaps someone",
#                      aliases=['Bitchslap'])
#    async def bitchslap(self, ctx, user: discord.Member):
#        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got a bitch slap.".format(user.mention) + "\n\n[Image link](https://i.imgur.com/bTGigCv.gif)")
#        embed.set_image(url="https://i.imgur.com/bTGigCv.gif")
#        await self.bot.say(embed=embed)
#    Here you can see that bitchslap now takes three arguments (when it was in the main script, it only took two).
#    'self' tells it that it's working in a submodule, 'ctx' carries the context of the message like channel, author of message, mentions, etc. pp., and 'user' (which has to be a discord.Member element) which is of course the mentioned user
#    Additionally, the "await bot.say(embed=embed)" of course needs to be changed into "await self.bot.say(embed=embed)
#
#    For the bot, this module would be loaded with a "+load vc"

def setup(bot):
    bot.add_cog(VC(bot))
