from typing import Coroutine

import discord.ui

FIRST_PAGE = '⏮'
PREV_PAGE = '◀'
STOP = '⏹'
NEXT_PAGE = '▶'
LAST_PAGE = '⏭'
CUTOFFS: dict[str, int] = {
    FIRST_PAGE: 3,
    PREV_PAGE: 1,
    STOP: 1,
    NEXT_PAGE: 1,
    LAST_PAGE: 3
}


class NavButton(discord.ui.Button):
    """Custom subclass that takes a Coroutine callback for the button in its constructor"""

    def __init__(self, *, callback: Coroutine, style: discord.ButtonStyle = discord.ButtonStyle.secondary,
                 label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None,
                 emoji: str | discord.Emoji | discord.PartialEmoji | None = None, row: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji,
                         row=row)
        self.callback = callback


class PaginatorSession(discord.ui.View):
    def __init__(self, *, pages: list[discord.Embed] = None):
        super().__init__()
        self.callbacks: dict[str, Coroutine] = {
            FIRST_PAGE: self.first_page,
            PREV_PAGE: self.prev_page,
            STOP: self.stop_session,
            NEXT_PAGE: self.next_page,
            LAST_PAGE: self.last_page
        }
        if pages is None:
            pages = []
        self.pages = pages
        self.current = 0
        self.message: discord.Message | None = None

    async def start(self, interaction: discord.Interaction):
        self.message = await interaction.original_response()
        # add buttons manually, so we have first/last page skippers and normal next/prev/stop buttons only when needed
        view = discord.ui.View.from_message(self.message).clear_items()
        skippers_needed = len(self.pages) > CUTOFFS[FIRST_PAGE]
        pagers_needed = len(self.pages) > CUTOFFS[PREV_PAGE]
        if skippers_needed:
            view.add_item(NavButton(callback=self.callbacks[FIRST_PAGE], label=FIRST_PAGE))
        if pagers_needed:
            view.add_item(NavButton(callback=self.callbacks[PREV_PAGE], label=PREV_PAGE))
            view.add_item(NavButton(callback=self.callbacks[STOP], label=STOP))
            view.add_item(NavButton(callback=self.callbacks[NEXT_PAGE], label=NEXT_PAGE))
        if skippers_needed:
            view.add_item(NavButton(callback=self.callbacks[LAST_PAGE], label=LAST_PAGE))
        self.message = await interaction.edit_original_response(content=None, embed=self.pages[0], view=view)

    async def on_timeout(self) -> None:
        await super().on_timeout()
        if self.message:
            await self.message.edit(view=None)
            self.stop()

    async def first_page(self, interaction: discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()
        self.current = 0
        await interaction.edit_original_response(embed=self.pages[self.current])

    async def prev_page(self, interaction: discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()
        self.current = (self.current - 1) % len(self.pages)
        await interaction.edit_original_response(embed=self.pages[self.current])

    async def stop_session(self, interaction: discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()
        await interaction.edit_original_response(view=None)
        self.stop()

    async def next_page(self, interaction: discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()
        self.current = (self.current + 1) % len(self.pages)
        await interaction.edit_original_response(embed=self.pages[self.current])

    async def last_page(self, interaction: discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()
        self.current = len(self.pages) - 1
        await interaction.edit_original_response(embed=self.pages[self.current])
