import datetime
from math import ceil

import discord
import requests
from discord.ext import commands
from discord.ext.commands import cooldown

from DTbot import DTbot
from database_management import dbcallprocedure
from linklist import changelog_link
from util.PaginatorSession import PaginatorSession


class General(commands.Cog):
    """General utility commands, like user info and uptime, among others"""

    def __init__(self, bot: DTbot):
        self.bot = bot
        main_dev = self.bot.bot_config.get('Developers', 'main')
        secondary_dev = self.bot.bot_config.get('Developers', 'secondary')
        self.MAIN_DEV_ID = self.bot.bot_config.getint('Developers', 'main dev id')
        self.DTBOT_DEVS = f'{main_dev}\n{secondary_dev}'
        self.INVITE = self.bot.bot_config.get('General', 'INVITE')
        self.PERMSEXPL = self.bot.bot_config.get('General', 'PERMSEXPL')
        self.REQHALL = self.bot.bot_config.getint('General', 'REQHALL')
        self.AVATAR_ARTIST = self.bot.bot_config.get('About', 'AVATAR ARTIST')
        self.GH_LINK = self.bot.bot_config.get('About', 'GH LINK')
        self.SUPPORT_LINK = self.bot.bot_config.get('About', 'SUPPORT LINK')
        self.TWITTER_LINK = self.bot.bot_config.get('About', 'TWITTER LINK')
        self.ANNOUNCEMENT_LINK = self.bot.bot_config.get('About', 'ANNOUNCEMENT LINK')
        self.ANNOUNCEMENT_MSG = self.bot.bot_config.get('About', 'ANNOUNCEMENT MSG')

    @commands.command(description="Displays a user's avatar. Defaults to command user's avatar when "
                                  "no user is mentioned.",
                      brief="Show a user's avatar")
    @commands.bot_has_permissions(embed_links=True)
    async def avatar(self, ctx: commands.Context, *, user: discord.Member = None):
        if user:
            avatar_url = user.avatar.url
            embed = discord.Embed(colour=self.bot.dtbot_colour,
                                  description=f"{user.mention}'s avatar\n\n[Avatar Link]({avatar_url})")
            embed.set_image(url=avatar_url)
        else:
            avatar_url = ctx.author.avatar.url
            embed = discord.Embed(colour=self.bot.dtbot_colour,
                                  description=f"{ctx.author.mention}'s avatar\n\n[Avatar Link]({avatar_url})")
            embed.set_image(url=avatar_url)
        await ctx.send(embed=embed)

    @commands.command(description='Current DTbot announcements',
                      brief='DTbot announcements')
    async def announcements(self, ctx: commands.Context):
        embed = discord.Embed(colour=self.bot.dtbot_colour, title='Announcement',
                              url=self.ANNOUNCEMENT_LINK,
                              description=self.ANNOUNCEMENT_MSG)
        await ctx.send(embed=embed)

    @commands.command(description="Get an overview over the recentmost update of DTbot",
                      brief="Recent updates to DTbot")
    @commands.bot_has_permissions(embed_links=True)
    async def changelog(self, ctx: commands.Context):
        latest_commit = requests.get("https://api.github.com/repos/MajorTanya/DTbot/commits").json()[0]
        dtbot_version = self.bot.bot_config.get('Info', 'dtbot_version')
        last_updated = self.bot.bot_config.get('Info', 'last_updated')
        embed = discord.Embed(colour=self.bot.dtbot_colour,
                              description=f'__Recent changes to DTbot:__\nNewest version: {dtbot_version} '
                                          f'({last_updated})')
        embed.set_image(url=changelog_link)
        embed.add_field(name=f"Latest Commit", value=f"[`{latest_commit['sha'][:7]}`]({latest_commit['html_url']})\t"
                                                     f"{latest_commit['commit']['message']}")
        embed.set_footer(text="Prefixes have been discontinued. Check out DTbot's Slash Commands instead!")
        await ctx.send(embed=embed)

    @commands.command(hidden=True,
                      description="Discontinued, see `@DTbot announcements`.",
                      aliases=['csp', 'changeprefix', 'prefix'])
    @commands.has_guild_permissions(manage_guild=True)
    async def changeserverprefix(self, ctx: commands.Context, *_):
        await ctx.send("Custom prefix have been discontinued. Check `@DTbot announcements` for more information.")

    @commands.command(description="Info about me, DTbot. Please take a look.",
                      brief="Info about me")
    @commands.bot_has_permissions(embed_links=True)
    async def info(self, ctx: commands.Context):
        now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        uptime = now_dt - self.bot.bot_startup
        dtbot_version = self.bot.bot_config.get('Info', 'dtbot_version')
        embed = discord.Embed(title=f"{self.bot.user.name}'s info",
                              description=f"Hello, I'm {self.bot.user.name}, a multipurpose bot for your Discord "
                                          f"server.\n\nIf you have any command requests, use the `request` "
                                          f"command.\n\nThank you and have a good day.\n\n[__**"
                                          f"{self.bot.user.name} Support Server**__]({self.SUPPORT_LINK})",
                              colour=self.bot.dtbot_colour)
        embed.add_field(name="Authors", value=self.DTBOT_DEVS)
        embed.add_field(name="GitHub repository", value=f"Find me [here]({self.GH_LINK})")
        embed.add_field(name="Twitter", value=f"[Tweet @DTbotDiscord]({self.TWITTER_LINK})", inline=True)
        embed.add_field(name="Stats", value=f"In {len(self.bot.guilds)} servers with {len(self.bot.users)} members")
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name="Invite me", value=f"[Invite me]({self.INVITE}) to your server too.\n"
                                                f"[Explanation]({self.PERMSEXPL}) for DTbot's permissions")
        embed.add_field(name="Avatar by", value=self.AVATAR_ARTIST, inline=False)
        embed.set_footer(text=f"DTbot v. {dtbot_version}")
        await ctx.send(embed=embed)

    @commands.command(description="Show the latency between DTbot and the Discord web servers",
                      brief="Pong")
    @cooldown(3, 30, commands.BucketType.guild)
    async def ping(self, ctx: commands.Context):
        try:
            embed = discord.Embed(colour=self.bot.dtbot_colour,
                                  description=f':ping_pong:\n**Pong!** __**`{self.bot.latency * 1000:.2f} ms`**__')
            await ctx.send(embed=embed)
        except discord.Forbidden:  # not allowed to send embeds
            await ctx.send(f':ping_pong:\n**Pong!** __**`{self.bot.latency * 1000:.2f} ms`**__')

    @commands.command(description=f"Request a command to be added to DTbot. Functionality can be described in detail."
                                  f"\nPlease keep it reasonably concise.\nRestricted to 2 uses every 24 hours.\n\n"
                                  f"Usage:\n@DTbot request burn Burn someone at the stake for being a heretic.",
                      brief="Request a new command (2x/24hr)",
                      aliases=['req'])
    @cooldown(2, 86400, commands.BucketType.user)
    async def request(self, ctx: commands.Context, command: str, *functionality: str):
        reqhall = self.bot.get_channel(self.REQHALL)
        dev_dm = self.bot.get_user(self.MAIN_DEV_ID)
        embed = discord.Embed(title=f"New request by {ctx.author.name}",
                              description=f'{ctx.author} (ID: {ctx.author.id}) requested the following command:',
                              colour=ctx.author.colour)
        embed.add_field(name='Suggested command name', value=f'**{command}**')
        embed.add_field(name='Suggested functionality', value=f'*{" ".join(functionality)}*', inline=False)
        await reqhall.send('New command request!', embed=embed)
        await dev_dm.send('New command request!', embed=embed)
        await ctx.send(f'New command request was sent to the developers, {ctx.author.mention}.')

    @commands.command(hidden=True,
                      description="Discontinued, see `@DTbot announcements`. "
                                  "Mention DTbot instead or use its Slash Commands.",
                      aliases=['rsp', 'resetprefix'])
    @commands.has_guild_permissions(manage_guild=True)
    async def resetserverprefix(self, ctx: commands.Context):
        await ctx.send("Custom prefix have been discontinued. Check `@DTbot announcements` for more information."
                       "Mention DTbot instead or use its Slash Commands.")

    @commands.command(description="Gives the bot's uptime since the last restart.",
                      brief="DTbot's uptime")
    async def uptime(self, ctx: commands.Context):
        now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        uptime = now_dt - self.bot.bot_startup
        await ctx.send(f"{self.bot.user.name}'s uptime is: `{uptime}`")

    @commands.command(description="Shows details on user, such as Name, Join Date, or Highest Role",
                      brief="Get info on a user",
                      aliases=['uinfo'])
    @commands.bot_has_permissions(embed_links=True)
    async def userinfo(self, ctx: commands.Context, user: discord.Member):
        join_ts = int(user.joined_at.timestamp())
        created_ts = int(user.created_at.timestamp())
        embed = discord.Embed(title=f"{user}'s info",
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
    async def whohas(self, ctx: commands.Context, *, role: discord.Role):
        role = discord.utils.get(ctx.guild.roles, name=role.name)
        embed_desc_max_size = 2048  # max char count in embed.description of a discord.Embed
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
            pages.append(discord.Embed(colour=role.colour,
                                       title=f'{len(role.members)} users with {role.name} - Page {i + 1}/{page_count}',
                                       description=page_members))
        p_sess = PaginatorSession(ctx, pages=pages)
        await p_sess.run()

    @commands.command(description="Shows a user's XP points. If no user is mentioned, it will default to command user.",
                      brief="Check user's XP")
    async def xp(self, ctx: commands.Context, user: discord.Member = None):
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


async def setup(bot: DTbot):
    await bot.add_cog(General(bot))
