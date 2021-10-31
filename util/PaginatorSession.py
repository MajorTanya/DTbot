import asyncio
from collections import OrderedDict

import nextcord


class PaginatorSession:
    def __init__(self, ctx, timeout=60, pages=None, footer=''):
        if pages is None:
            pages = []
        self.footer = footer
        self.ctx = ctx
        self.timeout = timeout
        self.pages = pages
        self.running = False
        self.message = None
        self.current = 0
        self.reactions = OrderedDict({
            '⏮': self.first_page,
            '◀': self.previous_page,
            '⏹': self.close,
            '▶': self.next_page,
            '⏭': self.last_page
        })

    def add_page(self, page):
        if isinstance(page, nextcord.Embed):
            self.pages.append(page)
        else:
            raise TypeError('Page must be a nextcord.Embed.')

    def valid_page(self, index):
        return index >= 0 or index < len(self.pages)

    async def show_page(self, index: int):
        if not self.valid_page(index):
            return

        self.current = index
        page = self.pages[index]
        page.set_footer(text=self.footer)

        if self.running:
            await self.message.edit(embed=page)
        else:
            self.running = True
            self.message = await self.ctx.send(embed=page)

            for reaction in self.reactions.keys():
                if len(self.pages) == 1 and reaction in '⏮◀▶⏭':
                    continue
                elif len(self.pages) == 2 and reaction in '⏮⏭':
                    continue
                await self.message.add_reaction(reaction)

    def react_check(self, reaction, user):
        """Check to make sure it only responds to reactions from the sender and on the same message"""
        if reaction.message.id != self.message.id:
            return False  # not the same message
        if user.id != self.ctx.author.id:
            return False  # not the same user
        if reaction.emoji in self.reactions.keys():
            return True  # reaction was one of the pagination emojis

    async def run(self):
        if not self.running:
            await self.show_page(0)
        while self.running:
            try:
                reaction, user = await self.ctx.bot.wait_for('reaction_add', check=self.react_check,
                                                             timeout=self.timeout)
            except asyncio.TimeoutError:
                self.running = False
                try:
                    await self.message.clear_reactions()
                except:
                    pass
                finally:
                    break
            else:
                try:
                    await self.message.remove_reaction(reaction, user)
                except:
                    pass

                action = self.reactions[reaction.emoji]
                await action()

    async def first_page(self):
        return await self.show_page(0)

    async def last_page(self):
        return await self.show_page(len(self.pages) - 1)

    async def next_page(self):
        return await self.show_page((self.current + 1) % len(self.pages))

    async def previous_page(self):
        return await self.show_page((self.current - 1) % len(self.pages))

    async def close(self):
        self.running = False
        try:
            await self.message.clear_reactions()
            return
        except:
            pass
            return
