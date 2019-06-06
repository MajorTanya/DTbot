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
main_dev_id = config.get('General', 'main_dev_id')
INVITE = config.get('General', 'invite')
REQHALL = config.get('General', 'reqhall')
REPORTS_CH = config.get('General', 'reports_ch')
TOKEN = config.get('General', 'token')
dtbot_version = config.get('Info', 'dtbot_version')
last_updated = config.get('Info', 'last_updated')
ger_tz = config.get('Heartbeat', 'ger_tz')
ger_tz = timezone(ger_tz)

human_startup_time = datetime.datetime.now(ger_tz)
human_startup_time = human_startup_time.strftime('%d-%m-%Y - %H:%M:%S %Z')
startup_time = datetime.datetime.utcnow()

authlist = open('./config/authlist.txt', 'r')
authlist = [x.replace('\n', '') for x in authlist]
authlist = [line.split(',') for line in authlist[7:]]
dev_set = set(authlist[-4])

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


# online confirmation
@bot.event
async def on_ready():
    await bot.change_presence(game=Game(name=command_prefix + "help (v. " + dtbot_version + ")"))
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

    bot.run(TOKEN)
