import re
import urllib.parse

import aiohttp
import discord

from DTbot import DTbot
from error_handler import AniMangaLookupError
from util.AniListResponseDTO import AniListResponseDTO

AL_EMOTE = "<:AniList:742063839259918336>"
KITSU_EMOTE = "<:Kitsu:742063838555275337>"
MAL_EMOTE = "<:MyAnimeList:742063838760927323>"


class AniListMediaResultView(discord.ui.View):
    def __init__(self, *, anilist: str, kitsu: str | None = None, mal: str | None = None):
        super().__init__()
        self.add_item(discord.ui.Button(label=f"AniList", url=anilist, emoji=AL_EMOTE))
        self.add_item(discord.ui.Button(label=f"Kitsu", disabled=kitsu is None, url=kitsu, emoji=KITSU_EMOTE))
        self.add_item(discord.ui.Button(label=f"MyAnimeList", disabled=mal is None, url=mal, emoji=MAL_EMOTE))


class AniListMediaQuery:
    def __init__(self, bot: DTbot):
        self.bot = bot
        self._AniList: str
        self._MyAnimeList: str | None = None
        self._Kitsu: str | None = None
        self._is_manga_request: bool | None = None
        self._AL_API_URL = self.bot.bot_config.get("AniManga Lookup", "AL_API_URL")
        self._KITSU_URL = self.bot.bot_config.get("AniManga Lookup", "kitsu_url")
        self._MAL_URL = self.bot.bot_config.get("AniManga Lookup", "mal_url")
        self._anilist_query = self.bot.bot_config.get("AniManga Lookup", "anilist_query")
        self._kitsu_query = self.bot.bot_config.get("AniManga Lookup", "kitsu_query")
        # Kitsu needs URL encoded strings, except for '&' and '=', which would break the filters if encoded
        kitsu_filters = urllib.parse.quote(self.bot.bot_config.get("AniManga Lookup", "kitsu_filters"), safe="&=")
        self._kitsu_query += kitsu_filters

    async def lookup(self, title: str, is_manga: bool) -> tuple[discord.Embed, AniListMediaResultView]:
        """Look up an Anime or Manga on AniList, Kitsu, and MyAnimeList - Returns an Embed and a View"""
        self._is_manga_request = is_manga
        anilist_dto = await self._fetch_from_anilist(title)
        embed = await self._process_result(anilist_dto)
        view = AniListMediaResultView(anilist=self._AniList, kitsu=self._Kitsu, mal=self._MyAnimeList)
        return embed, view

    async def _fetch_from_anilist(self, title: str) -> AniListResponseDTO:
        """Searches AniList for the title - Returns an AniListResponseDTO, or raises an AniMangaLookupError"""
        query = self._anilist_query.replace("INSERTTYPE", "MANGA" if self._is_manga_request else "ANIME")
        async with aiohttp.ClientSession() as session:
            async with session.post(self._AL_API_URL, json={"query": query, "variables": {"search": title}}) as r:
                response = await r.json()
                result = response["data"]["Page"]
                if result["pageInfo"]["total"] == 0:  # nothing found
                    raise AniMangaLookupError(title=title)
                else:
                    return AniListResponseDTO.from_media_response(result["media"][0])

    async def _fetch_from_kitsu(self, anilist_id: int) -> str | None:
        """Fetches Kitsu info for an AniList ID - Returns the Kitsu URL, or None if no valid AL->Kitsu mapping exists"""
        media_type = "manga" if self._is_manga_request else "anime"
        kitsu_url = None
        kitsu_req = self._kitsu_query.replace("ALIDHERE", str(anilist_id)).replace("TYPE", media_type)
        async with aiohttp.ClientSession() as session:
            async with session.get(kitsu_req) as r:
                try:
                    kitsu_response = await r.json()
                    if kitsu_response["meta"]["count"] != 0:
                        kitsu_url = f"{self._KITSU_URL}/{media_type}/{kitsu_response['included'][0]['id']}"
                except (IndexError, KeyError):
                    pass
        return kitsu_url

    async def _process_result(self, dto: AniListResponseDTO) -> discord.Embed:
        """Processes the AniListResponseDTO to build an Embed - Returns the built Embed"""
        colour = DTbot.DTBOT_COLOUR
        self._AniList = dto.site_url
        self._Kitsu = await self._fetch_from_kitsu(dto.id_al)

        if dto.id_mal:
            self._MyAnimeList = f"{self._MAL_URL}/{'manga' if dto.is_manga else 'anime'}/{dto.id_mal}"

        if dto.cover_image and dto.cover_image.rgb:
            colour = discord.Colour.from_rgb(dto.cover_image.rgb[0], dto.cover_image.rgb[1], dto.cover_image.rgb[2])

        description = re.sub("<.*?>", "", dto.description) if dto.description is not None else None
        embed = discord.Embed(colour=colour, title=dto.title.romaji, description=description)

        if dto.cover_image:
            embed.set_image(url=dto.cover_image.url)

        if dto.title.english and dto.title.english.casefold() != dto.title.romaji.casefold():
            embed.add_field(name="English Title", value=dto.title.english)

        if dto.source_type:
            embed.add_field(name="Source", value=dto.source_type)

        if dto.genres:
            embed.add_field(name="Genres", value=", ".join(dto.genres))

        if dto.format:
            embed.add_field(name="Format", value=dto.format)

        if entries_strs := _make_entries_string(dto):
            heading = "Runtime" if dto.format == "Movie" else "Episodes"
            embed.add_field(name="Chapters" if dto.is_manga else heading, value=entries_strs)

        if dto.status:
            embed.add_field(name="Status", value=dto.status)

        if dto.average_score:
            embed.add_field(name="Average Score", value=f"{dto.average_score}%")

        if not dto.is_manga and dto.season and dto.season_year:
            embed.add_field(name="Season", value=f"{dto.season.title()} {dto.season_year}")

        if dto.start_date and dto.end_date and dto.start_date == dto.end_date:
            embed.add_field(name="Release Date", value=dto.start_date)
        else:
            if dto.start_date:
                embed.add_field(name="Start Date", value=dto.start_date)
            if dto.end_date:
                embed.add_field(name="End Date", value=dto.end_date)

        if not dto.is_manga and dto.next_airing_episode:
            timestamp_str = f"<t:{dto.next_airing_episode}:F> (<t:{dto.next_airing_episode}:R>)"
            embed.add_field(name=f"Next Episode Date", value=timestamp_str)

        if dto.studio:
            embed.add_field(name="Studio", value=f"[{dto.studio.name}]({dto.studio.site_url})")

        if dto.staff:
            staff = ""
            for staffer in dto.staff:
                staffer_entry = f"- {staffer.role}: {staffer.name}\n"
                if (len(staff) + len(staffer_entry)) > 1024:  # max length of embed field
                    break
                staff += staffer_entry
            embed.add_field(name="Staff", value=staff.strip(), inline=False)

        return embed


def _make_entries_string(dto: AniListResponseDTO) -> str | None:
    """Create "`X Chapter{s}[in Y Volume{s}]`" or "`X Episode{s}[à Y Minute{s}]`" style strings"""
    if (dto.is_manga and not dto.chapters) or (not dto.is_manga and not dto.episodes):
        return None
    entry_amount = dto.chapters if dto.is_manga else dto.episodes
    episode_or_movie = "Movie" if dto.format == "Movie" else "Episode"
    entries_str = f"{entry_amount} {'Chapter' if dto.is_manga else episode_or_movie}{'s' if entry_amount != 1 else ''}"
    vols_or_dur = ""

    if dto.is_manga and dto.volumes:
        vols_or_dur = f" in {dto.volumes} Volume{'s' if dto.volumes != 1 else ''}"
    elif not dto.is_manga and dto.duration:
        vols_or_dur = f" à {dto.duration} Minute{'s' if dto.duration != 1 else ''}"

    return f"{entries_str}{vols_or_dur}"
