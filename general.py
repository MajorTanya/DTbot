import datetime
import itertools
import math
from platform import python_version

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from DTbot import DTbot
from linklist import changelog_link
from util.AniListMediaQuery import AniListMediaQuery
from util.PaginatorSession import PaginatorSession
from util.database_utils import DBProcedure, dbcallprocedure
from util.utils import even_out_embed_fields

anilist_cooldown = app_commands.Cooldown(80, 60)


class RequestModal(discord.ui.Modal, title="Request for DTbot"):
    def __init__(self, bot: DTbot):
        super().__init__()
        self.bot = bot
        self.functionality = discord.ui.TextInput(
            label="Functionality",
            placeholder="Short description here",
            max_length=100,
        )
        self.description = discord.ui.TextInput(
            label="Description",
            style=discord.TextStyle.long,
            placeholder="Describe the feature in more detail here",
            max_length=500,
        )
        self.add_item(self.functionality).add_item(self.description)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Thank you for your request, {interaction.user.name}.", ephemeral=True)
        embed = discord.Embed(title=f"Requested: {self.functionality.value}", description=self.description.value)
        req_hall: discord.TextChannel = self.bot.get_channel(self.bot.bot_config.getint("General", "REQHALL"))  # type: ignore
        await req_hall.send(f"{interaction.user} filed the following feature request:", embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("Something went wrong, please try again later.", ephemeral=True)
        raise


class General(commands.Cog):
    """General commands, like user info, uptime, anime/manga lookup, among others"""

    def __init__(self, bot: DTbot):
        self.bot = bot
        main_dev = self.bot.bot_config.get("Developers", "main")
        secondary_dev = self.bot.bot_config.get("Developers", "secondary")
        self.DTBOT_DEVS = f"{main_dev}\n{secondary_dev}"
        self.INVITE = self.bot.bot_config.get("General", "INVITE")
        self.PERMSEXPL = self.bot.bot_config.get("General", "PERMSEXPL")
        self.REQHALL = self.bot.bot_config.getint("General", "REQHALL")
        self.AVATAR_ARTIST = self.bot.bot_config.get("About", "AVATAR ARTIST")
        self.GH_LINK = self.bot.bot_config.get("About", "GH LINK")
        self.COMMITS_URL = self.bot.bot_config.get("About", "GH COMMITS LINK")
        self.SUPPORT_LINK = self.bot.bot_config.get("About", "SUPPORT LINK")
        self.TWITTER_LINK = self.bot.bot_config.get("About", "TWITTER LINK")
        self.ANNOUNCEMENT_LINK = self.bot.bot_config.get("About", "ANNOUNCEMENT LINK")
        self.ANNOUNCEMENT_MSG = self.bot.bot_config.get("About", "ANNOUNCEMENT MSG")

    @app_commands.command(description="Look up an Anime on AniList (SFW results only)")
    @app_commands.describe(title="The title to look up")
    @app_commands.checks.bot_has_permissions(embed_links=True, use_external_emojis=True)
    @app_commands.checks.dynamic_cooldown(lambda x: anilist_cooldown)
    async def anime(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer()
        media_query = AniListMediaQuery(bot=self.bot)
        embed, view = await media_query.lookup(title=title, is_manga=False)
        await interaction.followup.send(embed=embed, view=view)

    @app_commands.command(description="Current DTbot announcements")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def announcements(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour=DTbot.DTBOT_COLOUR,
            title="Announcement",
            url=self.ANNOUNCEMENT_LINK,
            description=self.ANNOUNCEMENT_MSG,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Shows the mentioned user's (server) avatar.")
    @app_commands.describe(user="The user whose avatar to show")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def avatar(self, interaction: discord.Interaction, user: discord.Member | discord.User | None):
        user = user if user else interaction.user
        embed = discord.Embed(
            colour=DTbot.DTBOT_COLOUR,
            description=f"{user.mention}'s avatar\n\n[Avatar Link]({user.display_avatar.url})",
        )
        embed.set_image(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Shows an overview over the recentmost update of DTbot")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def changelog(self, interaction: discord.Interaction):
        await interaction.response.defer()
        dtbot_version = self.bot.bot_config.get("Info", "dtbot_version")
        last_updated = self.bot.bot_config.get("Info", "last_updated")
        async with aiohttp.ClientSession() as session:
            async with session.get(self.COMMITS_URL) as r:
                response = await r.json()
                latest_commit = response[0]
                embed = discord.Embed(
                    colour=DTbot.DTBOT_COLOUR,
                    description=f"__Recent changes to DTbot:__\nNewest version: {dtbot_version} ({last_updated})",
                )
                embed.set_image(url=changelog_link)
                embed.add_field(
                    name=f"Latest Commit",
                    value=f"[`{latest_commit['sha'][:7]}`]({latest_commit['html_url']})\t"
                    f"{latest_commit['commit']['message']}",
                )
                await interaction.followup.send(embed=embed)

    @app_commands.command(description="Info about me, DTbot. Please take a look.")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def info(self, interaction: discord.Interaction):
        now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        uptime = now_dt - self.bot.bot_startup
        dtbot_version = self.bot.bot_config.get("Info", "dtbot_version")
        embed = discord.Embed(
            colour=DTbot.DTBOT_COLOUR,
            title=f"{self.bot.user.name}'s info",  # type: ignore
            description=f"Hello, I'm {self.bot.user.name}, a multipurpose bot for your Discord "  # type: ignore
            f"server.\n\nIf you have any command requests, use the `request` command.\n\n"
            f"Thank you and have a good day.\n\n"
            f"[__**{self.bot.user.name} Support Server**__]({self.SUPPORT_LINK})",  # type: ignore
        )
        embed.add_field(name="Authors", value=self.DTBOT_DEVS)
        embed.add_field(name="GitHub repository", value=f"Find me [here]({self.GH_LINK})")
        embed.add_field(name="Twitter", value=f"[Tweet @DTbotDiscord]({self.TWITTER_LINK})", inline=True)
        embed.add_field(name="Stats", value=f"In {len(self.bot.guilds)} servers with {len(self.bot.users)} members")
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(
            name="Invite me",
            value=f"[Invite me]({self.INVITE}) to your server too.\n[Explanation]({self.PERMSEXPL}) for DTbot's "
            f"permissions",
        )
        embed.add_field(name="Avatar by", value=self.AVATAR_ARTIST, inline=False)
        embed.add_field(name="Made with", value=f"discord.py {discord.__version__} on Python {python_version()}")
        embed.set_footer(text=f"DTbot v. {dtbot_version}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Look up a Manga on AniList (SFW results only)")
    @app_commands.describe(title="The title to look up")
    @app_commands.checks.bot_has_permissions(embed_links=True, use_external_emojis=True)
    @app_commands.checks.dynamic_cooldown(lambda x: anilist_cooldown)
    async def manga(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer()
        media_query = AniListMediaQuery(bot=self.bot)
        embed, view = await media_query.lookup(title=title, is_manga=True)
        await interaction.followup.send(embed=embed, view=view)

    @app_commands.command(description="Show the latency between DTbot and the Discord web servers")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.checks.cooldown(3, 30.0, key=lambda i: i.guild_id)
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour=DTbot.DTBOT_COLOUR,
            description=f":ping_pong:\n**Pong!** __**`{self.bot.latency * 1000:.2f} ms`**__",
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Request some new functionality for DTbot. Limited to twice per day, per user.")
    @app_commands.checks.cooldown(2, 86400, key=lambda i: i.user.id)  # 86400 seconds = 60 * 60 * 24
    async def request(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RequestModal(self.bot))

    @app_commands.command(description="Shows details on this server, such as Name, Member amounts, Role count, etc.")
    @app_commands.guild_only()
    async def serverinfo(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild: discord.Guild = interaction.guild  # type: ignore # the command is set as guild_only, guild will exist
        embed = discord.Embed(colour=DTbot.DTBOT_COLOUR, title=f"About {guild.name}")
        if guild.description:
            embed.description = guild.description
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        if guild.banner:
            embed.set_image(url=guild.banner.url)
        embed.add_field(name="Name", value=guild.name)
        if guild.owner:
            embed.add_field(name="Owner", value=guild.owner.mention)

        created_at = int(guild.created_at.timestamp())
        embed.add_field(name="Created at", value=f"<t:{created_at}:D> - <t:{created_at}:T> (<t:{created_at}:R>)")

        boosters = f"{guild.premium_subscription_count} Booster{'s' if guild.premium_subscription_count != 1 else ''}"
        embed.add_field(name="Nitro Level", value=f"Level {guild.premium_tier} with {boosters}")

        channels = f"{len(guild.channels)} channel{'s' if len(guild.channels) != 1 else ''}"
        categories = f"{len(guild.categories)} categor{'ies' if len(guild.categories) != 1 else 'y'}"
        embed.add_field(name="Channels", value=f"{channels} in {categories}")

        bot_count = len([m for m in guild.members if m.bot])
        user_count = len(guild.members) - bot_count
        bots = f"{bot_count} bot{'s' if bot_count != 1 else ''}"
        users = f"{user_count} user{'s' if guild.member_count != 1 else ''}"
        embed.add_field(name="Members", value=f"{users} and {bots} ({guild.member_count} total)")

        embed.add_field(name="Roles", value=f"{len(guild.roles)}")

        non_animated_emotes = len([e for e in guild.emojis if not e.animated])
        animated_emotes = len([e for e in guild.emojis if e.animated])
        embed.add_field(name="Emotes", value=f"{non_animated_emotes} of {guild.emoji_limit} max")
        embed.add_field(name="Animated Emotes", value=f"{animated_emotes} of {guild.emoji_limit} max")
        embed.add_field(name="Stickers", value=f"{len(guild.stickers)} of {guild.sticker_limit} max")

        if guild.vanity_url:
            embed.add_field(name="Vanity Invite", value=f"[{guild.vanity_url_code}]({guild.vanity_url})")
        if guild.rules_channel:
            embed.add_field(name="Rules Channel", value=f"{guild.rules_channel.mention}")
        embed = even_out_embed_fields(embed)
        embed.set_footer(text=f"ID: {guild.id}", icon_url=guild.icon.url if guild.icon else None)
        await interaction.followup.send(embed=embed)

    @app_commands.command(description="Gives the bot's uptime since the last restart.")
    async def uptime(self, interaction: discord.Interaction):
        now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        uptime = now_dt - self.bot.bot_startup
        await interaction.response.send_message(f"{self.bot.user.name}'s uptime is: `{uptime}`")  # type: ignore

    @app_commands.command(description="Shows details on a user, such as Name, Join Date, or Highest Role")
    @app_commands.describe(user="The user to get some info on")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member | None):
        target: discord.Member | discord.User = user if user else interaction.user
        created_ts = int(target.created_at.timestamp())
        embed = discord.Embed(title=f"{target}'s info", description="Here is what I could find:")
        if target.display_name != target.name and target.display_name != target.global_name:
            embed.add_field(name="Nickname", value=f"{target.display_name}")
        embed.add_field(name="Display Name", value=f"{target.global_name}")
        embed.add_field(name="ID", value=f"{target.id}", inline=True)
        if isinstance(target, discord.Member):
            embed.add_field(name="Highest Role", value=f"<@&{target.top_role.id}>", inline=True)
            join_ts = int(target.joined_at.timestamp())
            embed.add_field(name="Joined at", value=f"<t:{join_ts}:D> - <t:{join_ts}:T>", inline=True)
        embed.add_field(name="Created at", value=f"<t:{created_ts}:D> - <t:{created_ts}:T>", inline=True)
        embed.set_footer(text=f"{target.name}'s Info", icon_url=f"{target.display_avatar.url}")
        embed.set_thumbnail(url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Shows how many users have a particular role (max. 15 pages)")
    @app_commands.describe(role="The role to check out")
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def whohas(self, interaction: discord.Interaction, role: discord.Role):
        if len(role.members) == 0:
            embed = discord.Embed(
                colour=role.colour,
                title=f"0 users with {role.name}",
                description=f"No members with the role {role.mention} exist.",
            )
            return await interaction.response.send_message(embed=embed)

        await interaction.response.defer()
        pages: list[discord.Embed] = []
        # unchanging values between calls
        max_pages = 15
        embed_desc_max_size = 2048  # former max char count in embed.description of a discord.Embed, better than 4096
        max_user_id_length = 19  # current max length of a user snowflake ID, can be shorter for older accounts
        max_mention_length = len("<@>, ") + max_user_id_length  # (24) mention string syntax & separators in listing
        users_per_page = math.floor(embed_desc_max_size / max_mention_length)  # (85) users / page

        role_member_count = len(role.members)
        # overshoots real value because older Discord users have shorter IDs, but makes the calculations a bit simpler
        needed_page_count: int = math.ceil((max_mention_length * role_member_count) / embed_desc_max_size)
        page_count = min(needed_page_count, max_pages)  # max. 15 pages allowed
        max_users = page_count * users_per_page  # max. 1275 total (15 pages * 85 users/page = 1275 users total)

        mentions_generator = (member.mention for member in role.members)
        # only evaluate the generator as many times as we can display users
        role_members = list(itertools.islice(mentions_generator, max_users))
        role_members.reverse()  # so we can pop() "from the front"

        for i in range(page_count):
            page_members = f"{role_member_count} members with {role.mention}\n\n" if i == 0 else ""
            while len(role_members) > 0 and ((len(page_members) + len(role_members[0])) < embed_desc_max_size):
                page_members += f"{role_members.pop()}, "
            page_members = page_members.rstrip(", ")
            embed = discord.Embed(
                colour=role.colour,
                title=f"{role_member_count} users with {role.name} - Page {i + 1}/{page_count}",
                description=page_members,
            )
            pages.append(embed)
        pager = PaginatorSession(pages=pages)
        await pager.start(interaction=interaction)

    @app_commands.command(description="Shows a user's XP points. Defaults to command user.")
    @app_commands.describe(user="The user whose XP to check")
    async def xp(self, interaction: discord.Interaction, user: discord.Member | discord.User | None):
        user = user if user else interaction.user
        if user.bot:
            return await interaction.response.send_message("Bots don't get XP. :robot:")
        await interaction.response.defer()
        xp = dbcallprocedure(self.bot.db_cnx, DBProcedure.GetUserXp, params=(user.id,))
        if xp > 0:
            await interaction.followup.send(f"**{user.display_name}** has `{xp}` XP.")
        else:
            await interaction.followup.send("User hasn't talked yet.")


async def setup(bot: DTbot):
    await bot.add_cog(General(bot))
