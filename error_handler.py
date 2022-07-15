import discord
from discord import app_commands
from discord.ext import commands

from DTbot import DTbot


class AniMangaLookupError(app_commands.AppCommandError):
    # raised if something went wrong with the anime/manga lookup with the AL API
    def __init__(self, *, title: str):
        self.title = title
        super().__init__(f"Something went wrong when looking up \"{title}\" on AniList.")


class ErrorHandler(commands.Cog):
    """Handles and logs DTbot's errors and exceptions"""

    def __init__(self, bot: DTbot):
        self.bot = bot
        self.PERMSEXPL = self.bot.bot_config.get('General', 'PERMSEXPL')
        self._std_on_error = self.bot.tree.on_error
        self.bot.tree.on_error = self.on_app_command_error

    async def cog_unload(self):
        self.bot.tree.on_error = self._std_on_error

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        send = interaction.response.send_message if not interaction.response.is_done() else interaction.followup.send
        command = interaction.command.qualified_name
        if isinstance(error, app_commands.BotMissingPermissions):
            await send(f"`Error: {error.args[0].replace('Bot', 'DTbot').replace('this command', 'properly')}` "
                       f"Please make sure that the missing permissions are granted to the bot. (You can read about "
                       f"why DTbot needs these permissions [here]({self.PERMSEXPL}))")
        elif isinstance(error, app_commands.CommandOnCooldown):
            await send(f"_This command is currently on cooldown. Try again in `{error.retry_after:.0f}` seconds._",
                       ephemeral=True)
        elif type(error).__name__ == AniMangaLookupError.__name__:
            # Something goes wrong with isinstance here, this is the best workaround
            error: AniMangaLookupError = error  # type: ignore
            await send(f"Couldn't find \"{error.title}\" on AniList.")
        else:
            self.bot.log.error(type(error).__name__)
            self.bot.log.error(f"Command '{command}' raised the following error: '{error}'")


async def setup(bot: DTbot):
    await bot.add_cog(ErrorHandler(bot))
