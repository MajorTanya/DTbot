import json
import random
import re

import discord
import requests
from discord.ext import commands
from discord.ext.commands import Cooldown, CooldownMapping, cooldown

from DTbot import config
from error_handler import AniMangaLookupError
from launcher import dtbot_colour

AL_API_URL = config.get('AL API Queries', 'API_URL')
anime_query = config.get('AL API Queries', 'anime_query')
manga_query = config.get('AL API Queries', 'manga_query')


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
anilist_cooldown = shared_cooldown(80, 60, commands.BucketType.default)


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

    class AniListMediaResult(object):
        def __init__(self, title, manga: bool):
            self.request(title, manga)

        def request(self, title, manga: bool):
            query = manga_query if manga else anime_query
            variables = {
                'search': title
            }
            response = requests.post(AL_API_URL, json={'query': query, 'variables': variables})
            result = json.loads(response.text)['data']['Page']
            if result['pageInfo']['total'] == 0:  # nothing found
                raise AniMangaLookupError(title=title, status_code=response.status_code, manga=manga)
            else:
                result = result['media'][0]
                self.title = result['title']['romaji']
                self.description = re.sub('<.*?>', '', result['description'])
                genres = ""
                for genre in result['genres']:
                    genres += genre + ', '
                self.genres = genres[:len(genres) - 2]
                self.format = result['format']
                self.status = result['status']
                self.status_str = self.status.replace('_', ' ').title()
                self.avgScore = result['averageScore']
                if manga:
                    self.chapters = result['chapters']
                    self.volumes = result['volumes']
                else:
                    self.episodes = result['episodes']
                    if result['episodes'] == 1:
                        self.ep_str = f"{result['episodes']} Episode"
                    else:
                        self.ep_str = f"{result['episodes']} Episodes"
                    self.duration = result['duration']
                    self.duration_str = 'Minutes' if self.duration != 1 else 'Minute'
                    self.season = result['season'].title() if result['season'] is not None else None
                    self.year = result['seasonYear']
                    self.season_str = f"{self.season} {self.year}" if self.status != 'NOT_YET_RELEASED' else 'Unknown'
                if self.status != 'NOT_YET_RELEASED':
                    # manually assemble the start (and end) date because some entries may be None from the API
                    date = result['startDate']
                    year = date['year'] if date['year'] is not None else '????'
                    month = date['month'] if date['month'] is not None else '??'
                    day = date['day'] if date['day'] is not None else '??'
                    self.startDate = f'{year}-{str(month).rjust(2, "0")}-{str(day).rjust(2, "0")}'
                if self.status == 'FINISHED':
                    date = result['endDate']
                    year = date['year'] if date['year'] is not None else '????'
                    month = date['month'] if date['month'] is not None else '??'
                    day = date['day'] if date['day'] is not None else '??'
                    self.endDate = f'{year}-{str(month).rjust(2, "0")}-{str(day).rjust(2, "0")}'
                self.id = result['id']
                if result['coverImage']['color']:
                    rgb = tuple(int(result['coverImage']['color'].lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
                    self.colour = discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2])
                else:
                    self.colour = dtbot_colour
                self.coverImage = result['coverImage']['large']

    @commands.command(description="Enter the title of an anime here and DTbot will return a small overview for that "
                                  "anime from AniList. Expect data like the synopsis, episode count, airing season, "
                                  "etc.\nMind you, AniList doesn't necessarily recognize abbreviations or alternative "
                                  "titles. The best bet is to look it up with the Japanese or official English titles."
                                  "\nUsage:\n\n+anime senko-san\n+anime oregairu 3",
                      brief="Look up an anime title on AniList",
                      aliases=['lookupanime', 'searchanime', 'animesearch'])
    @anilist_cooldown
    async def anime(self, ctx, *anime_title):
        anime = ' '.join(anime_title)
        result = Misc.AniListMediaResult(anime, False)
        ft = result.format
        ft_str = ft.replace('_', ' ').replace('SHORT', 'Short').replace('SPECIAL', 'Special').replace('MOVIE', 'Movie')
        embed = discord.Embed(colour=result.colour, title=result.title, description=result.description)
        embed.add_field(name='Genres', value=result.genres)
        embed.add_field(name='Format', value=ft_str)
        if result.episodes is not None:
            embed.add_field(name='Episodes', value=f"{result.ep_str} à {result.duration} {result.duration_str}")
        embed.add_field(name='Status', value=result.status_str)
        if result.avgScore is not None:
            embed.add_field(name='Average Score', value=f"{result.avgScore}%")
        embed.add_field(name='Season', value=result.season_str)
        if result.status != 'NOT_YET_RELEASED':
            embed.add_field(name='Start Date', value=result.startDate)
        if result.status == 'FINISHED':
            embed.add_field(name='End Date', value=result.endDate)
        if len(embed.fields) % 3 == 2:  # even out the last line of embeds
            embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='On AniList', value=f"[AniList link](https://anilist.co/anime/{result.id}/)",
                        inline=False)
        embed.set_image(url=result.coverImage)
        await ctx.send(embed=embed)

    @commands.command(description="Enter the title of a manga here and DTbot will return a small overview for that "
                                  "manga from AniList. Expect data like the synopsis, chapter count, release status, "
                                  "etc.\nMind you, AniList doesn't necessarily recognize abbreviations or alternative "
                                  "titles. The best bet is to look it up with the Japanese or official English titles."
                                  "\nUsage:\n\n+manga haikyuu\n+manga akatsuki no yona",
                      brief="Look up a manga title on AniList",
                      aliases=['lookupmanga', 'searchmanga', 'mangasearch'])
    @anilist_cooldown
    async def manga(self, ctx, *manga_title):
        manga = ' '.join(manga_title)
        result = Misc.AniListMediaResult(manga, True)
        embed = discord.Embed(colour=result.colour, title=result.title, description=result.description)
        embed.add_field(name='Genres', value=result.genres)
        ft_str = result.format.replace('_', ' ').title()
        embed.add_field(name='Format', value=ft_str)
        if result.chapters is not None and result.chapters != 0:
            vol_str = ""
            ch_str = f"{result.chapters} Chapter" if result.chapters == 1 else f"{result.chapters} Chapters"
            if result.volumes is not None and result.volumes != 0:
                vol_str = f"{result.volumes} Volume" if result.volumes == 1 else f"{result.volumes} Volumes"
            embed.add_field(name='Chapters', value=f'{ch_str}{" in " + vol_str if vol_str else ""}')
        embed.add_field(name='Status', value=result.status_str)
        if result.avgScore is not None:
            embed.add_field(name='Average Score', value=f"{result.avgScore}%")
        if result.status != 'NOT_YET_RELEASED':
            embed.add_field(name='Start Date', value=result.startDate)
        if result.status == 'FINISHED':
            embed.add_field(name='End Date', value=result.endDate)
        if len(embed.fields) % 3 == 2:  # even out the last line of embeds
            embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='On AniList', value=f"[AniList link](https://anilist.co/manga/{result.id}/)",
                        inline=False)
        embed.set_image(url=result.coverImage)
        await ctx.send(embed=embed)

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


def setup(bot):
    bot.add_cog(Misc(bot))
