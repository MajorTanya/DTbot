import datetime
from math import ceil

import nextcord
import requests
from nextcord.ext import commands
from nextcord.ext.commands import cooldown

from DTbot import DTbot, config, startup_time
from database_management import dbcallprocedure
from dev import dtbot_version, last_updated
from error_handler import send_cmd_help
from launcher import default_prefix
from linklist import changelog_link
from util.PaginatorSession import PaginatorSession

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

    def __init__(self, bot: DTbot):
        self.bot = bot

    @commands.command(description="Displays a user's avatar. Defaults to command user's avatar when "
                                  "no user is mentioned.",
                      brief="Show a user's avatar")
    @commands.bot_has_permissions(embed_links=True)
    async def avatar(self, ctx: commands.Context, *, user: nextcord.Member = None):
        if user:
            avatar_url = user.avatar.url
            embed = nextcord.Embed(colour=self.bot.dtbot_colour,
                                   description=f"{user.mention}'s avatar\n\n[Avatar Link]({avatar_url})")
            embed.set_image(url=avatar_url)
        else:
            avatar_url = ctx.author.avatar.url
            embed = nextcord.Embed(colour=self.bot.dtbot_colour,
                                   description=f"{ctx.author.mention}'s avatar\n\n[Avatar Link]({avatar_url})")
            embed.set_image(url=avatar_url)
        await ctx.send(embed=embed)

    @commands.command(description='Current DTbot announcements',
                      brief='DTbot announcements')
    async def announcements(self, ctx: commands.Context):
        embed = nextcord.Embed(colour=self.bot.dtbot_colour, title='Announcement',
                               url=config.get('About', 'ANNOUNCEMENT LINK'),
                               description=config.get('About', 'ANNOUNCEMENT MSG'))
        await ctx.send(embed=embed)

    @commands.command(description="Get an overview over the recentmost update of DTbot",
                      brief="Recent updates to DTbot")
    @commands.bot_has_permissions(embed_links=True)
    async def changelog(self, ctx: commands.Context):
        latest_commit = requests.get("https://api.github.com/repos/MajorTanya/DTbot/commits").json()[0]
        embed = nextcord.Embed(colour=self.bot.dtbot_colour,
                               description=f'__Recent changes to DTbot:__\nNewest version: {dtbot_version} '
                                           f'({last_updated})')
        embed.set_image(url=changelog_link)
        embed.add_field(name=f"Latest Commit", value=f"[`{latest_commit['sha'][:7]}`]({latest_commit['html_url']})\t"
                                                     f"{latest_commit['commit']['message']}")
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
    async def changeserverprefix(self, ctx: commands.Context, *newprefix: str):
        newprefix = ''.join(newprefix)
        if newprefix == '':
            try:
                await send_cmd_help(self.bot, ctx, "")
            except nextcord.Forbidden:  # not allowed to send embeds
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
    async def info(self, ctx: commands.Context):
        now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        uptime = now_dt - startup_time
        embed = nextcord.Embed(title=f"{self.bot.user.name}'s info",
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
    async def ping(self, ctx: commands.Context):
        try:
            embed = nextcord.Embed(colour=self.bot.dtbot_colour,
                                   description=f':ping_pong:\n**Pong!** __**`{self.bot.latency * 1000:.2f} ms`**__')
            await ctx.send(embed=embed)
        except nextcord.Forbidden:  # not allowed to send embeds
            await ctx.send(f':ping_pong:\n**Pong!** __**`{self.bot.latency * 1000:.2f} ms`**__')

    @commands.command(description=f"Request a command to be added to DTbot. Functionality can be described in detail."
                                  f"\nPlease keep it reasonably concise.\nRestricted to 2 uses every 24 hours.\n\n"
                                  f"Usage:\n{default_prefix}request burn Burn someone at the stake for being a heretic.",
                      brief="Request a new command (2x/24hr)",
                      aliases=['req'])
    @cooldown(2, 86400, commands.BucketType.user)
    async def request(self, ctx: commands.Context, command: str, *functionality: str):
        reqhall = self.bot.get_channel(REQHALL)
        dev_dm = self.bot.get_user(main_dev_id)
        embed = nextcord.Embed(title=f"New request by {ctx.author.name}",
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
    async def resetserverprefix(self, ctx: commands.Context):
        dbcallprocedure('ChangeServerPrefix', params=(ctx.message.guild.id, '+'))
        await ctx.send(f'Prefix for {ctx.guild} reset to `+`.')

    @commands.command(description="Gives the bot's uptime since the last restart.",
                      brief="DTbot's uptime")
    async def uptime(self, ctx: commands.Context):
        now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        uptime = now_dt - startup_time
        await ctx.send(f"{self.bot.user.name}'s uptime is: `{uptime}`")

    @commands.command(description="Shows details on user, such as Name, Join Date, or Highest Role",
                      brief="Get info on a user",
                      aliases=['uinfo'])
    @commands.bot_has_permissions(embed_links=True)
    async def userinfo(self, ctx: commands.Context, user: nextcord.Member):
        join_ts = int(user.joined_at.timestamp())
        created_ts = int(user.created_at.timestamp())
        embed = nextcord.Embed(title=f"{user}'s info",
                               description='Here is what I could find:', colour=ctx.author.colour)
        embed.add_field(name='Nickname', value=f'{user.display_name}')
        embed.add_field(name='ID', value=f'{user.id}', inline=True)
        embed.add_field(name='Status', value=f'{user.status}', inline=True)
        embed.add_field(name='Highest Role', value=f'<@&{user.top_role.id}>', inline=True)
        embed.add_field(name='Joined at', value=f'<t:{join_ts}:D> - <t:{join_ts}:T>', inline=True)
        embed.add_field(name='Created at', value=f'<t:{created_ts}:D> - <t:{created_ts}:T>', inline=True)
        embed.set_footer(text=f"{user.name}'s Info", icon_url=f'{user.avatar.url}')
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(description='Shows how many users have a particular role (case sensitive), and lists them.\n\n'
                                  'Limited to 10 pages of output, which hold roughly 900 members.',
                      brief='List users with this role')
    async def whohas(self, ctx: commands.Context, *, role: nextcord.Role):
        role = nextcord.utils.get(ctx.guild.roles, name=role.name)
        embed_desc_max_size = 2048  # max char count in embed.description of a nextcord.Embed
        pages, role_members = [], []
        for member in role.members:
            role_members.append(member.mention)
        # get character count in role_members, divide by 2048 (max size of embed.description) = pages needed
        page_count = ceil(len(str(role_members).strip("[]").replace("'", "")) / embed_desc_max_size)
        for i in range(0, min(page_count, 10)):  # we allow 10 pages max
            page_members = f"{len(role.members)} members with {role.mention}\n\n" if i == 0 else ""
            role_members.reverse()  # so we can pop() "from the front"
            try:
                while (len(page_members) + len(role_members[0])) < embed_desc_max_size:
                    page_members += f'{role_members.pop()}, '
            except IndexError:  # list is empty now, ignore and continue
                pass
            page_members = page_members.rstrip(", ")
            pages.append(nextcord.Embed(colour=role.colour,
                                        title=f'{len(role.members)} users with {role.name} - Page {i + 1}/{page_count}',
                                        description=page_members))
        p_sess = PaginatorSession(ctx, pages=pages)
        await p_sess.run()

    @commands.command(description="Shows a user's XP points. If no user is mentioned, it will default to command user.",
                      brief="Check user's XP")
    async def xp(self, ctx: commands.Context, user: nextcord.Member = None):
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


def setup(bot: DTbot):
    bot.add_cog(General(bot))
