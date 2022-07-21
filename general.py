import datetime
from math import ceil

import discord
import requests
from discord import app_commands
from discord.ext import commands

from DTbot import DTbot
from linklist import changelog_link
from util.AniListMediaResult import AniListMediaResult
from util.PaginatorSession import PaginatorSession
from util.utils import dbcallprocedure

anilist_cooldown = app_commands.Cooldown(80, 60)


class RequestModal(discord.ui.Modal, title='Request for DTbot'):
    def __init__(self, bot: DTbot):
        super().__init__()
        self.bot = bot

    functionality = discord.ui.TextInput(label='Functionality', placeholder='Short description here')
    description = discord.ui.TextInput(label='Description', style=discord.TextStyle.long,
                                       placeholder='Describe the feature in more detail here', max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thank you for your request, {interaction.user.name}.',
                                                ephemeral=True)
        embed = discord.Embed(title=f'Requested: {self.functionality}', description=self.description)
        req_hall = self.bot.get_channel(self.bot.bot_config.getint('General', 'REQHALL'))
        await req_hall.send(f'{interaction.user} filed the following feature request:', embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message('Something went wrong, please try again later.', ephemeral=True)
        raise


class General(commands.Cog):
    """General commands, like user info, uptime, anime/manga lookup, among others"""

    def __init__(self, bot: DTbot):
        self.bot = bot
        main_dev = self.bot.bot_config.get('Developers', 'main')
        secondary_dev = self.bot.bot_config.get('Developers', 'secondary')
        self.DTBOT_DEVS = f'{main_dev}\n{secondary_dev}'
        self.INVITE = self.bot.bot_config.get('General', 'INVITE')
        self.PERMSEXPL = self.bot.bot_config.get('General', 'PERMSEXPL')
        self.REQHALL = self.bot.bot_config.getint('General', 'REQHALL')
        self.AVATAR_ARTIST = self.bot.bot_config.get('About', 'AVATAR ARTIST')
        self.GH_LINK = self.bot.bot_config.get('About', 'GH LINK')
        self.COMMITS_URL = self.bot.bot_config.get('About', 'GH COMMITS LINK')
        self.SUPPORT_LINK = self.bot.bot_config.get('About', 'SUPPORT LINK')
        self.TWITTER_LINK = self.bot.bot_config.get('About', 'TWITTER LINK')
        self.ANNOUNCEMENT_LINK = self.bot.bot_config.get('About', 'ANNOUNCEMENT LINK')
        self.ANNOUNCEMENT_MSG = self.bot.bot_config.get('About', 'ANNOUNCEMENT MSG')

    @app_commands.command(description="Look up an Anime on AniList (SFW results only)")
    @app_commands.describe(title="The title to look up")
    @app_commands.checks.bot_has_permissions(embed_links=True, use_external_emojis=True)
    @app_commands.checks.dynamic_cooldown(lambda x: anilist_cooldown)
    async def anime(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer()
        result = AniListMediaResult(title, is_manga=False, bot=self.bot)
        await interaction.followup.send(embed=result.embed, view=result.view)

    @app_commands.command(description='Current DTbot announcements')
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def announcements(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=self.bot.dtbot_colour, title='Announcement',
                              url=self.ANNOUNCEMENT_LINK,
                              description=self.ANNOUNCEMENT_MSG)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Shows the mentioned user's (server) avatar.")
    @app_commands.describe(user="The user whose avatar to show")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def avatar(self, interaction: discord.Interaction, user: discord.Member | discord.User | None):
        user = user if user else interaction.user
        embed = discord.Embed(colour=self.bot.dtbot_colour,
                              description=f"{user.mention}'s avatar\n\n[Avatar Link]({user.display_avatar.url})")
        embed.set_image(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Shows an overview over the recentmost update of DTbot")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def changelog(self, interaction: discord.Interaction):
        await interaction.response.defer()
        dtbot_version = self.bot.bot_config.get('Info', 'dtbot_version')
        last_updated = self.bot.bot_config.get('Info', 'last_updated')
        latest_commit = requests.get(self.COMMITS_URL).json()[0]
        embed = discord.Embed(colour=self.bot.dtbot_colour,
                              description=f'__Recent changes to DTbot:__\nNewest version: {dtbot_version} '
                                          f'({last_updated})')
        embed.set_image(url=changelog_link)
        embed.add_field(name=f"Latest Commit", value=f"[`{latest_commit['sha'][:7]}`]({latest_commit['html_url']})\t"
                                                     f"{latest_commit['commit']['message']}")
        await interaction.followup.send(embed=embed)

    @app_commands.command(description="Info about me, DTbot. Please take a look.")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def info(self, interaction: discord.Interaction):
        now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        uptime = now_dt - self.bot.bot_startup
        dtbot_version = self.bot.bot_config.get('Info', 'dtbot_version')
        embed = discord.Embed(title=f"{self.bot.user.name}'s info",
                              description=f"Hello, I'm {self.bot.user.name}, a multipurpose bot for your Discord "
                                          f"server.\n\nIf you have any command requests, use the `request` command.\n\n"
                                          f"Thank you and have a good day.\n\n"
                                          f"[__**{self.bot.user.name} Support Server**__]({self.SUPPORT_LINK})",
                              colour=self.bot.dtbot_colour)
        embed.add_field(name="Authors", value=self.DTBOT_DEVS)
        embed.add_field(name="GitHub repository", value=f"Find me [here]({self.GH_LINK})")
        embed.add_field(name="Twitter", value=f"[Tweet @DTbotDiscord]({self.TWITTER_LINK})", inline=True)
        embed.add_field(name="Stats", value=f"In {len(self.bot.guilds)} servers with {len(self.bot.users)} members")
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name="Invite me", value=f"[Invite me]({self.INVITE}) to your server too."
                                                f"\n[Explanation]({self.PERMSEXPL}) for DTbot's permissions")
        embed.add_field(name="Avatar by", value=self.AVATAR_ARTIST, inline=False)
        embed.set_footer(text=f"DTbot v. {dtbot_version}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Look up a Manga on AniList (SFW results only)")
    @app_commands.describe(title="The title to look up")
    @app_commands.checks.bot_has_permissions(embed_links=True, use_external_emojis=True)
    @app_commands.checks.dynamic_cooldown(lambda x: anilist_cooldown)
    async def manga(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer()
        result = AniListMediaResult(title, is_manga=True, bot=self.bot)
        await interaction.followup.send(embed=result.embed, view=result.view)

    @app_commands.command(description="Show the latency between DTbot and the Discord web servers")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.checks.cooldown(3, 30.0, key=lambda i: i.guild_id)
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=self.bot.dtbot_colour,
                              description=f':ping_pong:\n**Pong!** __**`{self.bot.latency * 1000:.2f} ms`**__')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Request some new functionality for DTbot. Limited to twice per day, per user.")
    @app_commands.checks.cooldown(2, 86400, key=lambda i: i.user_id)  # 86400 seconds = 60 * 60 * 24
    async def request(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RequestModal(self.bot))

    @app_commands.command(description="Gives the bot's uptime since the last restart.")
    async def uptime(self, interaction: discord.Interaction):
        now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        uptime = now_dt - self.bot.bot_startup
        await interaction.response.send_message(f"{self.bot.user.name}'s uptime is: `{uptime}`")

    @app_commands.command(description="Shows details on a user, such as Name, Join Date, or Highest Role")
    @app_commands.describe(user="The user to get some info on")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member | None):
        user = user if user else interaction.user
        join_ts = int(user.joined_at.timestamp())
        created_ts = int(user.created_at.timestamp())
        embed = discord.Embed(title=f"{user}'s info",
                              description='Here is what I could find:', colour=interaction.user.colour)
        embed.add_field(name='Nickname', value=f'{user.display_name}')
        embed.add_field(name='ID', value=f'{user.id}', inline=True)
        embed.add_field(name='Status', value=f'{user.status}', inline=True)
        embed.add_field(name='Highest Role', value=f'<@&{user.top_role.id}>', inline=True)
        embed.add_field(name='Joined at', value=f'<t:{join_ts}:D> - <t:{join_ts}:T>', inline=True)
        embed.add_field(name='Created at', value=f'<t:{created_ts}:D> - <t:{created_ts}:T>', inline=True)
        embed.set_footer(text=f"{user.name}'s Info", icon_url=f'{user.display_avatar.url}')
        embed.set_thumbnail(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description='Shows how many users have a particular role (max. 10 pages)')
    @app_commands.describe(role='The role to check out')
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def whohas(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.response.defer()
        embed_desc_max_size = 2048  # former max char count in embed.description of a discord.Embed, better than 4096
        pages = []
        role_members = [member.mention for member in role.members]
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
        pager = PaginatorSession(pages=pages)
        await pager.start(interaction=interaction)

    @app_commands.command(description="Shows a user's XP points. Defaults to command user.")
    @app_commands.describe(user="The user whose XP to check")
    async def xp(self, interaction: discord.Interaction, user: discord.Member | discord.User | None):
        user = user if user else interaction.user
        if user.bot:
            return await interaction.response.send_message("Bots don't get XP. :robot:")
        await interaction.response.defer()
        xp = dbcallprocedure(self.bot.db_cnx, 'GetUserXp', returns=True, params=(user.id, '@res'))
        if xp > 0:
            await interaction.followup.send(f"**{user.display_name}** has `{xp}` XP.")
        else:
            await interaction.followup.send("User hasn't talked yet.")


async def setup(bot: DTbot):
    await bot.add_cog(General(bot))
