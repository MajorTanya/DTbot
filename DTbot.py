import datetime
from configparser import ConfigParser

from discord import Game
from discord.ext import commands

config = ConfigParser()
config.read('./config/config.ini')
command_prefix = config.get('General', 'prefix')
TOKEN = config.get('General', 'token')
dtbot_version = config.get('Info', 'dtbot_version')

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
    elif message.author.bot:
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
