from collections import OrderedDict

import nextcord
from nextcord.ext import commands

from DTbot import config
from error_handler import IllegalCustomCommandAccess
from util.PaginatorSession import PaginatorSession

hidden_cogs = config.items('Hidden')
allowed_servers = config.get('General', 'allowed_servers')


def acq_sig(bot, ctx, command):
    bot.help_command.context = ctx
    signature = bot.help_command.get_command_signature(command=command)
    return signature


def command_help(bot, ctx, cmd):
    if cmd.cog.qualified_name in hidden_cogs[0][1]:
        if str(ctx.message.guild.id) not in allowed_servers:
            raise IllegalCustomCommandAccess(ctx)

    embed = nextcord.Embed(colour=bot.dtbot_colour, description=f'{cmd.description}\n\n{acq_sig(bot, ctx, cmd)}',
                           title=f'{ctx.prefix}{cmd.name}')
    return embed


def cog_help(bot, ctx, cog):
    if cog.qualified_name in hidden_cogs[0][1]:
        if str(ctx.message.guild.id) not in allowed_servers:
            raise IllegalCustomCommandAccess(ctx)

    cmd_list = []
    embed = nextcord.Embed(colour=bot.dtbot_colour, title=cog.qualified_name)
    embed2 = nextcord.Embed(colour=bot.dtbot_colour)
    embed3 = nextcord.Embed(colour=bot.dtbot_colour)
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
    embed = nextcord.Embed(colour=bot.dtbot_colour, title='DTbot',
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
                        if len(em.fields) % 3 != 0:  # even out the last line of info embed fields
                            em.add_field(name='\u200b', value='\u200b')
                            if len(em.fields) % 3 == 2:  # if we added one and still need one more to make it 3
                                em.add_field(name='\u200b', value='\u200b')
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
