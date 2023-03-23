import dataclasses
import enum
from typing import Any, Self


class StaffRole(enum.Enum):
    ORIGINAL_CREATOR = 0
    DIRECTOR = 1
    STORY_AND_ART = 2
    STORY = 3
    ART = 4
    CHAR_DESIGN = 5


DISPLAYED_STAFF_ROLES = [
    ("Original Creator", StaffRole.ORIGINAL_CREATOR),
    ("Director", StaffRole.DIRECTOR),
    ("Story & Art", StaffRole.STORY_AND_ART),
    ("Story", StaffRole.STORY),
    ("Art", StaffRole.ART),
    ("Character Design", StaffRole.CHAR_DESIGN),
]

# fmt: off
UNDISPLAYED_STAFF_ROLES = [
    '(eps ', 'Action', 'ADR', 'Animation', 'Art Design', 'Art Director', 'Assistant',
    'CG', 'Chief', 'Episode', 'Photography', 'Sound', 'Sub', 'Touch-up',
]  # fmt: on


@dataclasses.dataclass(frozen=True)
class AniListMediaStaffer:
    role_order: int
    name: str
    role: str


@dataclasses.dataclass(frozen=True)
class AniListMediaStudio:
    name: str
    site_url: str


@dataclasses.dataclass(frozen=True)
class AniListMediaTitle:
    romaji: str
    english: str | None


@dataclasses.dataclass(frozen=True)
class AniListMediaCover:
    url: str
    rgb: tuple[int, int, int] | None


@dataclasses.dataclass(frozen=True)
class AniListResponseDTO:
    id_al: int
    id_mal: int | None
    site_url: str
    title: AniListMediaTitle
    description: str | None
    source_type: str | None
    staff: list[AniListMediaStaffer] | None
    studio: AniListMediaStudio | None
    cover_image: AniListMediaCover | None
    genres: list[str]
    format: str | None
    chapters: int | None
    volumes: int | None
    episodes: int | None
    duration: int | None
    status: str | None
    next_airing_episode: int | None
    average_score: int | None
    season: str | None
    season_year: int | None
    start_date: str | None
    end_date: str | None
    is_manga: bool

    @classmethod
    def from_media_response(cls, media_response: dict[str, Any]) -> Self:
        """Build an AniListResponseDTO from the JSON response from AniList (for a single search result list entry)"""
        return AniListResponseDTO(
            id_al=media_response["id"],
            id_mal=media_response["idMal"],
            site_url=media_response["siteUrl"],
            title=AniListMediaTitle(
                romaji=media_response["title"]["romaji"],
                english=media_response["title"]["english"],
            ),
            description=media_response["description"],
            source_type=_source_type_mapper(media_response["source"]),
            staff=_filter_staff_entries(media_response["staff"]["edges"]),
            studio=_extract_studio_info(media_response["studios"]["nodes"]),
            cover_image=_extract_cover_image(media_response["coverImage"]),
            genres=media_response["genres"],
            format=_format_mapper(media_response["format"]),
            chapters=media_response["chapters"],
            volumes=media_response["volumes"],
            episodes=media_response["episodes"],
            duration=media_response["duration"],
            status=_extract_status_info(media_response["status"]),
            next_airing_episode=_extract_next_episode_date(media_response["nextAiringEpisode"]),
            average_score=media_response["averageScore"],
            season=media_response["season"],
            season_year=media_response["seasonYear"],
            start_date=_make_date(media_response["startDate"]),
            end_date=_make_date(media_response["endDate"]),
            is_manga=media_response["type"] == "MANGA",
        )


def _colour_string_to_rgb_tuple(color_str: str | None) -> tuple[int, int, int] | None:
    """Transforms the hex colour string to a tuple of RGB values - Returns a tri-tuple of ints, or None if the colour
    string was None"""
    return None if color_str is None else tuple(int(color_str.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))


def _extract_cover_image(cover_element: dict[str, str | None]) -> AniListMediaCover | None:
    """Extracts cover image data from the media response - Returns an AniListMediaCover, or None if the media entry
    uses the default cover (i.e. no 'real' cover is available)"""
    if cover_element["large"] is None or cover_element["large"].endswith("default.jpg"):
        return None
    else:
        return AniListMediaCover(url=cover_element["large"], rgb=_colour_string_to_rgb_tuple(cover_element["color"]))


def _extract_next_episode_date(next_airing_date: dict[str, int] | None) -> int | None:
    """Extracts the info about the next episode airing date from the nullable entry - Returns an int representing a
    timestamp in seconds, or None if no date info is available"""
    return None if next_airing_date is None else next_airing_date["airingAt"]


def _extract_status_info(status: str | None) -> str | None:
    """Extracts the release status info from the nullable entry - Returns a string, or None if no status info is
    available"""
    return None if status is None else status.replace("_", " ").title()


def _extract_studio_info(studios: list[dict[str, Any]]) -> AniListMediaStudio | None:
    """Extracts the studio info from a list of studios - Returns an AniListMediaStudio, or None if no studios were
    provided"""
    return None if not studios else AniListMediaStudio(name=studios[0]["name"], site_url=studios[0]["siteUrl"])


def _filter_staff_entries(staff: list[dict[str, Any]] | None) -> list[AniListMediaStaffer] | None:
    """Filters the staff list to only keep some roles - Returns a (potentially empty) list of AniListMediaStaffer,
    or None if the provided list was None"""
    if staff is None:
        return None
    filtered_staff: list[AniListMediaStaffer] = []
    for member in staff:
        for undisplayed_role in UNDISPLAYED_STAFF_ROLES:
            if undisplayed_role in member["role"]:
                break
        else:
            for displayed_role in DISPLAYED_STAFF_ROLES:
                if displayed_role[0] in member["role"]:
                    filtered_staff.append(
                        AniListMediaStaffer(
                            displayed_role[1].value,
                            member["node"]["name"]["userPreferred"],
                            member["role"],
                        )
                    )
                    break
    filtered_staff.sort(key=lambda x: x.role_order)
    return filtered_staff


def _format_mapper(media_format: str | None) -> str | None:
    """Maps release formats to non-caps strings where needed ("MOVIE" -> "Movie", or "TV_SHORT" -> "TV Short", etc.,
    but "TV" -> "TV") - Returns the adjusted string"""
    match media_format:
        case "MOVIE" | "SPECIAL" | "MUSIC" | "MANGA" | "NOVEL":
            return media_format.title()
        case "TV_SHORT":
            return "TV Short"
        case "ONE_SHOT":
            return "One-Shot"
        case "TV" | "OVA" | "ONA" | _:
            return media_format


def _source_type_mapper(source: str | None) -> str | None:
    """Maps source types to non-caps strings where needed ("LIGHT_NOVEL" -> "Light Novel", "MANGA" -> "Manga", etc.) -
    Returns the adjusted string"""
    return None if source is None else source.replace("_", " ").title()  # Currently no special adjustments necessary


def _make_date(date: dict[str, int | None]) -> str | None:
    """Combine dates to YYYY-MM-DD with unknown parts as question marks - Returns the string, or None if the string
    would be "????-??-??" """
    year = date["year"] if date["year"] else "????"
    month = date["month"] if date["month"] else "??"
    day = date["day"] if date["day"] else "??"
    return full_date if (full_date := f"{year}-{month:02}-{day:02}") != "????-??-??" else None
