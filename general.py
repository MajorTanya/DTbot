import discord
from discord.ext import commands

class General:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def repeat(self, times : int, content='repeating...'):
        """Repeats a message multiple times."""
        for i in range(times):
            await self.bot.say(content)


    @commands.command(pass_context=True,
                      description="Shows details on user, such as Name, Join Date, or Highest Role",
                      brief="Get info on a user",
                      aliases=['uinfo'])
    async def userinfo(self, ctx, user: discord.Member):
    
        embed = discord.Embed(title="{}'s info".format(user.name), description='Here is what I could find:', color=ctx.message.author.color)
        embed.add_field(name='Nickname', value='{}'.format(user.display_name))
        embed.add_field(name='ID', value='{}'.format(user.id), inline=True)
        embed.add_field(name='Status', value='{}'.format(user.status), inline=True)
        embed.add_field(name='Highest Role', value='<@&{}>'.format(user.top_role.id), inline=True)
        embed.add_field(name='Joined at', value='{:%d. %h \'%y at %H:%M}'.format(user.joined_at), inline=True)
        embed.add_field(name='Created at', value='{:%d. %h \'%y at %H:%M}'.format(user.created_at), inline=True)
        embed.add_field(name='Discriminator', value='{}'.format(user.discriminator), inline=True)
        embed.add_field(name='Playing', value='{}'.format(user.game))
        embed.set_footer(text="{}'s Info".format(user.name), icon_url='{}'.format(user.avatar_url))
        embed.set_thumbnail(url=user.avatar_url)

        await self.bot.say(embed=embed)


    @commands.command(description="Info about me, Dbot. Please take a look.",
                      brief="Info about me")
    async def info(self):
        embed = discord.Embed(title="Dbot's info", description="Hello, I'm <@427902715138408458>, a bot created by <@327763028701347840> for one server only.\nIf you have any requests or questions, please primarily ask <@274684924324347904>.\nYou can find a version of the code minus the server specific stuff here: https://github.com/angelgggg/Pbot\nThank you and have a good day.", colour=discord.Colour(0x5e51a8))
        embed.set_footer(text="DTbot v. " + dbot_version)
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Pong",
                      brief="Pong")
    @commands.has_any_role("The Dark Lords", "Administrator", "Dbot Dev", "Tanya")
    @commands.cooldown(3, 30, commands.BucketType.server)
    async def ping(self, ctx):
        time_then = time.monotonic()
        pinger = await self.bot.say('__*`Pinging...`*__')
        ping = '%.2f' % (1000*(time.monotonic()-time_then))
        await self.bot.edit_message(pinger, ':ping_pong: \n **Pong!** __**`' + ping + 'ms`**__')


def setup(bot):
    bot.add_cog(General(bot))
