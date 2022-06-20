import nextcord
from nextcord.ext import commands

from DTbot import DTbot


class AniMangaLookupError(commands.CommandError):
    # raised if something went wrong with the anime/manga lookup with the AL API
    def __init__(self, *, title, status_code, manga: bool):
        self.title = title
        self.status_code = status_code
        self.isManga = manga
        self.type = 'a Manga' if self.isManga else 'an Anime'
        super().__init__(f"Something went wrong when looking up \"{title}\" on AniList.")


class IllegalCustomCommandAccess(commands.CommandError):
    # raised if custom commands are accessed by users in unauthorized servers
    def __init__(self, ctx):
        server = ctx.guild
        user = ctx.message.author
        command = ctx.command
        super().__init__(f"{user} (ID: {user.id}) tried to use \"{command}\" in server \"{server.name}\" "
                         f"(ID: {server.id})")


async def send_cmd_help(bot, ctx, error_msg, delete_after=None, plain=False):
    bot.help_command.context = ctx
    command = ctx.subcommand if ctx.invoked_subcommand else ctx.command
    usage = bot.help_command.get_command_signature(command=command)
    if not plain:
        em = nextcord.Embed(description=f"{command.description}\n\n{usage.replace('<', '[').replace('>', ']')}",
                            colour=bot.dtbot_colour)
        em.set_footer(text=error_msg)
        await ctx.channel.send(embed=em, delete_after=delete_after)
    else:
        await ctx.channel.send(
                f"```{command.description}\n\n{usage.replace('<', '[').replace('>', ']')}\n\n{error_msg}```")


class ErrorHandler(commands.Cog):
    """Handles and logs DTbot's errors and exceptions"""

    def __init__(self, bot: DTbot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        command = ctx.subcommand if ctx.invoked_subcommand else ctx.command
        if isinstance(error, commands.MissingRequiredArgument):
            try:
                await send_cmd_help(self.bot, ctx, f"Error: Missing Required Argument: {' '.join(error.args)}", 15)
            except nextcord.Forbidden:
                await send_cmd_help(self.bot, ctx, f"Error: Missing Required Argument: {' '.join(error.args)}",
                                    15, plain=True)
        elif isinstance(error, commands.BadArgument):
            try:
                await send_cmd_help(self.bot, ctx, f"Error: Bad Argument ({' '.join(error.args)})", 15)
            except nextcord.Forbidden:
                await send_cmd_help(self.bot, ctx, f"Error: Bad Argument ({' '.join(error.args)})", 15, plain=True)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"_This command is currently on cooldown. Try again in `{error.retry_after:.0f}` seconds._",
                           delete_after=15)
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CheckFailure):
            if isinstance(error, commands.BotMissingPermissions):
                await ctx.send(f"`Error: {error.args[0].replace('Bot', 'DTbot').replace('this command', 'properly')} "
                               f"Please make sure that the missing permissions are granted to the bot.`",
                               delete_after=30)
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send(f"`Error: {error.args[0]}`", delete_after=15)
        elif isinstance(error, IllegalCustomCommandAccess):
            pass
        elif isinstance(error, AniMangaLookupError):
            await ctx.send(f"`Error: Something went wrong when looking up \"{error.title}\" on AniList.`\nCheck your "
                           f"request for typos and make sure that you are looking up {error.type} with the correct "
                           f"command.\nRemember that DTbot doesn't return NSFW results.\nSometimes, AniList doesn't "
                           f"recognize alternative titles or acronyms. Please try again with e.g. a different name "
                           f"for \"{error.title}\".")
            self.bot.log.error(type(error).__name__)
            self.bot.log.error(f'HTML Status Code for the error below: {error.status_code}')
        else:
            pass
        self.bot.log.error(type(error).__name__)
        self.bot.log.error(f"Command '{command}' raised the following error: '{error}'")


def setup(bot: DTbot):
    bot.add_cog(ErrorHandler(bot))
