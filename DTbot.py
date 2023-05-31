import datetime
import logging
import os
import sys
from configparser import ConfigParser

import discord
import mariadb
from discord import app_commands
from discord.ext import commands

from util.database_utils import DBProcedure, checkdbforuser, dbcallprocedure
from util.utils import add_file_logging, add_stream_logging

intents = discord.Intents.default()
intents.members = True


class DTbot(commands.Bot):
    DEV_GUILD: discord.Object = None
    DTBOT_COLOUR: discord.Colour = discord.Colour(0x5E51A8)

    def __init__(self, bot_config: ConfigParser | None = None):
        super().__init__(
            case_insensitive=True,
            command_prefix=commands.when_mentioned,
            intents=intents,
            help_command=None,
        )
        self.bot_startup = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        self.db_cnx: mariadb.ConnectionPool = None  # type: ignore # this is set properly during setup_hook
        if bot_config:
            self.bot_config = bot_config
        else:
            self.bot_config = ConfigParser()
            self.bot_config.read("./config/config.ini")
        DTbot.DEV_GUILD = discord.Object(id=(self.bot_config.getint("General", "DEV_GUILD")))
        # set up logging and bind to instance
        self.log = logging.getLogger("dtbot")
        self.log.setLevel(logging.DEBUG)
        self._file_handler: logging.FileHandler = discord.utils.MISSING
        if not self.in_dev_mode:
            self._file_handler = add_file_logging(self.log, logs_folder="./logs", startup_time=self.bot_startup)
            add_stream_logging(self.log)
        else:
            add_stream_logging(self.log, level=logging.DEBUG, stream=sys.stdout)

    @property
    def in_dev_mode(self) -> bool:
        return "--dev" in sys.argv

    async def setup_hook(self) -> None:
        db_config = dict(self.bot_config.items("Database"))
        self.db_cnx = mariadb.ConnectionPool(
            pool_size=10,
            reconnect=True,
            user=os.environ.get("DTBOT_DB_USER"),
            password=os.environ.get("DTBOT_DB_PASS"),
            **db_config,
        )

        for _, extension in self.bot_config.items("Extensions"):
            try:
                await self.load_extension(extension)
                self.log.debug(f"Successfully loaded extension {extension}.")
            except Exception as e:
                self.log.error(f"Failed to load extension {extension}\n{type(e).__name__}: {e}.")
        await self.tree.sync(guild=DTbot.DEV_GUILD)
        if not self.in_dev_mode:
            await self.tree.sync()

    async def on_guild_join(self, guild: discord.Guild):
        dbcallprocedure(self.db_cnx, DBProcedure.AddNewServer, params=(guild.id, guild.member_count))

    async def on_message(self, message: discord.Message):
        if (message.author == self.user) or message.author.bot:
            return
        try:
            checkdbforuser(self.db_cnx, message)
        finally:
            pass

    async def on_app_command_completion(self, _: discord.Interaction, command: app_commands.Command):
        result = dbcallprocedure(self.db_cnx, DBProcedure.CheckAppCommandExist, params=(command.qualified_name,))
        if result:
            dbcallprocedure(self.db_cnx, DBProcedure.IncrementAppCommandUsage, params=(command.qualified_name,))
        else:
            dbcallprocedure(self.db_cnx, DBProcedure.AddNewAppCommand, params=(command.qualified_name,))
            # because the command was used this one time, we increment the default value (0) by 1
            dbcallprocedure(self.db_cnx, DBProcedure.IncrementAppCommandUsage, params=(command.qualified_name,))

    async def on_ready(self):
        # online confimation
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

    def run(self, **kwargs):
        super().run(os.environ.get("DTBOT_TOKEN"), log_handler=self._file_handler, **kwargs)
