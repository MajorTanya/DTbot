import random

import discord
from discord.ext import commands
from discord.ext.commands import Cooldown, CooldownMapping, cooldown

from error_handler import send_cmd_help
from linklist import woop_links
from util.AniListMediaResult import AniListMediaResult


def shared_cooldown(rate, per, type=commands.BucketType.default):
    # we have one rate limit for AniList, not differentiated by media type, so we build a shared cooldown that tracks
    # uses across different commands
    cooldown = Cooldown(rate, per, type=type)

    def decorator(func):
        if isinstance(func, commands.Command):
            func._buckets = CooldownMapping(cooldown)
        else:
            func.__commands_cooldown__ = cooldown
        return func

    return decorator


# AniList rate limit is 90/minute, so we make the command cooldown to 80/minute to be safe
anilist_cooldown = shared_cooldown(80, 60)


class Misc(commands.Cog):
    """Miscellaneous commands for fun"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="SAY BLESS YOU TO THE CAT",
                      brief="Say bless you to the cat")
    @cooldown(3, 60, commands.BucketType.guild)
    async def cat(self, ctx):
        await ctx.send('<:sneezecat:472732802727804928> <:sneezecat:472732802727804928> '
                       '<:sneezecat:472732802727804928> <:sneezecat:472732802727804928> '
                       '<:sneezecat:472732802727804928>')

    @commands.command(description="For when you need to pay a lot of respects",
                      brief="Pay big Respects")
    async def bigf(self, ctx):
        await ctx.send('FFFFFFFFFFFFFFFFFFF\nFFFFFFFFFFFFFFFFFFF\nFFFFFFFFFF\nFFFFFFFFFF\nFFFFFFFFFFFFFFFFFFF\n'
                       'FFFFFFFFFFFFFFFFFFF\nFFFFFFFFFF\nFFFFFFFFFF\nFFFFFFFFFF\nFFFFFFFFFF')

    @commands.command(description="To Pay Respects",
                      brief="Pay Respects")
    async def f(self, ctx):
        await ctx.send('fffffffffffffff\nfffffff\nfffffffffffffff\nfffffff\nfffffff')

    @commands.command(description="Enter the title of an anime here and DTbot will return a small overview for that "
                                  "anime from AniList. Expect data like the synopsis, episode count, airing season, "
                                  "etc.\n*Doesn't* return NSFW entries.\nMind you, AniList doesn't necessarily "
                                  "recognize abbreviations or alternative titles. The best bet is to look it up with "
                                  "the Japanese or official English titles.\nUsage:\n\n+anime senko-san\n+anime "
                                  "oregairu 3",
                      brief="Look up an anime title on AniList",
                      aliases=['lookupanime', 'searchanime', 'animesearch'])
    @commands.bot_has_permissions(embed_links=True)
    @anilist_cooldown
    async def anime(self, ctx, *anime_title):
        anime = ' '.join(anime_title)
        if anime == '':
            try:
                await send_cmd_help(self.bot, ctx, "")
            except discord.Forbidden:  # not allowed to send embeds
                await send_cmd_help(self.bot, ctx, "", plain=True)
        else:
            await ctx.trigger_typing()
            result = AniListMediaResult(anime, is_manga=False, bot=self.bot)
            await ctx.send(embed=result.embed)

    @commands.command(description="Enter the title of a manga here and DTbot will return a small overview for that "
                                  "manga from AniList. Expect data like the synopsis, chapter count, release status, "
                                  "etc.\n*Doesn't* return NSFW entries.\nMind you, AniList doesn't necessarily "
                                  "recognize abbreviations or alternative titles. The best bet is to look it up with "
                                  "the Japanese or official English titles.\nUsage:\n\n+manga haikyuu\n+manga "
                                  "akatsuki no yona",
                      brief="Look up a manga title on AniList",
                      aliases=['lookupmanga', 'searchmanga', 'mangasearch'])
    @commands.bot_has_permissions(embed_links=True)
    @anilist_cooldown
    async def manga(self, ctx, *manga_title):
        manga = ' '.join(manga_title)
        if manga == '':
            try:
                await send_cmd_help(self.bot, ctx, "")
            except discord.Forbidden:  # not allowed to send embeds
                await send_cmd_help(self.bot, ctx, "", plain=True)
        else:
            await ctx.trigger_typing()
            result = AniListMediaResult(manga, is_manga=True, bot=self.bot)
            await ctx.send(embed=result.embed)

    @commands.command(description="Actually you can't",
                      brief="Kill yourself")
    async def kms(self, ctx):
        possible_responses = [
            'NO',
            'NEVER',
            'HOW ABOUT NO',
            'Need a hug? <:kannahug:461996510637326386>',
            'Yeah, sure. *If* you can do it in the next nanosecond.\nWell, you failed. Then my answer is no.',
            'NOPE',
            'What would you say if I told you that it is impossible',
            "Your pet wouldn't know why you didn't come home, so no.",
            "We would miss you, so don't."
        ]
        await ctx.send(random.choice(possible_responses))

    @commands.command(description="IT'S JUST A REEE BRO",
                      brief="REEEEE")
    @cooldown(3, 120, commands.BucketType.guild)
    async def re(self, ctx):
        await ctx.send('REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')

    @commands.command(description="Woop woop!",
                      brief="Woop woop!")
    @commands.bot_has_permissions(embed_links=True)
    async def woop(self, ctx):
        chosen = random.choice(woop_links)
        embed = discord.Embed(colour=self.bot.dtbot_colour, description=f'[Image link]({chosen})')
        embed.set_image(url=f"{chosen}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
