import asyncio
import datetime

import discord
from discord import Game
from discord.ext import commands
from pytz import timezone

from DTbot import config, dev_set, startup_time, command_prefix, dtbot_version

h_code = config.get('Dev', 'h_code')
sdb_code = config.get('Dev', 'sdb_code')
REPORTS_CH = config.get('General', 'reports_ch')
ger_tz = timezone(config.get('Heartbeat', 'ger_tz'))
human_startup_time = datetime.datetime.now(ger_tz).strftime('%d-%m-%Y - %H:%M:%S %Z')


class Dev:
    def __init__(self, bot):
        self.bot = bot

    async def heartbeat(self):
        await self.bot.wait_until_ready()

        hb_freq = int(config.get('Heartbeat', 'hb_freq'))
        hb_chamber = self.bot.get_channel(config.get('Heartbeat', 'hb_chamber'))

        startup_embed = discord.Embed(colour=discord.Colour(0x5e51a8), title=self.bot.user.name + "'s Heartbeat",
                                      description=self.bot.user.name + " is starting up!")
        startup_embed.add_field(name="Startup time:", value=str(human_startup_time))
        await self.bot.send_message(hb_chamber, embed=startup_embed)
        await asyncio.sleep(hb_freq)
        while not self.bot.is_closed:
            now = datetime.datetime.utcnow()
            now_timezone = datetime.datetime.now(ger_tz).strftime('%d-%m-%Y - %H:%M:%S %Z')
            tdelta = now - startup_time
            tdelta = tdelta - datetime.timedelta(microseconds=tdelta.microseconds)
            beat_embed = discord.Embed(colour=discord.Colour(0x5e51a8), title=self.bot.user.name + "'s Heartbeat",
                                       description=self.bot.user.name + " is still alive and running!")
            beat_embed.add_field(name="Startup time:", value=str(human_startup_time))
            beat_embed.add_field(name="Time now:", value=str(now_timezone), inline=False)
            beat_embed.add_field(name="Uptime:", value=str(tdelta))
            beat_embed.set_footer(text="DTbot v. " + dtbot_version)
            beat = await self.bot.send_message(hb_chamber, embed=beat_embed)
            await asyncio.sleep(hb_freq)
            await self.bot.delete_message(beat)

    async def on_ready(self):
        self.heartbeat_task = self.bot.loop.create_task(self.heartbeat())


    @commands.group(hidden=True,
                    pass_context=True,
                    description="Manages the heartbeat of DTbot. Developers only.")
    async def heart(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @heart.command(pass_context=True,
                   description="Stops the heartbeat of DTbot. Developers only.")
    async def stop(self, ctx, code=None):
        if code == h_code:
            self.heartbeat_task.cancel()
            await self.bot.say('Heartbeat stopped by user {}'.format(ctx.message.author.name))

    @heart.command(pass_context=True,
                   description="Starts the heartbeat of DTbot. Developers only.")
    async def start(self, ctx, code=None):
        if code == h_code:
            self.heartbeat_task = self.bot.loop.create_task(self.heartbeat())
            await self.bot.say('Heartbeat started by user {}'.format(ctx.message.author.name))


    @commands.command(hidden=True,
                      pass_context=True,
                      description="Lists all servers that DTbot is a member of. Developers only.",
                      brief="Full server list of DTbot. Developers only.")
    async def listservers(self, ctx):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            serverlist = list()
            servers = list(self.bot.servers)
            server_count = len(servers)
            reporting_channel = self.bot.get_channel(REPORTS_CH)
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="A list of all the servers " + self.bot.user.name + " is a member of")
            embed.set_footer(text="Total server count: " + str(server_count))
            for x in range(server_count):
                serverlist.append(servers[x - 1].name)
            stringle = '\n'.join(serverlist)
            embed.add_field(name="Servers", value=stringle)
            await self.bot.send_message(reporting_channel, embed=embed)


    @commands.command(hidden=True,
                      pass_context=True,
                      description="Can load additional extensions into DTbot. Developers only.",
                      brief="Load an extension. Developers only.")
    async def load(self, ctx, extension_name: str):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            try:
                self.bot.load_extension(extension_name)
            except (AttributeError, ImportError) as e:
                await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
                return
            await self.bot.say("{} loaded.".format(extension_name))
        else:
            await self.bot.say("Insufficient permissions to modify the loadout of DTbot.")


    @commands.command(hidden=True,
                      pass_context=True,
                      description="Unload an extension. Developers only.",
                      brief="Unload an extension. Developers only.")
    async def unload(self, ctx, extension_name: str):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            self.bot.unload_extension(extension_name)
            await self.bot.say("Module `{}` unloaded.".format(extension_name))


    @commands.command(hidden=True,
                      pass_context=True,
                      description="First unload and then immediately reload a module. Developers only.",
                      brief="Reload an extension. Developers only.")
    async def reload(self, ctx, extension_name: str):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            self.bot.unload_extension(extension_name)
            await self.bot.say("{} unloaded.".format(extension_name))
            try:
                self.bot.load_extension(extension_name)
            except (AttributeError, ImportError) as e:
                await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
                return
            await self.bot.say("{} loaded.".format(extension_name))


    @commands.command(hidden=True,
                      pass_context=True,
                      description="Update / Refresh DTbot's Rich Presence. Developers only.",
                      brief="Update DTbot's Rich Presence. Developers only.")
    async def updaterp(self, ctx, *caption: str):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            if caption:
                caption = " ".join(caption)
                if "command_prefix" in caption:
                    caption = caption.replace("command_prefix", command_prefix)
                if "dtbot_version" in caption:
                    caption = caption.replace("dtbot_version", dtbot_version)
                await self.bot.change_presence(game=Game(name=caption))
            else:
                await self.bot.change_presence(game=Game(name=command_prefix + "help (v. " + dtbot_version + ")"))
            await self.bot.say("Rich Presence updated.")


    @commands.command(hidden=True,
                      pass_context=True,
                      description='Shutdown command for the bot. Developers only.',
                      brief='Shutdown the bot. Developers only.')
    async def shutdownbot(self, ctx, passcode: str):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            if passcode == sdb_code:
                await self.bot.logout()
            else:
                return


def setup(bot):
    bot.add_cog(Dev(bot))
