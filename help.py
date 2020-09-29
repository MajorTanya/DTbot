import asyncio
from collections import OrderedDict

import discord
from discord.ext import commands

from DTbot import config
from error_handler import IllegalCustomCommandAccess

hidden_cogs = config.items('Hidden')
allowed_servers = config.get('General', 'allowed_servers')


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
        if isinstance(page, discord.Embed):
            self.pages.append(page)
        else:
            raise TypeError('Page must be a discord.Embed.')

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


def acq_sig(bot, ctx, command):
    bot.help_command.context = ctx
    signature = bot.help_command.get_command_signature(command=command)
    return signature


def command_help(bot, ctx, cmd):
    if cmd.cog.qualified_name in hidden_cogs[0][1]:
        if str(ctx.message.guild.id) not in allowed_servers:
            raise IllegalCustomCommandAccess(ctx)

    embed = discord.Embed(colour=bot.dtbot_colour, description=f'{cmd.description}\n\n{acq_sig(bot, ctx, cmd)}',
                          title=f'{ctx.prefix}{cmd.name}')
    return embed


def cog_help(bot, ctx, cog):
    if cog.qualified_name in hidden_cogs[0][1]:
        if str(ctx.message.guild.id) not in allowed_servers:
            raise IllegalCustomCommandAccess(ctx)

    cmd_list = []
    embed = discord.Embed(colour=bot.dtbot_colour, title=cog.qualified_name)
    embed2 = discord.Embed(colour=bot.dtbot_colour)
    embed3 = discord.Embed(colour=bot.dtbot_colour)
    for command in bot.commands:
        if not command.hidden:
            if command.cog is cog:
                cmd_list.append(command)

    sorted_commands = sorted(cmd_list, key=lambda x: x.name)
    if len(sorted_commands) > 0:
        field_counter = 0
        for c in sorted_commands:
            if field_counter < 21:
                embed.add_field(name=f'**{ctx.prefix}{c.name}**', value=f'{c.brief}')
                field_counter += 1
            elif 21 <= field_counter < 42:
                embed2.add_field(name=f'**{ctx.prefix}{c.name}**', value=f'{c.brief}')
                field_counter += 1
            elif 42 <= field_counter < 63:
                embed3.add_field(name=f'**{ctx.prefix}{c.name}**', value=f'{c.brief}')
                field_counter += 1

        if field_counter <= 21:
            return [embed]
        elif 21 < field_counter <= 42:
            embed.title = f'{cog.qualified_name}, Part 1/2'
            embed2.title = f'{cog.qualified_name}, Part 2/2'
            return [embed, embed2]
        elif 42 < field_counter <= 63:
            embed.title = f'{cog.qualified_name}, Part 1/3'
            embed2.title = f'{cog.qualified_name}, Part 2/3'
            embed3.title = f'{cog.qualified_name}, Part 3/3'
            return [embed, embed2, embed3]


def bot_help(bot, ctx):
    cog_list = []
    cog_dict = OrderedDict()
    embed = discord.Embed(colour=bot.dtbot_colour, title='DTbot',
                          description=f'An overview over all DTbot modules'
                                      f'\nDo `{ctx.prefix}help [module]` for a command overview of the module.')
    for c in bot.cogs:
        if str(ctx.message.guild.id) in allowed_servers and c in hidden_cogs[0][1]:
            cog_list.append(bot.cogs[c].qualified_name)
            continue
        elif c is None or c in hidden_cogs[1][1]:
            continue
        cog_list.append(bot.cogs[c].qualified_name)
    cog_list = sorted(cog_list)
    for cog in cog_list:
        cog_dict[cog] = bot.cogs[cog].description
        embed.add_field(name=f'**{cog}**', value=bot.cogs[cog].description, inline=False)

    return embed


class Help(commands.Cog):
    """Go here for help"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage='[command or module]')
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, ctx, *command: str):
        """Shows this message"""
        pages = []
        command = ' '.join(command)
        if command != '':
            cog = cmd = None
            if command.lower() == 'help':
                cmd = self.bot.get_command(command)
            elif command in hidden_cogs[0][1]:
                cog = self.bot.get_cog(hidden_cogs[2][1])
            else:
                cog = self.bot.get_cog(command.title() if not command.lower() == 'rng' else command.upper())
                cmd = self.bot.get_command(command)
            if cog:
                embed = cog_help(self.bot, ctx, cog)
                if embed:
                    for em in embed:
                        pages.append(em)
                    p_sess = PaginatorSession(ctx, pages=pages,
                                              footer=f'Type {ctx.prefix}help [command] for more info on a command.')
                    await p_sess.run()

            elif cmd:
                embed = command_help(self.bot, ctx, cmd)
                return await ctx.send(embed=embed)
            else:
                pass

        else:
            embed = bot_help(self.bot, ctx)
            pages.append(embed)
            p_sess = PaginatorSession(ctx, pages=pages,
                                      footer=f'Type {ctx.prefix}help [module] for more info on a module.')
            await p_sess.run()


def setup(bot):
    bot.add_cog(Help(bot))
