import datetime
import sys
from configparser import ConfigParser

import nextcord
from nextcord import Game
from nextcord.ext import commands, tasks

from DTbot import config, startup_time

dtbot_version = config.get('Info', 'dtbot_version')
last_updated = config.get('Info', 'last_updated')
h_code = config.get('Developers', 'h_code')
hb_freq = config.getint('Heartbeat', 'hb_freq')
sdb_code = config.get('Developers', 'sdb_code')


class Dev(commands.Cog, command_attrs=dict(hidden=True)):
    """Developer Commands and DTbot Management"""

    def __init__(self, bot):
        self.bot = bot
        self.hb_chamber = None
        if len(sys.argv) < 2 or sys.argv[1] == '1':
            # run "python launcher.py 1" to start DTbot with a heartbeat message, 0 if not
            # if no parameter is provided, defaults to run with a heartbeat
            self.heartbeat.start()

    def cog_unload(self):
        try:
            self.heartbeat.stop()
        except:
            pass

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.message.author)

    @tasks.loop(seconds=hb_freq)
    async def heartbeat(self):
        if not self.bot.is_closed():
            now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
            now_ts = int(now_dt.timestamp())
            startup_ts = int(startup_time.timestamp())
            uptime = now_dt - startup_time
            beat_embed = nextcord.Embed(colour=self.bot.dtbot_colour, title=f"{self.bot.user.name}'s Heartbeat",
                                        description=f"{self.bot.user.name} is still alive and running!")
            beat_embed.add_field(name="Startup time:", value=f"<t:{startup_ts}:D> - <t:{startup_ts}:T>")
            beat_embed.add_field(name="Time now:", value=f"<t:{now_ts}:D> - <t:{now_ts}:T>", inline=False)
            beat_embed.add_field(name="Uptime:", value=uptime)
            beat_embed.set_footer(text=f"DTbot v. {dtbot_version}")
            await self.hb_chamber.send(embed=beat_embed, delete_after=hb_freq)

    @heartbeat.before_loop
    async def before_heartbeat(self):
        await self.bot.wait_until_ready()
        startup_ts = int(startup_time.timestamp())
        self.hb_chamber = self.bot.get_channel(config.getint('Heartbeat', 'hb_chamber'))
        startup_embed = nextcord.Embed(colour=self.bot.dtbot_colour, title=f"{self.bot.user.name}'s Heartbeat",
                                       description=f"{self.bot.user.name} is starting up!")
        startup_embed.add_field(name="Startup time:", value=f"<t:{startup_ts}:D> - <t:{startup_ts}:T>")
        await self.hb_chamber.send(embed=startup_embed)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=Game(name=f"Do @\u200bDTbot help (v. {dtbot_version})"))

    @commands.group(description="Manages the heartbeat of DTbot. Developers only.")
    async def heart(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @heart.command(description="Stops the heartbeat of DTbot. Developers only.")
    async def stop(self, ctx, code=None):
        if code == h_code:
            self.heartbeat.stop()
            self.bot.log.dtbotinfo(self.bot.log, f'Heartbeat stopped by user {ctx.author}.')
            await ctx.send(f'Heartbeat stopped by user {ctx.author}.')

    @heart.command(description="Starts the heartbeat of DTbot. Developers only.")
    async def start(self, ctx, code=None):
        if code == h_code:
            self.heartbeat.restart() if self.heartbeat.is_running() else self.heartbeat.start()
            self.bot.log.dtbotinfo(self.bot.log, f'Heartbeat started by user {ctx.author}.')
            await ctx.send(f'Heartbeat started by user {ctx.author}.')

    @commands.command(description="Can load additional extensions into DTbot. Developers only.",
                      brief="Load an extension. Developers only.")
    async def load(self, ctx, extension_name: str):
        self.bot.load_extension(extension_name)
        self.bot.log.dtbotinfo(self.bot.log, f"Module `{extension_name}` loaded by user {ctx.author}.")
        await ctx.send(f"Module `{extension_name}` loaded successfully.")

    @commands.command(description="Unload an extension. Developers only.",
                      brief="Unload an extension. Developers only.")
    async def unload(self, ctx, extension_name: str):
        self.bot.unload_extension(extension_name)
        self.bot.log.dtbotinfo(self.bot.log, f"Module `{extension_name}` unloaded by user {ctx.author}.")
        await ctx.send(f"Module `{extension_name}` unloaded successfully.")

    @commands.command(description="First unload and then immediately reload a module. Developers only.",
                      brief="Reload an extension. Developers only.")
    async def reload(self, ctx, extension_name: str):
        self.bot.reload_extension(extension_name)
        self.bot.log.dtbotinfo(self.bot.log, f"Module `{extension_name}` reloaded by user {ctx.author}.")
        await ctx.send(f"Module `{extension_name}` reloaded successfully.")

    @commands.command(description="Update / Refresh DTbot's Rich Presence. Developers only.",
                      brief="Update DTbot's Rich Presence. Developers only.")
    async def updaterp(self, ctx, *caption: str):
        if caption:
            caption = " ".join(caption)
            caption = caption.replace("DTbot", "@\u200bDTbot")
            caption = caption.replace("dtbot_version", dtbot_version)
        else:
            caption = f"Do @\u200bDTbot help (v. {dtbot_version})"
        await self.bot.change_presence(activity=Game(name=caption))
        self.bot.log.dtbotinfo(self.bot.log,
                               f"{self.bot.user.name}'s Rich Presence was updated to '{caption}' by {ctx.author}")
        await ctx.send("Rich Presence updated.")

    @commands.command(description='Refresh the version number and date of last update from the config.'
                                  '\nCalls `updaterp Do DTbot (v. dtbot_version)` to update the Rich Presence.'
                                  '\nCalls `reload general` to update the use of the version'
                                  'and date in the `info` and `changelog` commands.\nDevelopers only.',
                      brief='Refresh the version and date of the last update. Developers only.')
    async def updatever(self, ctx):
        global dtbot_version, last_updated
        refreshed_config = ConfigParser()
        refreshed_config.read('./config/config.ini')
        dtbot_version = refreshed_config.get('Info', 'dtbot_version')
        last_updated = refreshed_config.get('Info', 'last_updated')
        config.set('Info', 'dtbot_version', dtbot_version)
        config.set('Info', 'last_updated', last_updated)
        self.bot.log.dtbotinfo(self.bot.log, f"{ctx.author} refreshed dtbot_version and last_update.")
        self.bot.log.dtbotinfo(self.bot.log, "Updating Rich Presence and reloading General...")
        await ctx.invoke(self.bot.get_command('updaterp'), 'Do DTbot help (v. dtbot_version)')
        await ctx.invoke(self.bot.get_command('reload'), extension_name='general')

    @commands.command(description='Shutdown command for the bot. Developers only.',
                      brief='Shut the bot down. Developers only.')
    async def shutdownbot(self, ctx, passcode: str):
        if passcode == sdb_code:
            try:
                self.heartbeat.stop()
            except:
                pass
            await self.bot.close()
        else:
            return


def setup(bot):
    bot.add_cog(Dev(bot))
