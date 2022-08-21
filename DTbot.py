import datetime
import logging
import sys
from configparser import ConfigParser

import discord
from discord import app_commands
from discord.ext import commands
from mysql.connector import pooling as mariadbpooling

from util.utils import checkdbforuser, dbcallprocedure

intents = discord.Intents.default()
intents.members = True


class DTbot(commands.Bot):
    DEV_GUILD: discord.Object = None

    def __init__(self, bot_config: ConfigParser | None = None):
        super().__init__(case_insensitive=True, command_prefix=commands.when_mentioned, intents=intents,
                         help_command=None)
        self.bot_startup = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        if bot_config:
            self.bot_config = bot_config
        else:
            self.bot_config = ConfigParser()
            self.bot_config.read('./config/config.ini')
        DTbot.DEV_GUILD = discord.Object(id=(bot_config.getint('General', 'DEV_GUILD')))
        db_config = dict(self.bot_config.items('Database'))
        self.db_cnx = mariadbpooling.MySQLConnectionPool(pool_size=10, pool_reset_session=True, **db_config)
        self.dtbot_colour = discord.Colour(0x5e51a8)
        # set up logging and bind to instance
        self.log = logging.getLogger('dtbot')
        self.log.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(filename=f'./logs/{self.bot_startup.strftime("%Y-%m-%d (%H-%M-%S %Z)")}.log',
                                           encoding='utf-8', mode='w')
        stream_handler = logging.StreamHandler()
        file_handler.setLevel(logging.INFO)
        stream_handler.setLevel(logging.WARNING)  # will log to syserr, more immediately visible than file
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', '%Y-%m-%d %H:%M:%S', style='{')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)
        self.log.addHandler(stream_handler)

    async def setup_hook(self) -> None:
        await super().setup_hook()
        for _, extension in self.bot_config.items('Extensions'):
            try:
                await self.load_extension(extension)
                self.log.debug(f'Successfully loaded extension {extension}.')
            except Exception as e:
                self.log.error(f'Failed to load extension {extension}\n{type(e).__name__}: {e}.')
        await self.tree.sync(guild=DTbot.DEV_GUILD)
        if '--dev' not in sys.argv:
            await self.tree.sync()

    async def on_guild_join(self, guild: discord.Guild):
        dbcallprocedure(self.db_cnx, 'AddNewServer', params=(guild.id, guild.member_count))

    async def on_message(self, message: discord.Message):
        if (message.author == self.user) or message.author.bot:
            return
        try:
            checkdbforuser(self.db_cnx, message)
        finally:
            pass

    async def on_app_command_completion(self, interaction: discord.Interaction, command: app_commands.Command):
        result = dbcallprocedure(self.db_cnx, 'CheckAppCommandExist', returns=True,
                                 params=(command.qualified_name, '@res'))
        if result:
            dbcallprocedure(self.db_cnx, 'IncrementAppCommandUsage', params=(command.qualified_name,))
        else:
            dbcallprocedure(self.db_cnx, 'AddNewAppCommand', params=(command.qualified_name,))
            # because the command was used this one time, we increment the default value (0) by 1
            dbcallprocedure(self.db_cnx, 'IncrementAppCommandUsage', params=(command.qualified_name,))

    async def on_ready(self):
        # online confimation
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    def run(self, **kwargs):
        super().run(self.bot_config.get('General', 'TOKEN'), log_handler=self.log.handlers[0], **kwargs)
