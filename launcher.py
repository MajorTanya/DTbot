from configparser import ConfigParser

import discord
import mysql.connector as mariadb
from discord.ext import commands
from mysql.connector import pooling

from DTbot import DTbot

launch_config = ConfigParser()
launch_config.read('./config/config.ini')
default_prefixes = [launch_config.get('General', 'prefix')]

db_config = dict(launch_config.items('Database'))
lauch_db_config = db_config
lauch_db_config['pool_name'] = 'launch_pool'
DB_NAME = db_config.get('database')
commandstats_default = launch_config.get('Database defaults', 'commandstats_default')
servers_default = launch_config.get('Database defaults', 'servers_default')
users_default = launch_config.get('Database defaults', 'users_default')

dtbot_colour = discord.Colour(0x5e51a8)


def det_prefixes(bot, msg):
    if msg.guild.id:
        db = cnx.get_connection()
        cursor = db.cursor()
        prefix = cursor.callproc('GetServerPrefix', (msg.guild.id, '@res'))[1]
        db.close()
        prefixes = [prefix + ' ', prefix]
        return commands.when_mentioned_or(*prefixes)(bot, msg)
    else:
        return commands.when_mentioned_or(default_prefixes)(bot, msg)


def ensuredb():
    # to ensure we have a database, create it on launch with a non-pooled connection
    fcnx = mariadb.connect(user=db_config.get('user'), password=db_config.get('password'))
    firstcursor = fcnx.cursor()
    try:
        firstcursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        bot.log.dtbotinfo(bot.log, f"Successfully created database {DB_NAME}")
    except mariadb.Error as err:
        bot.log.error(f"Failed creating database: {err}")
    finally:
        fcnx.close()


def start_db():
    try:
        # try to USE the given database and CREATE the tables if necessary
        db = cnx.get_connection()
        cursor = db.cursor()
        cursor.execute(f"USE {DB_NAME}")
        bot.log.dtbotinfo(bot.log, f"Using database: {DB_NAME}")

        tables = {'users': users_default, 'commandstats': commandstats_default, 'servers': servers_default}

        for table_name in tables:
            table_description = tables[table_name]
            try:
                bot.log.dtbotinfo(bot.log, f"Creating table {table_name}: ")
                cursor.execute(table_description)
            except mariadb.Error as err:
                bot.log.error(err.msg)
            else:
                bot.log.dtbotinfo(bot.log, "OK")
        db.close()
    except mariadb.Error as err:
        bot.log.error(f"Error connecting to {DB_NAME}.")
        bot.log.error(err)
    finally:
        pass


def run_bot():
    try:
        start_db()
    except Exception as e:
        print('Exception connecting to database. Closing.')
        bot.log.exception(f'Exception connecting to database. Closing.\n{e}')
        return

    bot.run()


if __name__ == '__main__':
    bot = DTbot(det_prefixes=det_prefixes)

    ensuredb()
    # open a pooled connection solely used for prefix checking
    cnx = mariadb.pooling.MySQLConnectionPool(pool_size=10, pool_reset_session=True, **lauch_db_config)

    run_bot()
