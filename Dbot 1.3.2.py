from discord import Game
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import asyncio
import time
import datetime
import json
import os.path
dbot_version = "1.3.2"
xp_timer = 120

startup_extensions = ["conversion", "general", "interaction", "maths", "misc", "people", "rng"]
bot = commands.Bot(command_prefix='+')
epoch = datetime.datetime.utcfromtimestamp(0)

#commands


@bot.event
async def on_message(message):
        user_add_xp(message.author.id, 2)
        await bot.process_commands(message)


@bot.command(hidden=True,
             description="Can load additional extensions into DTbot (devs, mods and admins only)",
             brief="Load an extension")
@commands.has_any_role("The Dark Lords", "Administrator", "Dbot Dev", "Tanya")
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))


@bot.command(hidden=True,
             description="Unload an extension (devs, mods, and admins only)",
             brief="Unload an extension")
@commands.has_any_role("The Dark Lords", "Administrator", "Dbot Dev", "Tanya")
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))


@bot.group(hidden=True,
           aliases=['dtbot'])
async def DTbot():
        await bot.say('You found a secret. Good job')
        await bot.say('this will eventually be used for something')
        # D:TANYA DO NOT DELETE THIS
        # D:its for something i wanna do in the future and im just making sure it doesnt get used for a diferent command
        # T:okay


@bot.group(pass_context=True,
           description="Shows a user's amount of XP (tells the command user's XP if called without mentioning a user)",
           brief="Show XP",
           aliases=['XP'])
async def xp(ctx, user: discord.Member = None):
        if user:
                await bot.say('**{}**'.format(ctx.message.mentions[0].display_name) + ' has `{}'.format(get_xp(ctx.message.mentions[0].id)) + ' XP`.')
        else:
                await bot.say('You have `{}'.format(get_xp(ctx.message.author.id)) + ' XP`, **{}**.'.format(ctx.message.author.display_name))


@xp.error
async def xp_error(error, ctx):
        await bot.say('**{}**'.format(ctx.message.mentions[0].display_name) + ' has not said anything yet. <:sad:420377816509710356> `(0 XP)`.')


def user_add_xp(user_id, xp):
    if os.path.isfile('users.json'):
        try:
            with open('users.json', 'r') as fp:
                users = json.load(fp)

            time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - users[user_id]['xp_time']
            if time_diff >= xp_timer:
                users[user_id]['xp'] += xp
                users[user_id]['xp_time'] = (datetime.datetime.utcnow() - epoch).total_seconds()
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id] = {}
            users[user_id]['xp'] = xp
            users[user_id]['xp_time'] = (datetime.datetime.utcnow() - epoch).total_seconds()
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    else:
        users = {user_id: {}}
        users[user_id]['xp'] = xp
        users[user_id]['xp_time'] = (datetime.datetime.utcnow() - epoch).total_seconds()
        with open('users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)


def get_xp(user_id):
    if os.path.isfile('users.json'):
        with open('users.json', 'r') as fp:
            users = json.load(fp)
        return users[user_id]['xp']
    else:
        return 0


@bot.group(hidden=True,
           description='Shutdown command for the bot, only usable by "Dbot Dev" or "Tanya" roles',
           brief='Shutdown the bot')
@commands.has_any_role("Dbot Dev", "Tanya")
async def shutdownbot(passcode: str):
        if passcode == '':
                # passcode not in public release
                await bot.logout()
        else:
                pass


# online confirmation
@bot.event
async def on_ready():
        await bot.change_presence(game=Game(name="+help (v. " + dbot_version + ")"))
        print(bot.user.name)
        print('online')
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
