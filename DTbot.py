import datetime
import logging
from configparser import ConfigParser

import discord
from discord.ext import commands
from pytz import timezone

intents = discord.Intents.default()
intents.members = True

config = ConfigParser()
config.read('./config/config.ini')
TOKEN = config.get('General', 'TOKEN')

extensions = config.items('Extensions')
startup_extensions = []
for key, ext in extensions:
    startup_extensions.append(ext)

ger_tz = timezone(config.get('Heartbeat', 'ger_tz'))
human_startup_time = datetime.datetime.now(ger_tz).strftime('%d-%m-%Y - %H:%M:%S %Z')
log_startup_time = datetime.datetime.now(ger_tz).strftime('%Y-%m-%d (%H-%M-%S %Z)')
startup_time = datetime.datetime.utcnow()


def dtbotinfo(self, msg, *args, **kwargs):
    # custom logging level (less verbose than INFO but not serious enough for WARNING or above)
    if self.isEnabledFor(25):
        self._log(25, msg, args, **kwargs)


class DTbot(commands.Bot):
    def __init__(self, det_prefixes=None):
        super().__init__(case_insensitive=True, command_prefix=det_prefixes, intents=intents)
        self.dtbot_colour = discord.Colour(0x5e51a8)
        self.remove_command('help')
        # set up logging and bind to instance
        self.log = logging.getLogger('discord')
        logging.addLevelName(25, 'DTBOT-INFO')
        self.log.dtbotinfo = dtbotinfo
        self.log.setLevel(25)
        handler = logging.FileHandler(filename=f'./logs/{log_startup_time}.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
        self.log.addHandler(handler)

        for extension in startup_extensions:
            try:
                self.load_extension(extension)
                print(f'Successfully loaded extension {extension}.')
            except Exception as e:
                exc = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exc}.')

    async def on_ready(self):
        # online confimation
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    def run(self):
        super().run(TOKEN)
