import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure


class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, error, ctx):
        channel = ctx.message.channel
        if isinstance(error, commands.MissingRequiredArgument):
            await self.send_cmd_help(ctx, "Error: Missing Required Argument: " + "{}".format(' '.join(error.args)))
        elif isinstance(error, commands.BadArgument):
            await self.send_cmd_help(ctx, "Error: Bad Argument")
        elif isinstance(error, commands.CommandOnCooldown):
            await self.bot.send_message(channel, f"_This command is currently on cooldown. Try again in `{error.retry_after:.0f}` seconds._")
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, CheckFailure):
            await self.bot.send_message(channel, "`Error: You don't have the required permissions to use this command.`")
        else:
            print(error)

    async def send_cmd_help(self, ctx, error_msg):
        if ctx.invoked_subcommand:
            command = ctx.subcommand
        else:
            command = ctx.command
        pages = self.bot.formatter.format_help_for(ctx, command)
        for page in pages:
            em = discord.Embed(description=page.strip("```").replace('<', '[').replace('>', ']'),
                               colour=discord.Colour(0x5e51a8))
            em.set_footer(text=error_msg)
            await self.bot.send_message(ctx.message.channel, embed=em)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
