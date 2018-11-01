import asyncio
import datetime
from configparser import ConfigParser

from discord import Game
from discord.ext import commands
from pytz import timezone

epoch = datetime.datetime.utcfromtimestamp(0)

config = ConfigParser()
config.read('./config/config.ini')
h_code = config.get('Dev', 'h_code')
sdb_code = config.get('Dev', 'sdb_code')
command_prefix = config.get('General', 'prefix')
REQHALL = config.get('General', 'reqhall')
TOKEN = config.get('General', 'token')
dbot_version = config.get('Info', 'dbot_version')
last_updated = config.get('Info', 'last_updated')
ger_tz = config.get('Heartbeat', 'ger_tz')
ger_tz = timezone(ger_tz)
human_startup_time = datetime.datetime.now(ger_tz)
startup_time = datetime.datetime.utcnow()

authlist = open('./config/authlist.txt', 'r')
authlist = [x.replace('\n', '') for x in authlist]
authlist = [line.split(',') for line in authlist[7:]]
dev_set = set(authlist[-4])

async def heartbeat():
    await bot.wait_until_ready()

    heartbeat_config = ConfigParser()
    heartbeat_config.read('./config/config.ini')
    hb_freq = int(heartbeat_config.get('Heartbeat', 'hb_freq'))
    hb_chamber = heartbeat_config.get('Heartbeat', 'hb_chamber')
    hb_chamber = bot.get_channel(hb_chamber)

    await bot.send_message(hb_chamber, "Starting up at: `" + str(startup_time) + "`")
    await asyncio.sleep(hb_freq)
    while not bot.is_closed:
        now = datetime.datetime.utcnow()
        ger_time = datetime.datetime.now(ger_tz)
        now_timezone = ger_time.strftime('%d-%m-%Y - %H:%M:%S %Z')
        tdelta = now - startup_time
        tdelta = tdelta - datetime.timedelta(microseconds=tdelta.microseconds)
        beat = await bot.send_message(hb_chamber, "Alive and still running since: `" + str(human_startup_time) + "`.\nTime now: `" + str(now_timezone) + "`.\nCurrent uptime: `" + str(tdelta) + "`\n:heart:")
        await asyncio.sleep(hb_freq)
        await bot.delete_message(beat)


extensions = config.items('Extensions')
startup_extensions = []
for key, ext in extensions:
    startup_extensions.append(ext)


bot = commands.Bot(command_prefix)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        try:
            triggerinmsg, contentofmsg = message.content.split(' ', 1)
            triggerinmsg_l = triggerinmsg.lower()
            message.content = triggerinmsg_l + " " + contentofmsg
        except ValueError:
            triggerinmsg = message.content.split(' ', 1)[0]
            triggerinmsg_l = triggerinmsg.lower()
            message.content = triggerinmsg_l
        await bot.process_commands(message)


@bot.group(hidden=True,
           pass_context=True,
           description="Manages the heartbeat of DTbot. Developers only.")
async def heart(ctx):
    if ctx.invoked_subcommand is None:
        return

@heart.command(pass_context=True,
               description="Stops the heartbeat of DTbot. Developers only.")
async def stop(ctx, code=None):
    if code == h_code:
        heartbeat_task.cancel()
        await bot.say('Heartbeat stopped by user {}'.format(ctx.message.author.name))


@heart.command(pass_context=True,
               description="Starts the heartbeat of DTbot. Developers only.")
async def start(ctx, code=None):
    if code == h_code:
        global heartbeat_task
        heartbeat_task = bot.loop.create_task(heartbeat())
        await bot.say('Heartbeat started by user {}'.format(ctx.message.author.name))


# online confirmation
@bot.event
async def on_ready():
    await bot.change_presence(game=Game(name=command_prefix + "help (v. " + dbot_version + ")"))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('Successfully loaded extension {}.'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}.'.format(extension, exc))

    heartbeat_task = bot.loop.create_task(heartbeat())
    bot.run(TOKEN)
