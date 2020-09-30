import datetime

import discord
from discord.ext import commands
from discord.ext.commands import cooldown

from DTbot import config, startup_time
from database_management import dbcallprocedure
from dev import dtbot_version
from error_handler import send_cmd_help
from launcher import default_prefixes
from linklist import changelog_link

last_updated = config.get('Info', 'last_updated')
main_dev_id = config.getint('Developers', 'main dev id')
main_dev = config.get('Developers', 'main')
secondary_dev = config.get('Developers', 'secondary')
dtbot_devs = f'{main_dev}\n{secondary_dev}'
INVITE = config.get('General', 'INVITE')
PERMSEXPL = config.get('General', 'PERMSEXPL')
REQHALL = config.getint('General', 'REQHALL')

AVATAR_ARTIST = config.get('About', 'AVATAR ARTIST')
GH_LINK = config.get('About', 'GH LINK')
SUPPORT_LINK = config.get('About', 'SUPPORT LINK')
TWITTER_LINK = config.get('About', 'TWITTER LINK')


class General(commands.Cog):
    """General utility commands, like user info and uptime, among others"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Displays a user's avatar. Defaults to command user's avatar when "
                                  "no user is mentioned.",
                      brief="Show a user's avatar")
    @commands.bot_has_permissions(embed_links=True)
    async def avatar(self, ctx, *, user: discord.Member = None):
        if user:
            embed = discord.Embed(colour=self.bot.dtbot_colour, description=f"{user.mention}'s avatar")
            embed.set_image(url=user.avatar_url)
        else:
            embed = discord.Embed(colour=self.bot.dtbot_colour, description=f"{ctx.author.mention}'s avatar")
            embed.set_image(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(description="Get an overview over the recentmost update of DTbot",
                      brief="Recent updates to DTbot")
    @commands.bot_has_permissions(embed_links=True)
    async def changelog(self, ctx):
        embed = discord.Embed(colour=self.bot.dtbot_colour,
                              description=f'__Recent changes to DTbot:__\nNewest version: {dtbot_version} '
                                          f'({last_updated})')
        embed.set_image(url=changelog_link)
        embed.set_footer(text="Check out our customizable prefixes with '@DTbot help changeserverprefix'!")
        await ctx.send(embed=embed)

    @commands.command(description="Manually changes the prefix a server wants to use for DTbot."
                                  "\nNeeds to be 1-3 characters in length.\nUsing @DTbot (command) will always work."
                                  " (e.g. `@DTbot resetprefix`)\nRequires the user to have the **manage_guild** "
                                  "permission.\nUsage:\n\n@DTbot changeprefix ! (DTbot now only works with e.g. `!help`"
                                  ". `+help` won't work anymore. `@DTbot help` will always work.)\nLonger "
                                  "prefix:\n`@DTbot changeprefix dt!` (`dt!help`)",
                      brief="Change DTbot's prefix in this server",
                      aliases=['csp', 'changeprefix', 'prefix'])
    @commands.has_guild_permissions(manage_guild=True)
    async def changeserverprefix(self, ctx, *newprefix: str):
        newprefix = ''.join(newprefix)
        if newprefix == '':
            try:
                await send_cmd_help(self.bot, ctx, "")
            except discord.Forbidden:  # not allowed to send embeds
                await send_cmd_help(self.bot, ctx, "", plain=True)
        elif len(newprefix) <= 3:
            dbcallprocedure('ChangeServerPrefix', params=(ctx.message.guild.id, newprefix))
            await ctx.send(f"Prefix for {ctx.guild} changed to `{newprefix}`.\nYou can always reach DTbot by "
                           f"mentioning it. You can also reset the prefix to the default by using "
                           f"`@DTbot resetserverprefix` if you forget your server's prefix.")
        else:
            await ctx.send("Invalid prefix length (max. 3 characters)")

    @commands.command(description="Info about me, DTbot. Please take a look.",
                      brief="Info about me")
    @commands.bot_has_permissions(embed_links=True)
    async def info(self, ctx):
        now = datetime.datetime.utcnow()
        tdelta = now - startup_time
        uptime = tdelta - datetime.timedelta(microseconds=tdelta.microseconds)
        embed = discord.Embed(title=f"{self.bot.user.name}'s info",
                              description=f"Hello, I'm {self.bot.user.name}, a multipurpose bot for your Discord "
                                          f"server.\n\nIf you have any command requests, use the `request` "
                                          f"command.\n\nThank you and have a good day.\n\n[__**"
                                          f"{self.bot.user.name} Support Server**__]({SUPPORT_LINK})",
                              colour=self.bot.dtbot_colour)
        embed.add_field(name="Authors", value=dtbot_devs)
        embed.add_field(name="GitHub repository", value=f"Find me [here]({GH_LINK})")
        embed.add_field(name="Twitter", value=f"[Tweet @DTbotDiscord]({TWITTER_LINK})", inline=True)
        embed.add_field(name="Stats", value=f"In {len(self.bot.guilds)} servers with {len(self.bot.users)} members")
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name="Invite me", value=f"[Invite me]({INVITE}) to your server too.\n[Explanation]({PERMSEXPL})"
                                                f" for DTbot's permissions")
        embed.add_field(name="Avatar by", value=AVATAR_ARTIST, inline=False)
        embed.set_footer(text=f"DTbot v. {dtbot_version}")
        await ctx.send(embed=embed)

    @commands.command(description="Show the latency between DTbot and the Discord web servers",
                      brief="Pong")
    @cooldown(3, 30, commands.BucketType.guild)
    async def ping(self, ctx):
        try:
            embed = discord.Embed(colour=self.bot.dtbot_colour,
                                  description=f':ping_pong:\n**Pong!** __**`{self.bot.latency * 1000:.2f} ms`**__')
            await ctx.send(embed=embed)
        except discord.Forbidden:  # not allowed to send embeds
            await ctx.send(f':ping_pong:\n**Pong!** __**`{self.bot.latency * 1000:.2f} ms`**__')

    @commands.command(description=f"Request a command to be added to DTbot. Functionality can be described in detail."
                                  f"\nPlease keep it reasonably concise.\nRestricted to 2 uses every 24 hours.\n\n"
                                  f"Usage:\n{default_prefixes[0]}request burn Burn someone at the stake for being a heretic.",
                      brief="Request a new command (2x/24hr)",
                      aliases=['req'])
    @cooldown(2, 86400, commands.BucketType.user)
    async def request(self, ctx, command: str, *functionality: str):
        reqhall = self.bot.get_channel(REQHALL)
        dev_dm = self.bot.get_user(main_dev_id)
        embed = discord.Embed(title=f"New request by {ctx.author.name}",
                              description=f'{ctx.author} (ID: {ctx.author.id}) requested the following command:',
                              colour=ctx.author.colour)
        embed.add_field(name='Suggested command name', value=f'**{command}**')
        embed.add_field(name='Suggested functionality', value=f'*{" ".join(functionality)}*', inline=False)
        await reqhall.send('New command request!', embed=embed)
        await dev_dm.send('New command request!', embed=embed)
        await ctx.send(f'New command request was sent to the developers, {ctx.author.mention}.')

    @commands.command(description="Manually resets the prefix a server wants to use for DTbot to the default."
                                  "\nRequires the **manage_guild** permission.",
                      brief="Reset DTbot's prefix to `+`",
                      aliases=['rsp', 'resetprefix'])
    @commands.has_guild_permissions(manage_guild=True)
    async def resetserverprefix(self, ctx):
        dbcallprocedure('ChangeServerPrefix', params=(ctx.message.guild.id, '+'))
        await ctx.send(f'Prefix for {ctx.guild} reset to `+`.')

    @commands.command(description="Gives the bot's uptime since the last restart.",
                      brief="DTbot's uptime")
    async def uptime(self, ctx):
        now = datetime.datetime.utcnow()
        tdelta = now - startup_time
        uptime = tdelta - datetime.timedelta(microseconds=tdelta.microseconds)
        await ctx.send(f"{self.bot.user.name}'s uptime is: `{uptime}`")

    @commands.command(description="Shows details on user, such as Name, Join Date, or Highest Role",
                      brief="Get info on a user",
                      aliases=['uinfo'])
    @commands.bot_has_permissions(embed_links=True)
    async def userinfo(self, ctx, user: discord.Member):
        embed = discord.Embed(title=f"{user}'s info",
                              description='Here is what I could find:', colour=ctx.author.colour)
        embed.add_field(name='Nickname', value=f'{user.display_name}')
        embed.add_field(name='ID', value=f'{user.id}', inline=True)
        embed.add_field(name='Status', value=f'{user.status}', inline=True)
        embed.add_field(name='Highest Role', value=f'<@&{user.top_role.id}>', inline=True)
        embed.add_field(name='Joined at', value=f'{user.joined_at:%d. %h \'%y at %H:%M}', inline=True)
        embed.add_field(name='Created at', value=f'{user.created_at:%d. %h \'%y at %H:%M}', inline=True)
        all_activities = ""
        for activity in user.activities:
            act_type_name = str(activity.type)[13:].title()  # remove the 'ActivityType.' start & make it Title Case
            act_type_name += ' to:' if activity.type == discord.ActivityType.listening else ':'  # make 'Listening to:'
            # ignore 'Custom:' and underline the Activity (e.g. __Listening to:__) for ease of reading
            act_type_name = '' if activity.type == discord.ActivityType.custom else f'__{act_type_name}__ '
            if activity.type == discord.ActivityType.listening:
                song_dict = activity.to_dict()  # __Listening to:__ "Title" by _Artist_ on "Album"
                act_details = f'"{song_dict["details"]}" by *{song_dict["state"]}* on ' \
                              f'"{song_dict["assets"]["large_text"]}"'
            elif activity.type == discord.ActivityType.streaming:  # __Streaming:__ (Title (Category) on Platform)[Link]
                act_details = f'{activity.name} ({activity.game}) on {activity.platform}'
                act_details = f'[{act_details}]({activity.url})'  # Title through Platform is a link to the stream
            else:
                act_details = activity.name  # either Playing or Watching
            all_activities += f'{act_type_name}{act_details}\n'  # new line for each simultaneous Activity
        embed.add_field(name='Activity', value=all_activities.strip('\n'))
        embed.set_footer(text=f"{user.name}'s Info", icon_url=f'{user.avatar_url}')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(description='Shows a list of all users with a particular role (case sensitive)',
                      brief='List all users with this role')
    @commands.bot_has_permissions(embed_links=True)
    async def whohas(self, ctx, *, role: discord.Role):
        role = discord.utils.get(ctx.guild.roles, name=role.name)
        role_members = list()
        for member in role.members:
            role_members.append(member.mention)
        role_members = str(role_members).strip("[]").replace("'", "")
        embed = discord.Embed(colour=role.colour, title=f'Users with the role {role.name}',
                              description=f"{len(role.members)} members with {role.mention}\n\n{role_members}")
        await ctx.send(embed=embed)

    @commands.command(description="Shows a user's XP points. If no user is mentioned, it will default to command user.",
                      brief="Check user's XP")
    async def xp(self, ctx, user: discord.Member = None):
        if user:
            if user.bot:
                await ctx.send("Bots don't get XP. :robot:")
                return
            user_id = user.id
            user_name = user.display_name
        else:
            user_id = ctx.author.id
            user_name = ctx.author.display_name
        xp = dbcallprocedure('GetUserXp', returns=True, params=(user_id, '@res'))
        if xp > 0:
            await ctx.send(f"**{user_name}** has `{xp}` XP.")
        else:
            await ctx.send("User hasn't talked yet.")


def setup(bot):
    bot.add_cog(General(bot))
