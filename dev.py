from __future__ import annotations

import datetime
import sys
from configparser import ConfigParser

import discord
from discord import Game
from discord.ext import commands, tasks

from DTbot import DTbot


class Dev(commands.Cog, command_attrs=dict(hidden=True)):
    """Developer Commands and DTbot Management"""

    HB_FREQ: float = 60

    def __init__(self, bot: DTbot):
        self.bot = bot
        Dev.HB_FREQ = self.bot.bot_config.getint('Heartbeat', 'hb_freq')
        self.H_CODE = self.bot.bot_config.get('Developers', 'h_code')
        self.SDB_CODE = self.bot.bot_config.get('Developers', 'sdb_code')
        self.hb_chamber: discord.TextChannel | None = None
        if len(sys.argv) < 2 or sys.argv[1] == '1':
            # run "python launcher.py 1" to start DTbot with a heartbeat message, 0 if not
            # if no parameter is provided, defaults to run with a heartbeat
            self.heartbeat.start()

    def cog_unload(self):
        try:
            self.heartbeat.stop()
        except:
            pass

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.message.author)

    @tasks.loop(seconds=HB_FREQ)
    async def heartbeat(self):
        if not self.bot.is_closed():
            now_dt = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
            now_ts = int(now_dt.timestamp())
            startup_ts = int(self.bot.bot_startup.timestamp())
            uptime = now_dt - self.bot.bot_startup
            dtbot_version = self.bot.bot_config.get('Info', 'dtbot_version')
            beat_embed = discord.Embed(colour=self.bot.dtbot_colour, title=f"{self.bot.user.name}'s Heartbeat",
                                       description=f"{self.bot.user.name} is still alive and running!")
            beat_embed.add_field(name="Startup time:", value=f"<t:{startup_ts}:D> - <t:{startup_ts}:T>")
            beat_embed.add_field(name="Time now:", value=f"<t:{now_ts}:D> - <t:{now_ts}:T>", inline=False)
            beat_embed.add_field(name="Uptime:", value=uptime)
            beat_embed.set_footer(text=f"DTbot v. {dtbot_version}")
            await self.hb_chamber.send(embed=beat_embed, delete_after=Dev.HB_FREQ)

    @heartbeat.before_loop
    async def before_heartbeat(self):
        await self.bot.wait_until_ready()
        self.heartbeat.change_interval(seconds=Dev.HB_FREQ)  # apply the config value
        startup_ts = int(self.bot.bot_startup.timestamp())
        self.hb_chamber = self.bot.get_channel(self.bot.bot_config.getint('Heartbeat', 'hb_chamber'))
        startup_embed = discord.Embed(colour=self.bot.dtbot_colour, title=f"{self.bot.user.name}'s Heartbeat",
                                      description=f"{self.bot.user.name} is starting up!")
        startup_embed.add_field(name="Startup time:", value=f"<t:{startup_ts}:D> - <t:{startup_ts}:T>")
        await self.hb_chamber.send(embed=startup_embed)

    @commands.Cog.listener()
    async def on_ready(self):
        dtbot_version = self.bot.bot_config.get('Info', 'dtbot_version')
        await self.bot.change_presence(activity=Game(name=f"Do @\u200bDTbot help (v. {dtbot_version})"))

    @commands.group(description="Manages the heartbeat of DTbot. Developers only.")
    async def heart(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            pass

    @heart.command(description="Stops the heartbeat of DTbot. Developers only.")
    async def stop(self, ctx: commands.Context, code=None):
        if code == self.H_CODE:
            self.heartbeat.stop()
            self.bot.log.info(f'Heartbeat stopped by user {ctx.author}.')
            await ctx.send(f'Heartbeat stopped by user {ctx.author}.')

    @heart.command(description="Starts the heartbeat of DTbot. Developers only.")
    async def start(self, ctx: commands.Context, code=None):
        if code == self.H_CODE:
            self.heartbeat.restart() if self.heartbeat.is_running() else self.heartbeat.start()
            self.bot.log.info(f'Heartbeat started by user {ctx.author}.')
            await ctx.send(f'Heartbeat started by user {ctx.author}.')

    @commands.command(description="Can load additional extensions into DTbot. Developers only.",
                      brief="Load an extension. Developers only.")
    async def load(self, ctx: commands.Context, extension_name: str):
        await self.bot.load_extension(extension_name)
        self.bot.log.info(f"Module `{extension_name}` loaded by user {ctx.author}.")
        await ctx.send(f"Module `{extension_name}` loaded successfully.")

    @commands.command(description="Unload an extension. Developers only.",
                      brief="Unload an extension. Developers only.")
    async def unload(self, ctx: commands.Context, extension_name: str):
        await self.bot.unload_extension(extension_name)
        self.bot.log.info(f"Module `{extension_name}` unloaded by user {ctx.author}.")
        await ctx.send(f"Module `{extension_name}` unloaded successfully.")

    @commands.command(description="First unload and then immediately reload a module. Developers only.",
                      brief="Reload an extension. Developers only.")
    async def reload(self, ctx: commands.Context, extension_name: str):
        await self.bot.reload_extension(extension_name)
        self.bot.log.info(f"Module `{extension_name}` reloaded by user {ctx.author}.")
        await ctx.send(f"Module `{extension_name}` reloaded successfully.")

    @commands.command(description="Update / Refresh DTbot's Rich Presence. Developers only.",
                      brief="Update DTbot's Rich Presence. Developers only.")
    async def updaterp(self, ctx: commands.Context, *caption: str):
        dtbot_version = self.bot.bot_config.get('Info', 'dtbot_version')
        if caption:
            caption = " ".join(caption)
            caption = caption.replace("DTbot", "@\u200bDTbot")
            caption = caption.replace("dtbot_version", dtbot_version)
        else:
            caption = f"Do @\u200bDTbot help (v. {dtbot_version})"
        await self.bot.change_presence(activity=Game(name=caption))
        self.bot.log.info(f"{self.bot.user.name}'s Rich Presence was updated to '{caption}' by {ctx.author}")
        await ctx.send("Rich Presence updated.")

    @commands.command(description='Refresh the version number and date of last update from the config.'
                                  '\nCalls `updaterp Do DTbot (v. dtbot_version)` to update the Rich Presence.'
                                  '\nCalls `reload general` to update the use of the version'
                                  'and date in the `info` and `changelog` commands.\nDevelopers only.',
                      brief='Refresh the version and date of the last update. Developers only.')
    async def updatever(self, ctx: commands.Context):
        self.bot.bot_config = ConfigParser()
        self.bot.bot_config.read('./config/config.ini')
        self.bot.log.info(f"{ctx.author} refreshed dtbot_version and last_update.")
        self.bot.log.info("Updating Rich Presence and reloading General...")
        await ctx.invoke(self.bot.get_command('updaterp'), 'Do DTbot help (v. dtbot_version)')  # type: ignore
        await ctx.invoke(self.bot.get_command('reload'), extension_name='general')  # type: ignore

    @commands.command(description='Shutdown command for the bot. Developers only.',
                      brief='Shut the bot down. Developers only.')
    async def shutdownbot(self, ctx: commands.Context, passcode: str):
        if passcode == self.SDB_CODE:
            try:
                self.heartbeat.stop()
            except:
                pass
            await self.bot.close()
        else:
            return


async def setup(bot: DTbot):
    await bot.add_cog(Dev(bot))
