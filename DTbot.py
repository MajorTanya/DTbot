import datetime
import logging
from configparser import ConfigParser

import discord
from discord.ext import commands
from mysql.connector import pooling as mariadbpooling

from util.utils import checkdbforuser, dbcallprocedure

intents = discord.Intents.default()
intents.members = True

config = ConfigParser()
config.read('./config/config.ini')
TOKEN = config.get('General', 'TOKEN')

extensions = config.items('Extensions')
startup_extensions = []
for key, ext in extensions:
    startup_extensions.append(ext)

startup_time = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
log_startup_time = startup_time.strftime('%Y-%m-%d (%H-%M-%S %Z)')


class DTbot(commands.Bot):
    def __init__(self, bot_config: ConfigParser | None = None, det_prefixes=None):
        super().__init__(case_insensitive=True, command_prefix=det_prefixes, intents=intents)
        if bot_config:
            self.bot_config = bot_config
        else:
            self.bot_config = ConfigParser()
            self.bot_config.read('./config/config.ini')
        db_config = dict(self.bot_config.items('Database'))
        self.db_cnx = mariadbpooling.MySQLConnectionPool(pool_size=10, pool_reset_session=True, **db_config)
        self.dtbot_colour = discord.Colour(0x5e51a8)
        self.remove_command('help')
        # set up logging and bind to instance
        self.log = logging.getLogger('discord')
        self.log.setLevel(logging.WARNING)
        filehandler = logging.FileHandler(filename=f'./logs/{log_startup_time}.log', encoding='utf-8', mode='w')
        streamhandler = logging.StreamHandler()
        filehandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
        streamhandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
        self.log.addHandler(filehandler)
        self.log.addHandler(streamhandler)

    async def setup_hook(self):
        for extension in startup_extensions:
            try:
                await self.load_extension(extension)
                print(f'Successfully loaded extension {extension}.')
            except Exception as e:
                exc = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exc}.')

    async def on_guild_join(self, guild: discord.Guild):
        dbcallprocedure(self.db_cnx, 'AddNewServer', params=(guild.id, guild.member_count))

    async def on_message(self, message: discord.Message):
        if (message.author == self.user) or message.author.bot:
            return
        try:
            checkdbforuser(self.db_cnx, message)
        finally:
            pass
        pass

    async def on_ready(self):
        # online confimation
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    def run(self, **kwargs):
        super().run(TOKEN, **kwargs)
