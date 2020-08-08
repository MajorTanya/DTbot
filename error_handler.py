import discord
from discord.ext import commands

from launcher import dtbot_colour, logger


class IllegalCustomCommandAccess(commands.CommandError):
    # raised if custom commands are accessed by users in unauthorized servers
    def __init__(self, ctx):
        server = ctx.guild
        user = ctx.message.author
        command = ctx.command
        super().__init__(f"{user} (ID: {user.id}) tried to use \"{command}\" in server \"{server.name}\" "
                         f"(ID: {server.id})")


async def send_cmd_help(bot, ctx, error_msg, delete_after=None):
    bot.help_command.context = ctx
    command = ctx.subcommand if ctx.invoked_subcommand else ctx.command
    usage = bot.help_command.get_command_signature(command=command)
    em = discord.Embed(description=f"{command.description}\n\n{usage.replace('<', '[').replace('>', ']')}",
                       colour=dtbot_colour)
    em.set_footer(text=error_msg)
    await ctx.channel.send(embed=em, delete_after=delete_after)


class ErrorHandler(commands.Cog):
    """Handles and logs DTbot's errors and exceptions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        command = ctx.subcommand if ctx.invoked_subcommand else ctx.command
        if isinstance(error, commands.MissingRequiredArgument):
            await send_cmd_help(self.bot, ctx, f"Error: Missing Required Argument: {' '.join(error.args)}", 15)
        elif isinstance(error, commands.BadArgument):
            await send_cmd_help(self.bot, ctx, f"Error: Bad Argument ({' '.join(error.args)})", 15)
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
        else:
            pass
        logger.error(type(error).__name__)
        logger.error(f"Command '{command}' raised the following error: '{error}'")


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
