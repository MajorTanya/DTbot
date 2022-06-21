import datetime
import logging
from configparser import ConfigParser

import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
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
    def __init__(self, det_prefixes=None):
        super().__init__(case_insensitive=True, command_prefix=det_prefixes, intents=intents,
                         # prevent application command overrides due to this being v2 (classic)
                         rollout_associate_known=False, rollout_delete_unknown=False, rollout_register_new=False,
                         rollout_update_known=False)
        self.dtbot_colour = nextcord.Colour(0x5e51a8)
        self.remove_command('help')
        # set up logging and bind to instance
        self.log = logging.getLogger('nextcord')
        self.log.setLevel(logging.WARNING)
        filehandler = logging.FileHandler(filename=f'./logs/{log_startup_time}.log', encoding='utf-8', mode='w')
        streamhandler = logging.StreamHandler()
        filehandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
        streamhandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
        self.log.addHandler(filehandler)
        self.log.addHandler(streamhandler)

        for extension in startup_extensions:
            try:
                self.load_extension(extension)
                print(f'Successfully loaded extension {extension}.')
            except Exception as e:
                exc = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exc}.')

    # Prevent nextcord's attempts at using Slash Commands (this is v2 (classic), traditional commands only mode)

    async def on_connect(self) -> None:
        pass

    async def on_guild_available(self, guild: nextcord.Guild) -> None:
        pass

    async def on_interaction(self, interaction: nextcord.Interaction):
        pass

    async def on_ready(self):
        # online confimation
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    def run(self):
        super().run(TOKEN)
