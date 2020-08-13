import json
import random
import re
import urllib.parse

import discord
import requests
from discord.ext import commands
from discord.ext.commands import Cooldown, CooldownMapping, cooldown

from DTbot import config
from error_handler import AniMangaLookupError, send_cmd_help
from launcher import dtbot_colour

AL_API_URL = config.get('AniManga Lookup', 'AL_API_URL')
KITSU_URL = config.get('AniManga Lookup', 'kitsu_url')
MAL_URL = config.get('AniManga Lookup', 'mal_url')
anime_query = config.get('AniManga Lookup', 'anime_query')
manga_query = config.get('AniManga Lookup', 'manga_query')
kitsu_query = config.get('AniManga Lookup', 'kitsu_query')
# Kitsu needs URL encoded strings, except for '&' and '=', which would break the filters if encoded
kitsu_filters = urllib.parse.quote(config.get('AniManga Lookup', 'kitsu_filters'), safe='&=')
kitsu_query += kitsu_filters


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
            self.MAL = ''
            self.Kitsu = ''
            self.request(title, manga)

        def request(self, title, manga: bool):
            query = manga_query if manga else anime_query
            response = requests.post(AL_API_URL, json={'query': query, 'variables': {'search': title}})
            result = json.loads(response.text)['data']['Page']
            if result['pageInfo']['total'] == 0:  # nothing found
                raise AniMangaLookupError(title=title, status_code=response.status_code, manga=manga)
            else:
                result = result['media'][0]
                mal_id = result['idMal']
                self.AL_url = result['siteUrl']
                if mal_id is not None:  # if AL doesn't know what the ID on MAL is, we just don't bother to get Kitsu
                    self.MAL = f'{MAL_URL}/{result["type"].lower()}/{mal_id}'
                    kitsu_req = kitsu_query.replace('MALIDHERE', str(mal_id)).replace('TYPE', result['type'].lower())
                    k_res = json.loads(requests.get(kitsu_req).text)
                    try:
                        k_res2 = requests.get(k_res['data'][0]['relationships']['item']['links']['self'])
                        k_res2_json = json.loads(k_res2.text)
                        self.Kitsu = f'{KITSU_URL}/{result["type"].lower()}/{k_res2_json["data"]["id"]}'
                    except IndexError:
                        pass
                self.title = result['title']['romaji']
                self.description = re.sub('<.*?>', '', result['description'])
                genres = ""
                for genre in result['genres']:
                    genres += genre + ', '
                self.genres = genres[:len(genres) - 2] if result['genres'] != [] else 'N/A'
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
                                  "etc.\n*Doesn't* return NSFW entries.\nMind you, AniList doesn't necessarily "
                                  "recognize abbreviations or alternative titles. The best bet is to look it up with "
                                  "the Japanese or official English titles.\nUsage:\n\n+anime senko-san\n+anime "
                                  "oregairu 3",
                      brief="Look up an anime title on AniList",
                      aliases=['lookupanime', 'searchanime', 'animesearch'])
    @anilist_cooldown
    async def anime(self, ctx, *anime_title):
        anime = ' '.join(anime_title)
        if anime != '':
            result = Misc.AniListMediaResult(anime, False)
            ft = result.format
            ft_str = ft.replace('_', ' ').title().replace('Tv', 'TV').replace('Ova', 'OVA').replace('Ona', 'ONA')
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
            if len(embed.fields) % 3 != 0:  # even out the last line of info embed fields
                embed.add_field(name='\u200b', value='\u200b')
                if len(embed.fields) % 3 == 2:  # if we added one and still need one more to make it 3
                    embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name='<:AniList:742063839259918336> AniList', value=f"[AniList]({result.AL_url})")
            urls = ['<:Kitsu:742063838555275337> Kitsu', f"[Kitsu]({result.Kitsu})",
                    '<:MyAnimeList:742063838760927323> MAL', f"[MyAnimeList]({result.MAL})"]
            embed.add_field(name=urls[0] if result.Kitsu else '\u200b', value=urls[1] if result.Kitsu else '\u200b')
            embed.add_field(name=urls[2] if result.MAL else '\u200b', value=urls[3] if result.MAL else '\u200b')
            embed.set_image(url=result.coverImage)
            await ctx.send(embed=embed)
        else:
            try:
                await send_cmd_help(self.bot, ctx, "")
            except discord.Forbidden:  # not allowed to send embeds
                await send_cmd_help(self.bot, ctx, "", plain=True)

    @commands.command(description="Enter the title of a manga here and DTbot will return a small overview for that "
                                  "manga from AniList. Expect data like the synopsis, chapter count, release status, "
                                  "etc.\n*Doesn't* return NSFW entries.\nMind you, AniList doesn't necessarily "
                                  "recognize abbreviations or alternative titles. The best bet is to look it up with "
                                  "the Japanese or official English titles.\nUsage:\n\n+manga haikyuu\n+manga "
                                  "akatsuki no yona",
                      brief="Look up a manga title on AniList",
                      aliases=['lookupmanga', 'searchmanga', 'mangasearch'])
    @anilist_cooldown
    async def manga(self, ctx, *manga_title):
        manga = ' '.join(manga_title)
        if manga != '':
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
            if len(embed.fields) % 3 != 0:  # even out the last line of info embed fields
                embed.add_field(name='\u200b', value='\u200b')
                if len(embed.fields) % 3 == 2:  # if we added one and still need one more to make it 3
                    embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name='<:AniList:742063839259918336> AniList', value=f"[AniList]({result.AL_url})")
            urls = ['<:Kitsu:742063838555275337> Kitsu', f"[Kitsu]({result.Kitsu})",
                    '<:MyAnimeList:742063838760927323> MAL', f"[MyAnimeList]({result.MAL})"]
            embed.add_field(name=urls[0] if result.Kitsu else '\u200b', value=urls[1] if result.Kitsu else '\u200b')
            embed.add_field(name=urls[2] if result.MAL else '\u200b', value=urls[3] if result.MAL else '\u200b')
            embed.set_image(url=result.coverImage)
            await ctx.send(embed=embed)
        else:
            try:
                await send_cmd_help(self.bot, ctx, "")
            except discord.Forbidden:  # not allowed to send embeds
                await send_cmd_help(self.bot, ctx, "", plain=True)

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
