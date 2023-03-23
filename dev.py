import datetime
import sys
from asyncio import sleep
from configparser import ConfigParser

import discord
from discord import app_commands
from discord.ext import commands, tasks

from DTbot import DTbot
from util.database_utils import DBProcedure, dbcallprocedure


@app_commands.guilds(DTbot.DEV_GUILD)
class Dev(commands.GroupCog):
    """Developer Commands and DTbot Management"""

    HB_FREQ: float = 60

    def __init__(self, bot: DTbot):
        self.bot = bot
        Dev.HB_FREQ = self.bot.bot_config.getint("Heartbeat", "hb_freq")
        self.H_CODE = self.bot.bot_config.get("Developers", "h_code")
        self.SDB_CODE = self.bot.bot_config.get("Developers", "sdb_code")
        self.hb_chamber: discord.TextChannel | None = None
        if "--no-heartbeat" not in sys.argv:
            # run "python launcher.py --no-heartbeat" to start DTbot without the heartbeat messages
            # If not provided, run with a heartbeat
            self.heartbeat.start()

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        bot: DTbot = interaction.client  # type: ignore
        return await bot.is_owner(interaction.user)

    async def cog_unload(self):
        try:
            self.heartbeat.stop()
        except:
            pass

    @tasks.loop(seconds=HB_FREQ)
    async def heartbeat(self):
        if not self.bot.is_closed():
            now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
            now_ts = int(now_dt.timestamp())
            startup_ts = int(self.bot.bot_startup.timestamp())
            uptime = now_dt - self.bot.bot_startup
            dtbot_version = self.bot.bot_config.get("Info", "dtbot_version")
            beat_embed = discord.Embed(
                colour=DTbot.DTBOT_COLOUR,
                title=f"{self.bot.user.name}'s Heartbeat",
                description=f"{self.bot.user.name} is still alive and running!",
            )
            beat_embed.add_field(name="Startup time:", value=f"<t:{startup_ts}:D> - <t:{startup_ts}:T>")
            beat_embed.add_field(name="Time now:", value=f"<t:{now_ts}:D> - <t:{now_ts}:T>", inline=False)
            beat_embed.add_field(name="Uptime:", value=uptime)
            beat_embed.set_footer(text=f"DTbot v. {dtbot_version}")
            msg: discord.Message = await self.hb_chamber.send(embed=beat_embed)
            await msg.delete(delay=Dev.HB_FREQ)

    @heartbeat.before_loop
    async def before_heartbeat(self):
        await self.bot.wait_until_ready()
        self.heartbeat.change_interval(seconds=Dev.HB_FREQ)  # apply the config value
        startup_ts = int(self.bot.bot_startup.timestamp())
        self.hb_chamber = self.bot.get_channel(self.bot.bot_config.getint("Heartbeat", "hb_chamber"))
        startup_embed = discord.Embed(
            colour=DTbot.DTBOT_COLOUR,
            title=f"{self.bot.user.name}'s Heartbeat",
            description=f"{self.bot.user.name} is starting up!",
        )
        startup_embed.add_field(name="Startup time:", value=f"<t:{startup_ts}:D> - <t:{startup_ts}:T>")
        await self.hb_chamber.send(embed=startup_embed)

    @commands.Cog.listener()
    async def on_ready(self):
        dtbot_version = self.bot.bot_config.get("Info", "dtbot_version")
        await self.bot.change_presence(activity=discord.Game(name=f"Check /announcements (v. {dtbot_version})"))

    heart = app_commands.Group(name="heart", description="Manages the heartbeat of DTbot.")

    @heart.command(description="Stops the heartbeat of DTbot.")
    async def stop(self, interaction: discord.Interaction, code: str):
        await interaction.response.defer(ephemeral=True)
        if code == self.H_CODE:
            self.heartbeat.stop()
            self.bot.log.info(f"Heartbeat stopped by user {interaction.user}.")
            await interaction.followup.send(f"Heartbeat stopped by user {interaction.user}.", ephemeral=True)
        else:
            await interaction.followup.send(f"Invalid code.", ephemeral=True)

    @heart.command(description="Starts the heartbeat of DTbot.")
    async def start(self, interaction: discord.Interaction, code: str):
        await interaction.response.defer(ephemeral=True)
        if code == self.H_CODE:
            self.heartbeat.restart() if self.heartbeat.is_running() else self.heartbeat.start()
            self.bot.log.info(f"Heartbeat started by user {interaction.user}.")
            await interaction.followup.send(f"Heartbeat started by user {interaction.user}.", ephemeral=True)
        else:
            await interaction.followup.send(f"Invalid code.", ephemeral=True)

    @app_commands.command(description="Load an extension. Optionally syncs Slash Commands.")
    async def load(
        self,
        interaction: discord.Interaction,
        extension_name: str,
        dev_sync: bool | None = False,
        global_sync: bool | None = False,
    ):
        await interaction.response.defer(ephemeral=True)
        try:
            await self.bot.load_extension(extension_name)
            await self.sync(dev_sync=dev_sync, global_sync=global_sync)
            self.bot.log.info(f"Module `{extension_name}` loaded by user {interaction.user}.")
            await interaction.followup.send(f"Module `{extension_name}` loaded successfully.")
        except commands.ExtensionError as e:
            self.bot.log.error(f"Error loading Module {extension_name}:", exc_info=e)
            await interaction.followup.send(f"{type(e).__name__}", ephemeral=True)

    @load.autocomplete("extension_name")
    async def load_autocomplete(self, _interaction: discord.Interaction, current: str):
        loaded = [cog.__class__.__name__.lower() for cog in self.bot.cogs.values()]
        not_loaded = [cog for key, cog in self.bot.bot_config.items("Extensions") if key.lower() not in loaded]
        return [
            app_commands.Choice(name=cog.title().replace("Rng", "RNG"), value=cog)
            for cog in not_loaded
            if current.lower() in cog.lower()
        ]

    @app_commands.command(description="Unload an extension. Optionally syncs Slash Commands.")
    async def unload(
        self,
        interaction: discord.Interaction,
        extension_name: str,
        dev_sync: bool | None = False,
        global_sync: bool | None = False,
    ):
        await interaction.response.defer(ephemeral=True)
        try:
            await self.bot.unload_extension(extension_name)
            await self.sync(dev_sync=dev_sync, global_sync=global_sync)
            self.bot.log.info(f"Module `{extension_name}` unloaded by user {interaction.user}.")
            await interaction.followup.send(f"Module `{extension_name}` unloaded successfully.")
        except commands.ExtensionError as e:
            self.bot.log.error(f"Error unloading Module {extension_name}:", exc_info=e)
            await interaction.followup.send(f"{type(e).__name__}", ephemeral=True)

    @app_commands.command(description="Atomically reload an extension. Optionally syncs Slash Commands.")
    async def reload(
        self,
        interaction: discord.Interaction,
        extension_name: str,
        dev_sync: bool | None = False,
        global_sync: bool | None = False,
    ):
        await interaction.response.defer(ephemeral=True)
        try:
            await self.bot.reload_extension(extension_name)
            await self.sync(dev_sync=dev_sync, global_sync=global_sync)
            self.bot.log.info(f"Module `{extension_name}` reloaded by user {interaction.user}.")
            await interaction.followup.send(f"Module `{extension_name}` reloaded successfully.")
        except commands.ExtensionError as e:
            self.bot.log.error(f"Error reloading Module {extension_name}:", exc_info=e)
            await interaction.followup.send(f"{type(e).__name__}", ephemeral=True)

    @unload.autocomplete("extension_name")
    @reload.autocomplete("extension_name")
    async def unreload_autocomplete(self, _interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(
                name=cog.qualified_name,
                value=cog.__class__.__name__.lower()
                .replace("databasemanagement", "database_management")
                .replace("errorhandler", "error_handler"),
            )
            for cog in (self.bot.cogs.values())
            if current.lower() in cog.__class__.__name__.lower()
        ]

    @app_commands.command(description="Update / Refresh DTbot's Rich Presence. No Syncing.")
    async def updaterp(self, interaction: discord.Interaction, caption: str | None, reload_config: bool | None = False):
        await interaction.response.defer(ephemeral=True)
        dtbot_version = self.bot.bot_config.get("Info", "dtbot_version")
        if reload_config:
            self.bot.bot_config = ConfigParser()
            self.bot.bot_config.read("./config/config.ini")
            dtbot_version = self.bot.bot_config.get("Info", "dtbot_version")
            self.bot.log.info(f"{interaction.user} reloaded DTbot config successfully.")
        if caption:
            caption = caption.replace("DTbot", "@\u200bDTbot").replace("dtbot_version", dtbot_version)
        else:
            caption = f"Check /announcements (v. {dtbot_version})"
        self.bot.log.info("Updating Rich Presence")
        await self.bot.change_presence(activity=discord.Game(name=caption))
        self.bot.log.info(f"{self.bot.user.name}'s Rich Presence was updated to '{caption}' by {interaction.user}")
        await interaction.followup.send(f"Successfully updated Rich Presence to: {caption}", ephemeral=True)

    @app_commands.command(description="Shutdown command for DTbot.")
    async def shutdownbot(self, interaction: discord.Interaction, passcode: str):
        await interaction.response.defer(ephemeral=True)
        if passcode == self.SDB_CODE:
            try:
                self.heartbeat.stop()
            except:
                pass
            await interaction.followup.send("Shutting down...", ephemeral=True)
            await sleep(1)  # race condition can cause the bot to close before it reponds, a short wait prevents this
            await self.bot.close()
        else:
            await interaction.followup.send("No.", ephemeral=True)

    @app_commands.command(description="Manually cycles through all servers to refresh the database.")
    async def refreshservers(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        for guild in self.bot.guilds:
            dbcallprocedure(self.bot.db_cnx, DBProcedure.AddNewServer, params=(guild.id, guild.member_count))
        await interaction.followup.send("Server list refreshed", ephemeral=True)

    async def sync(self, *, dev_sync: bool = False, global_sync: bool = False):
        if dev_sync:
            await self.bot.tree.sync(guild=DTbot.DEV_GUILD)
        if global_sync:
            await self.bot.tree.sync()


async def setup(bot: DTbot):
    await bot.add_cog(Dev(bot), guild=DTbot.DEV_GUILD)
