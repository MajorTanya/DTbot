import re
import urllib.parse
from configparser import ConfigParser

import discord
import requests

from DTbot import DTbot
from error_handler import AniMangaLookupError
from util.utils import even_out_embed_fields

config = ConfigParser()
config.read('./config/config.ini')
AL_API_URL = config.get('AniManga Lookup', 'AL_API_URL')
KITSU_URL = config.get('AniManga Lookup', 'kitsu_url')
MAL_URL = config.get('AniManga Lookup', 'mal_url')
anime_query = config.get('AniManga Lookup', 'anime_query')
manga_query = config.get('AniManga Lookup', 'manga_query')
kitsu_query = config.get('AniManga Lookup', 'kitsu_query')
# Kitsu needs URL encoded strings, except for '&' and '=', which would break the filters if encoded
kitsu_filters = urllib.parse.quote(config.get('AniManga Lookup', 'kitsu_filters'), safe='&=')
kitsu_query += kitsu_filters


def request(title: str, is_manga: bool):  # request the entry from AniList
    query = manga_query if is_manga else anime_query
    response = requests.post(AL_API_URL, json={'query': query, 'variables': {'search': title}})
    result = response.json()['data']['Page']
    if result['pageInfo']['total'] == 0:  # nothing found
        raise AniMangaLookupError(title=title)
    else:
        return result['media'][0]


def make_date(date: dict):
    # combine dates to YYYY-MM-DD with None as question marks because some entries may be None from the API
    year = date['year'] if date['year'] else '????'
    month = date['month'] if date['month'] else '??'
    day = date['day'] if date['day'] else '??'
    return f'{year}-{str(month).rjust(2, "0")}-{str(day).rjust(2, "0")}'


class AniListMediaResultView(discord.ui.View):

    def __init__(self, *, anilist: str, kitsu: str | None = None, mal: str | None = None):
        super().__init__()
        self.add_item(discord.ui.Button(label=f'AniList', url=anilist, emoji='<:AniList:742063839259918336>'))
        self.add_item(discord.ui.Button(label=f'Kitsu', disabled=kitsu is None, url=kitsu,
                                        emoji='<:Kitsu:742063838555275337>'))
        self.add_item(discord.ui.Button(label=f'MyAnimeList', disabled=mal is None, url=mal,
                                        emoji='<:MyAnimeList:742063838760927323>'))


class AniListMediaResult:
    def __init__(self, title: str, is_manga: bool, bot: DTbot):
        self.bot = bot
        self.AL: str | None = None
        self.MAL: str | None = None
        self.Kitsu: str | None = None
        result = request(title, is_manga)
        self.embed = self.process_result(result['idMal'], is_manga, result)
        self.view = AniListMediaResultView(anilist=self.AL, kitsu=self.Kitsu, mal=self.MAL)

    def process_result(self, mal_id, manga: bool, result):
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
            if season_str != 'None None':
                embed.add_field(name='Season', value=season_str)

        if result['status'] != 'NOT_YET_RELEASED':
            start_date = make_date(result['startDate'])
            embed.add_field(name='Start Date', value=start_date)
        if result['status'] == 'FINISHED':
            end_date = make_date(result['endDate'])
            embed.add_field(name='End Date', value=end_date)

        self.AL = al_url
        self.Kitsu = kitsu if kitsu else None
        self.MAL = mal if mal else None

        return even_out_embed_fields(embed)
