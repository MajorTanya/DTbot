from configparser import ConfigParser
from datetime import datetime
from logging import Logger
from typing import Any, override

import discord
import mariadb
from discord import app_commands
from discord.ext import commands

from util.database_utils import DBProcedure, checkdbforuser, dbcallprocedure

intents = discord.Intents.default()
intents.members = True


class DTbot(commands.Bot):
    DEV_GUILD: discord.Object = None  # type: ignore
    DTBOT_COLOUR: discord.Colour = discord.Colour(0x5E51A8)

    def __init__(
        self,
        *,
        bot_config: ConfigParser,
        db_connection_pool: mariadb.ConnectionPool,
        dtbot_version: str,
        in_dev_mode: bool,
        logger: Logger,
        startup_time: datetime,
    ):
        super().__init__(
            case_insensitive=True,
            command_prefix=commands.when_mentioned,
            intents=intents,
            help_command=None,
        )
        self._in_dev_mode = in_dev_mode
        self.bot_config = bot_config
        DTbot.DEV_GUILD = discord.Object(id=(self.bot_config.getint("General", "DEV_GUILD")))
        self.bot_startup = startup_time
        self.db_cnx = db_connection_pool
        self.dtbot_version = dtbot_version
        self.log = logger

    @override
    async def setup_hook(self):
        for _, extension in self.bot_config.items("Extensions"):
            try:
                await self.load_extension(extension)
                self.log.debug(f"Successfully loaded extension {extension}.")
            except Exception as e:
                self.log.error(f"Failed to load extension {extension}\n{type(e).__name__}: {e}.")
        if not self._in_dev_mode:
            await self.tree.sync(guild=DTbot.DEV_GUILD)
            await self.tree.sync()

    async def on_guild_join(self, guild: discord.Guild):
        dbcallprocedure(self.db_cnx, DBProcedure.AddNewServer, params=(guild.id, guild.member_count))

    @override
    async def on_message(self, message: discord.Message):
        if (message.author == self.user) or message.author.bot:
            return

        checkdbforuser(self.db_cnx, message)

    async def on_app_command_completion(
        self,
        _: discord.Interaction[discord.Client],
        command: app_commands.Command[Any, ..., Any],
    ):
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
        print(self.user.name)  # type: ignore
        print(self.user.id)  # type: ignore
        print("------")
