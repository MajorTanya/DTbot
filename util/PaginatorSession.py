from typing import Coroutine

import discord.ui

FIRST_PAGE = "⏮"
PREV_PAGE = "◀"
STOP = "⏹"
NEXT_PAGE = "▶"
LAST_PAGE = "⏭"
CUTOFFS: dict[str, int] = {
    FIRST_PAGE: 3,
    PREV_PAGE: 1,
    STOP: 1,
    NEXT_PAGE: 1,
    LAST_PAGE: 3,
}


class NavButton(discord.ui.Button):
    """Custom subclass that takes a Coroutine callback for the button in its constructor"""

    def __init__(
        self,
        *,
        callback: Coroutine,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        label: str | None = None,
        disabled: bool = False,
        custom_id: str | None = None,
        url: str | None = None,
        emoji: str | discord.Emoji | discord.PartialEmoji | None = None,
        row: int | None = None,
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
        )
        self.callback = callback


class NavButtonView(discord.ui.View):
    """Custom subclass that handles a timeout by clearing the interaction's view"""

    def __init__(self, *, interaction: discord.Interaction, timeout: float | None = 180.0):
        super().__init__(timeout=timeout)
        self.interaction = interaction

    async def on_timeout(self):
        if self.interaction:
            if not self.interaction.response.is_done():
                await self.interaction.response.defer()
            await self.interaction.edit_original_response(view=None)
        self.stop()


class PaginatorSession(object):
    def __init__(self, *, pages: list[discord.Embed] = None):
        super().__init__()
        self.callbacks: dict[str, Coroutine] = {
            FIRST_PAGE: self.first_page,
            PREV_PAGE: self.prev_page,
            STOP: self.stop_session,
            NEXT_PAGE: self.next_page,
            LAST_PAGE: self.last_page,
        }
        if pages is None:
            pages = []
        self.pages = pages
        self.current = 0
        self.view: NavButtonView | None = None

    async def start(self, interaction: discord.Interaction):
        # add buttons manually, so we have first/last page skippers and normal next/prev/stop buttons only when needed
        self.view = NavButtonView(interaction=interaction)  # default timeout of 180 seconds (3 minutes)
        skippers_needed = len(self.pages) > CUTOFFS[FIRST_PAGE]
        pagers_needed = len(self.pages) > CUTOFFS[PREV_PAGE]
        if skippers_needed:
            self.view.add_item(NavButton(callback=self.callbacks[FIRST_PAGE], emoji=FIRST_PAGE))
        if pagers_needed:
            self.view.add_item(NavButton(callback=self.callbacks[PREV_PAGE], emoji=PREV_PAGE))
            self.view.add_item(NavButton(callback=self.callbacks[STOP], emoji=STOP))
            self.view.add_item(NavButton(callback=self.callbacks[NEXT_PAGE], emoji=NEXT_PAGE))
        if skippers_needed:
            self.view.add_item(NavButton(callback=self.callbacks[LAST_PAGE], emoji=LAST_PAGE))
        await interaction.edit_original_response(content=None, embed=self.pages[0], view=self.view)

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
        self.view.stop()

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
