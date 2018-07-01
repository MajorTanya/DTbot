import discord
import time
from discord.ext import commands
from DTbot import dbot_version
from DTbot import command_prefix

class General:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot


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
        embed = discord.Embed(title="Dbot's info", description="Hello, I'm <@427902715138408458>, a bot created by <@327763028701347840> for one server only.\nIf you have any command requests, use +request (do +help request first).\nFor questions, please primarily ask <@274684924324347904>.\nYou can find a version of the code minus the server specific stuff here: https://github.com/angelgggg/Pbot\nThank you and have a good day.", colour=discord.Colour(0x5e51a8))
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


    @commands.command(pass_context=True,
                      description="Request a command to be added to DTbot. Functionality can be described in detail.\nPlease keep it reasonably concise.\nRestricted to 2 uses every 24 hours (reset is NOT at a set time of day but 24 hours after the command is used).\n\nExample use:\n" + command_prefix + "request burn Burn someone at the stake for being a heretic.",
                      brief="Request a new command (2x/24hr)",
                      aliases=['req'])
    @commands.cooldown(2, 86400, commands.BucketType.user)
    async def request(self, ctx, command : str, *functionality : str):
        user = discord.utils.get(self.bot.get_all_members(), id='274684924324347904')
        embed = discord.Embed(title="New request by {}".format(ctx.message.author.name), description='{} requested the following command:'.format(ctx.message.author.mention), color=ctx.message.author.color)
        embed.add_field(name='Suggested command name', value='**+' + command + '**')
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='Suggested functionality', value='*' + ' '.join(functionality) + '*')
        await self.bot.send_message(user, 'New command request!', embed=embed)
        await self.bot.say("New command request was sent to the developers, {}.".format(ctx.message.author.mention))


    @commands.command(hidden=True,
                      aliases=['dtbot'])
    async def DTbot(self):
        await self.bot.say('You found a secret. Good job')
        await self.bot.say('this will eventually be used for something')
        # D:TANYA DO NOT DELETE THIS
        # D:its for something i wanna do in the future and im just making sure it doesnt get used for a diferent command
        # T:okay


def setup(bot):
    bot.add_cog(General(bot))
