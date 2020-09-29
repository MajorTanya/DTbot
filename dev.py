import asyncio
import datetime
import sys

import discord
from discord import Game
from discord.ext import commands

from DTbot import config, ger_tz, human_startup_time, startup_time

dtbot_version = config.get('Info', 'dtbot_version')
h_code = config.get('Developers', 'h_code')
sdb_code = config.get('Developers', 'sdb_code')


class Dev(commands.Cog, command_attrs=dict(hidden=True)):
    """Developer Commands and DTbot Management"""

    def __init__(self, bot):
        self.bot = bot
        if len(sys.argv) < 2 or sys.argv[1] == '1':
            # run "python launcher.py 1" to start DTbot with a heartbeat message, 0 if not
            # if no parameter is provided, defaults to run with a heartbeat
            self.heartbeat_task = self.bot.loop.create_task(self.heartbeat())

    def cog_unload(self):
        self.heartbeat_task.cancel()

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.message.author)

    async def heartbeat(self):
        await self.bot.wait_until_ready()

        hb_freq = config.getint('Heartbeat', 'hb_freq')
        hb_chamber = self.bot.get_channel(config.getint('Heartbeat', 'hb_chamber'))

        startup_embed = discord.Embed(colour=self.bot.dtbot_colour, title=f"{self.bot.user.name}'s Heartbeat",
                                      description=f"{self.bot.user.name} is starting up!")
        startup_embed.add_field(name="Startup time:", value=str(human_startup_time))
        await hb_chamber.send(embed=startup_embed)
        await asyncio.sleep(hb_freq)
        while not self.bot.is_closed():
            now = datetime.datetime.utcnow()
            now_timezone = datetime.datetime.now(ger_tz).strftime('%d-%m-%Y - %H:%M:%S %Z')
            tdelta = now - startup_time
            tdelta = tdelta - datetime.timedelta(microseconds=tdelta.microseconds)
            beat_embed = discord.Embed(colour=self.bot.dtbot_colour, title=f"{self.bot.user.name}'s Heartbeat",
                                       description=f"{self.bot.user.name} is still alive and running!")
            beat_embed.add_field(name="Startup time:", value=str(human_startup_time))
            beat_embed.add_field(name="Time now:", value=str(now_timezone), inline=False)
            beat_embed.add_field(name="Uptime:", value=str(tdelta))
            beat_embed.set_footer(text=f"DTbot v. {dtbot_version}")
            await hb_chamber.send(embed=beat_embed, delete_after=hb_freq)
            await asyncio.sleep(hb_freq)

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
            self.heartbeat_task.cancel()
            self.bot.log.dtbotinfo(self.bot.log, f'Heartbeat stopped by user {ctx.author}.')
            await ctx.send(f'Heartbeat stopped by user {ctx.author}.')

    @heart.command(description="Starts the heartbeat of DTbot. Developers only.")
    async def start(self, ctx, code=None):
        if code == h_code:
            self.heartbeat_task = self.bot.loop.create_task(self.heartbeat())
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
            await self.bot.change_presence(activity=Game(name=caption))
        else:
            caption = f"Do @\u200bDTbot help (v. {dtbot_version})"
            await self.bot.change_presence(activity=Game(name=caption))
        self.bot.log.dtbotinfo(self.bot.log,
                               f"{self.bot.user.name}'s Rich Presence was updated to '{caption}' by {ctx.author}")
        await ctx.send("Rich Presence updated.")

    @commands.command(description='Shutdown command for the bot. Developers only.',
                      brief='Shut the bot down. Developers only.')
    async def shutdownbot(self, ctx, passcode: str):
        if passcode == sdb_code:
            try:
                self.heartbeat_task.cancel()
            except:
                pass
            await self.bot.logout()
        else:
            return


def setup(bot):
    bot.add_cog(Dev(bot))
