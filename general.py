import datetime
import time

import discord
from discord.ext import commands

from linklist import changelog_link
from DTbot import command_prefix, dbot_version, last_updated, startup_time


class General:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="Gives the bot's uptime since the last restart.",
                      brief="DTbot's uptime")
    async def uptime(self):
        now = datetime.datetime.utcnow()
        tdelta = now - startup_time
        tdelta = tdelta - datetime.timedelta(microseconds=tdelta.microseconds)
        await self.bot.say(self.bot.user.name + "'s uptime is: `" + str(tdelta) + "`")


    @commands.command(description="Get an overview over the recentmost update of DTbot",
                      brief="Recent updates to DTbot")
    async def changelog(self):
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description='__Recent changes to DTbot:__\nNewest version: ' + dbot_version + " (" + last_updated + ")")
        embed.set_image(url=changelog_link)
        await self.bot.say(embed=embed)


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
        now = datetime.datetime.utcnow()
        tdelta = now - startup_time
        tdelta = tdelta - datetime.timedelta(microseconds=tdelta.microseconds)
        server_amount = len(self.bot.servers)

        total_users = 0
        for server in self.bot.servers:
            for member in server.members:
                total_users += 1
        embed = discord.Embed(title=self.bot.user.name + "'s info", description="Hello, I'm " + self.bot.user.name + ", a multipurpose bot for your Discord server.\n\nIf you have any command requests, use +request (do +help request first).\n\nThank you and have a good day.\n\n[__**" + self.bot.user.name + " Support Server**__](https://discord.gg/kSPMd2v)", colour=discord.Colour(0x5e51a8))
        embed.add_field(name="Authors", value="Major Tanya#7318 aka Tanya\nangelgggg#7374 aka Demon")
        embed.add_field(name="GitHub repository", value="Find me [here](https://github.com/MajorTanya/DTbot)")
        embed.add_field(name="Twitter", value="[Tweet @DTbotDiscord](https://twitter.com/DTbotDiscord)", inline=True)
        embed.add_field(name="Stats", value="In {} servers with ".format(server_amount) + str(total_users) + " members")
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Uptime", value=tdelta)
        embed.add_field(name="Avatar by", value="[Kokoyabubu](http://kokoyabubu.tumblr.com/)", inline=False)
        embed.set_footer(text="DTbot v. " + dbot_version)
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Pong",
                      brief="Pong")
    @commands.has_any_role("The Dark Lords", "Administrator", "Dbot Dev", "DTbot Dev", "Tanya")
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
    async def request(self, ctx, command: str, *functionality: str):
        reqhall = self.bot.get_channel('477250023713800193')
        tanyadm = discord.utils.get(self.bot.get_all_members(), id='274684924324347904')
        embed = discord.Embed(title="New request by {}".format(ctx.message.author.name), description='{} requested the following command:'.format(ctx.message.author.mention), color=ctx.message.author.color)
        embed.add_field(name='Suggested command name', value='**+' + command + '**')
        embed.add_field(name='Suggested functionality', value='*' + ' '.join(functionality) + '*', inline=False)
        await self.bot.send_message(reqhall, 'New command request!', embed=embed)
        await self.bot.send_message(tanyadm, 'New command request!', embed=embed)
        await self.bot.say("New command request was sent to the developers, {}.".format(ctx.message.author.mention))


    @commands.command(hidden=True)
    async def DTbot(self):
        await self.bot.say('You found a secret. Good job')
        await self.bot.say('This will eventually be used for something')
        # D:TANYA DO NOT DELETE THIS
        # D:its for something i wanna do in the future and im just making sure it doesnt get used for a diferent command
        # T:okay


def setup(bot):
    bot.add_cog(General(bot))
