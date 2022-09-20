from __future__ import annotations

import datetime
import logging
from configparser import ConfigParser

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True


class DTbot(commands.Bot):
    def __init__(self, bot_config: ConfigParser | None = None):
        super().__init__(case_insensitive=True, command_prefix=commands.when_mentioned, intents=intents)
        self.bot_startup = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        if bot_config:
            self.bot_config = bot_config
        else:
            self.bot_config = ConfigParser()
            self.bot_config.read('./config/config.ini')
        self.dtbot_colour = discord.Colour(0x5e51a8)
        self.remove_command('help')
        # set up logging and bind to instance
        self.log = logging.getLogger('discord')
        self.log.setLevel(logging.WARNING)
        log_startup_time = self.bot_startup.strftime('%Y-%m-%d (%H-%M-%S %Z)')
        filehandler = logging.FileHandler(filename=f'./logs/{log_startup_time}.log', encoding='utf-8', mode='w')
        streamhandler = logging.StreamHandler()
        filehandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
        streamhandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
        self.log.addHandler(filehandler)
        self.log.addHandler(streamhandler)

    async def setup_hook(self):
        for _, extension in self.bot_config.items('Extensions'):
            try:
                await self.load_extension(extension)
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

    def run(self, **kwargs):
        super().run(self.bot_config.get('General', 'TOKEN'), log_handler=None)
