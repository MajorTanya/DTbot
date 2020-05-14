import datetime
import logging
from configparser import ConfigParser

import discord
import mysql.connector as mariadb
from discord.ext import commands
from mysql.connector import errorcode, pooling
from pytz import timezone

from bot import DTbot

launch_config = ConfigParser()
launch_config.read('./config/config.ini')
default_prefixes = [launch_config.get('General', 'prefix')]

ger_tz = timezone(launch_config.get('Heartbeat', 'ger_tz'))
human_startup_time = datetime.datetime.now(ger_tz).strftime('%d-%m-%Y - %H:%M:%S %Z')
log_startup_time = datetime.datetime.now(ger_tz).strftime('%Y-%m-%d (%H-%M-%S %Z)')
startup_time = datetime.datetime.utcnow()

db_config = dict(launch_config.items('Database'))
DB_NAME = db_config.get('database')
commandstats_default = launch_config.get('Database defaults', 'commandstats_default')
servers_default = launch_config.get('Database defaults', 'servers_default')
users_default = launch_config.get('Database defaults', 'users_default')

dtbot_colour = discord.Colour(0x5e51a8)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=f'./logs/{log_startup_time}.log', encoding='utf-8',
                              mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
logger.addHandler(handler)

# to ensure we have a database, create it on launch with a non-pooled connection
fcnx = mariadb.connect(user=db_config.get('user'), password=db_config.get('password'))
firstcursor = fcnx.cursor()
try:
    firstcursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
except mariadb.Error as err:
    logger.error(f"Failed creating database: {err}")
finally:
    fcnx.close()

# open the pooled connection
cnx = mariadb.pooling.MySQLConnectionPool(pool_size=10, pool_reset_session=True, **db_config)


def det_prefixes(bot, msg):
    guild = msg.guild.id
    if guild:
        db = cnx.get_connection()
        cursor = db.cursor()
        prefix = cursor.callproc('GetServerPrefix', (msg.guild.id, '@res'))[1]
        db.close()
        prefixes = [prefix + ' ', prefix]
        return commands.when_mentioned_or(*prefixes)(bot, msg)
    else:
        return commands.when_mentioned_or(default_prefixes)(bot, msg)


def start_db():
    try:
        # try to USE the given database and CREATE the tables if necessary
        db = cnx.get_connection()
        cursor = db.cursor()
        cursor.execute(f"USE {DB_NAME}")
        logger.info(f"Using database: {DB_NAME}")

        tables = {'users': users_default, 'commandstats': commandstats_default, 'servers': servers_default}

        for table_name in tables:
            table_description = tables[table_name]
            try:
                logger.info(f"Creating table {table_name}: ")
                cursor.execute(table_description)
            except mariadb.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    logger.info("already exists.")
                else:
                    logger.error(err.msg)
            else:
                logger.info("OK")
        db.close()
    except mariadb.Error as err:
        logger.error(f"Error connecting to {DB_NAME}.")
        logger.error(err)
    finally:
        pass


def run_bot():
    try:
        start_db()
    except Exception as e:
        print('Exception connecting to database. Closing.')
        logger.exception(f'Exception connecting to database. Closing.\n{e}')
        return

    bot = DTbot(det_prefixes=det_prefixes)
    bot.run()


if __name__ == '__main__':
    run_bot()
