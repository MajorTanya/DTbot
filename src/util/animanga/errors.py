from discord import app_commands


class AniMangaLookupError(app_commands.AppCommandError):
    # raised if something went wrong with the anime/manga lookup with the AL API
    def __init__(self, *, title: str) -> None:
        self.title = title
        super().__init__(f'Something went wrong when looking up "{title}" on AniList.')
