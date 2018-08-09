from discord import Game
from discord.ext import commands

dbot_version = "1.6"
command_prefix = '+'

startup_extensions = ["conversion", "general", "interaction", "maths", "misc", "people", "rng"]
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


@bot.command(hidden=True,
             description="Can load additional extensions into DTbot (devs, mods and admins only)",
             brief="Load an extension")
@commands.has_any_role("The Dark Lords", "Administrator", "Dbot Dev", "DTbot Dev", "Tanya")
async def load(extension_name : str):
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))


@bot.command(hidden=True,
             description="Unload an extension (devs, mods, and admins only)",
             brief="Unload an extension")
@commands.has_any_role("The Dark Lords", "Administrator", "Dbot Dev", "DTbot Dev", "Tanya")
async def unload(extension_name : str):
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))


@bot.command(hidden=True,
             description="First unload and then immediately reload a module",
             brief="Reload an extension")
@commands.has_any_role("The Dark Lords", "Administrator", "Dbot Dev", "Tanya")
async def reload(extension_name : str):
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))


@bot.command(hidden=True,
             description='Shutdown command for the bot, only usable by developer roles',
             brief='Shutdown the bot')
@commands.has_any_role("Dbot Dev", "DTbot Dev", "Tanya")
async def shutdownbot(passcode: str):
    if passcode == '':
                # passcode not in public release
        await bot.logout()
    else:
        pass


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
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run('')
