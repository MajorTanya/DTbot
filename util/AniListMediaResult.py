import re
import urllib.parse

import discord
import requests

from DTbot import config
from error_handler import AniMangaLookupError

AL_API_URL = config.get('AniManga Lookup', 'AL_API_URL')
KITSU_URL = config.get('AniManga Lookup', 'kitsu_url')
MAL_URL = config.get('AniManga Lookup', 'mal_url')
anime_query = config.get('AniManga Lookup', 'anime_query')
manga_query = config.get('AniManga Lookup', 'manga_query')
kitsu_query = config.get('AniManga Lookup', 'kitsu_query')
# Kitsu needs URL encoded strings, except for '&' and '=', which would break the filters if encoded
kitsu_filters = urllib.parse.quote(config.get('AniManga Lookup', 'kitsu_filters'), safe='&=')
kitsu_query += kitsu_filters


def request(title, is_manga: bool):  # request the entry from AniList
    query = manga_query if is_manga else anime_query
    response = requests.post(AL_API_URL, json={'query': query, 'variables': {'search': title}})
    result = response.json()['data']['Page']
    if result['pageInfo']['total'] == 0:  # nothing found
        raise AniMangaLookupError(title=title, status_code=response.status_code, manga=is_manga)
    else:
        return result['media'][0]


def make_date(date: dict):
    # combine dates to YYYY-MM-DD with None as question marks because some entries may be None from the API
    year = date['year'] if date['year'] else '????'
    month = date['month'] if date['month'] else '??'
    day = date['day'] if date['day'] else '??'
    return f'{year}-{str(month).rjust(2, "0")}-{str(day).rjust(2, "0")}'


class AniListMediaResult:
    def __init__(self, title, is_manga: bool, bot):
        self.bot = bot
        self.MAL = ''
        self.Kitsu = ''
        result = request(title, is_manga)
        self.embed = self.process_result(result['idMal'], is_manga, result)

    def process_result(self, mal_id, manga, result):
        mal, kitsu = '', ''
        al_url = result['siteUrl']
        if mal_id:  # if AL doesn't know what the ID on MAL is, we just don't bother to get Kitsu
            mal = f'{MAL_URL}/{result["type"].lower()}/{mal_id}'
            kitsu_req = kitsu_query.replace('MALIDHERE', str(mal_id)).replace('TYPE', result['type'].lower())
            k_res = requests.get(kitsu_req).json()
            try:  # fetch the entry itself from Kitsu again because the above is not a full entry
                k_res2 = requests.get(k_res['data'][0]['relationships']['item']['links']['self']).json()
                kitsu = f'{KITSU_URL}/{result["type"].lower()}/{k_res2["data"]["id"]}'
            except IndexError:
                pass

        if result['coverImage']['color']:
            rgb = tuple(int(result['coverImage']['color'].lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
            colour = discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2])
        else:
            colour = self.bot.dtbot_colour
        title = result['title']['romaji']
        description = re.sub('<.*?>', '', result['description']) if result['description'] else ""
        embed = discord.Embed(colour=colour, title=title, description=description)

        cover_image = result['coverImage']['large']
        embed.set_image(url=cover_image)

        genres = ""
        for genre in result['genres']:
            genres += genre + ', '
        genres = genres[:len(genres) - 2] if result['genres'] != [] else 'N/A'
        embed.add_field(name='Genres', value=genres)

        ft = result['format'].replace('_', ' ').title().replace('Tv', 'TV').replace('Ova', 'OVA').replace('Ona', 'ONA')
        embed.add_field(name='Format', value=ft)

        media_entries = [None, '']
        if manga:
            chapters = result['chapters']
            volumes = result['volumes']
            if chapters and chapters != 0:
                ch_str = f'{chapters} Chapter' if chapters == 1 else f'{chapters} Chapters'
                vol_str = ''
                if volumes and volumes != 0:
                    vol_str = f'{volumes} Volume' if volumes == 1 else f'{volumes} Volumes'
                media_entries = ['Chapters', f'{ch_str}{" in " + vol_str if vol_str else ""}']
        else:
            if result['episodes']:
                episodes = f"{result['episodes']} Episode"
                if result['episodes'] != 1:
                    episodes = f'{episodes}s'
                duration_str = 'Minutes' if result['duration'] != 1 else 'Minute'
                duration = f" à {result['duration']} {duration_str}" if result['duration'] else ''
                media_entries = ['Episodes', f'{episodes}{duration}']
        if media_entries[0]:
            embed.add_field(name=media_entries[0], value=media_entries[1])

        embed.add_field(name='Status', value=(result['status'].replace('_', ' ').title()))

        if result['averageScore']:
            embed.add_field(name='Average Score', value=f"{result['averageScore']}%")

        if not manga:
            season = result['season'].title() if result['season'] else None
            season_str = f"{season} {result['seasonYear']}" if result['status'] != 'NOT_YET_RELEASED' else 'Unknown'
            embed.add_field(name='Season', value=season_str)

        if result['status'] != 'NOT_YET_RELEASED':
            start_date = make_date(result['startDate'])
            embed.add_field(name='Start Date', value=start_date)
        if result['status'] == 'FINISHED':
            end_date = make_date(result['endDate'])
            embed.add_field(name='End Date', value=end_date)

        if len(embed.fields) % 3 != 0:  # even out the last line of info embed fields
            embed.add_field(name='\u200b', value='\u200b')
            if len(embed.fields) % 3 == 2:  # if we added one and still need one more to make it 3
                embed.add_field(name='\u200b', value='\u200b')

        embed.add_field(name='<:AniList:742063839259918336> AniList', value=f"[AniList]({al_url})")
        urls = ['<:Kitsu:742063838555275337> Kitsu', f"[Kitsu]({kitsu})",
                '<:MyAnimeList:742063838760927323> MAL', f"[MyAnimeList]({mal})"]
        embed.add_field(name=urls[0] if kitsu else '\u200b', value=urls[1] if kitsu else '\u200b')
        embed.add_field(name=urls[2] if mal else '\u200b', value=urls[3] if mal else '\u200b')

        return embed
