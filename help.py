from __future__ import annotations

import discord
from discord.ext import commands

from DTbot import DTbot
from error_handler import IllegalCustomCommandAccess
from util.PaginatorSession import PaginatorSession


class Help(commands.Cog):
    """Go here for help"""

    def __init__(self, bot: DTbot):
        self.bot = bot
        self.HIDDEN_COGS = self.bot.bot_config.items('Hidden')
        self.ALLOWED_SERVERS = self.bot.bot_config.get('General', 'allowed_servers')

    @commands.command(usage='[command or module]')
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, ctx: commands.Context, *command: str):
        """Shows this message"""
        pages = []
        command = ' '.join(command)
        used_prefix = self.clean_prefix(ctx.prefix)
        if command != '':
            cog = cmd = None
            if command.lower() == 'help':
                cmd = self.bot.get_command(command)
            elif command in self.HIDDEN_COGS[0][1]:
                cog = self.bot.get_cog(self.HIDDEN_COGS[2][1])
            else:
                cog = self.bot.get_cog(command.title() if not command.lower() == 'rng' else command.upper())
                cmd = self.bot.get_command(command)
            if cog:
                embed = self.cog_help(ctx, cog)
                if embed:
                    for em in embed:
                        if len(em.fields) % 3 != 0:  # even out the last line of info embed fields
                            em.add_field(name='\u200b', value='\u200b')
                            if len(em.fields) % 3 == 2:  # if we added one and still need one more to make it 3
                                em.add_field(name='\u200b', value='\u200b')
                        pages.append(em)
                    p_sess = PaginatorSession(ctx, pages=pages,
                                              footer=f'Type {used_prefix}help [command] for more info on a command.')
                    await p_sess.run()

            elif cmd:
                embed = self.command_help(ctx, cmd)
                return await ctx.send(embed=embed)
            else:
                pass

        else:
            embed = self.bot_help(ctx)
            pages.append(embed)
            p_sess = PaginatorSession(ctx, pages=pages,
                                      footer=f'Type {used_prefix}help [module] for more info on a module.')
            await p_sess.run()

    def clean_prefix(self, prefix: str | None):
        return prefix if prefix and prefix.strip() != self.bot.user.mention else f"@\u200b{self.bot.user.name} "

    def bot_help(self, ctx: commands.Context):
        cog_list = []
        cog_dict = {}
        embed = discord.Embed(colour=self.bot.dtbot_colour, title='DTbot',
                              description=f'An overview over all DTbot modules\n'
                                          f'Do `{self.clean_prefix(ctx.prefix)}help [module]` for a command overview of '
                                          f'the module.')
        for c in self.bot.cogs:
            if str(ctx.message.guild.id) in self.ALLOWED_SERVERS and c in self.HIDDEN_COGS[0][1]:
                cog_list.append(self.bot.cogs[c].qualified_name)
                continue
            elif c is None or c in self.HIDDEN_COGS[1][1]:
                continue
            cog_list.append(self.bot.cogs[c].qualified_name)
        cog_list = sorted(cog_list)
        for cog in cog_list:
            cog_dict[cog] = self.bot.cogs[cog].description
            embed.add_field(name=f'**{cog}**', value=self.bot.cogs[cog].description, inline=False)

        return embed

    def cog_help(self, ctx: commands.Context, cog: commands.Cog):
        if cog.qualified_name in self.HIDDEN_COGS[0][1]:
            if str(ctx.message.guild.id) not in self.ALLOWED_SERVERS:
                raise IllegalCustomCommandAccess(ctx)

        cmd_list = []
        used_prefix = self.clean_prefix(ctx.prefix)
        embed = discord.Embed(colour=self.bot.dtbot_colour, title=cog.qualified_name)
        embed2 = discord.Embed(colour=self.bot.dtbot_colour)
        embed3 = discord.Embed(colour=self.bot.dtbot_colour)
        for command in self.bot.commands:
            if not command.hidden:
                if command.cog is cog:
                    cmd_list.append(command)

        sorted_commands = sorted(cmd_list, key=lambda x: x.name)
        if len(sorted_commands) > 0:
            field_counter = 0
            for c in sorted_commands:
                if field_counter < 21:
                    embed.add_field(name=f'**{used_prefix}{c.name}**', value=f'{c.brief}')
                    field_counter += 1
                elif 21 <= field_counter < 42:
                    embed2.add_field(name=f'**{used_prefix}{c.name}**', value=f'{c.brief}')
                    field_counter += 1
                elif 42 <= field_counter < 63:
                    embed3.add_field(name=f'**{used_prefix}{c.name}**', value=f'{c.brief}')
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

    def acq_sig(self, ctx: commands.Context, command: commands.Command):
        self.bot.help_command.context = ctx
        signature = self.bot.help_command.get_command_signature(command)
        return signature.replace(ctx.clean_prefix, self.clean_prefix(ctx.prefix))

    def command_help(self, ctx: commands.Context, cmd: commands.Command):
        if cmd.cog.qualified_name in self.HIDDEN_COGS[0][1]:
            if str(ctx.message.guild.id) not in self.ALLOWED_SERVERS:
                raise IllegalCustomCommandAccess(ctx)

        embed = discord.Embed(colour=self.bot.dtbot_colour,
                              description=f'{cmd.description}\n\n{self.acq_sig(ctx, cmd)}',
                              title=f'{self.clean_prefix(ctx.prefix)}{cmd.name}')
        return embed


async def setup(bot: DTbot):
    await bot.add_cog(Help(bot))
