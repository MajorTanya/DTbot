from configparser import ConfigParser

from discord.ext import commands

config = ConfigParser()
config.read('./config/config.ini')
TOKEN = config.get('General', 'TOKEN')

extensions = config.items('Extensions')
startup_extensions = []
for key, ext in extensions:
    startup_extensions.append(ext)


class DTbot(commands.Bot):
    def __init__(self, det_prefixes=None):
        super().__init__(command_prefix=det_prefixes, case_insensitive=True)
        self.remove_command('help')

        for extension in startup_extensions:
            try:
                self.load_extension(extension)
                print(f'Successfully loaded extension {extension}.')
            except Exception as e:
                exc = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exc}.')

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_ready(self):
        # online confimation
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    def run(self):
        super().run(TOKEN)
