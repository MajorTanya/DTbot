import mysql.connector as mariadb
from discord.ext import commands
from mysql.connector import pooling

from DTbot import DTbot, config

config.read('./config/config.ini')
default_prefix = config.get('General', 'prefix')

db_config = dict(config.items('Database'))
tables = config.items('Database defaults')
procedures = config.items("Database procedures")


def det_prefixes(bot, msg):
    if msg.guild and msg.guild.id:
        db = cnx.get_connection()
        cursor = db.cursor()
        prefix = cursor.callproc('GetServerPrefix', (msg.guild.id, '@res'))[1]
        db.close()
        prefixes = [prefix + ' ', prefix]
        return commands.when_mentioned_or(*prefixes)(bot, msg)
    else:
        return commands.when_mentioned_or(default_prefix)(bot, msg)


def ensuredb():
    # to ensure we have a database, create it on launch with a non-pooled connection
    fcnx = mariadb.connect(user=db_config.get('user'), password=db_config.get('password'))
    firstcursor = fcnx.cursor()
    try:
        firstcursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']} DEFAULT CHARACTER SET 'utf8'")
        bot.log.debug(f"Successfully created database {db_config['database']}")
    except mariadb.Error as err:
        bot.log.error(f"Failed creating database: {err}")
    finally:
        fcnx.close()


def start_db():
    try:
        # try to USE the given database and CREATE the tables if necessary
        db = cnx.get_connection()
        cursor = db.cursor()
        cursor.execute(f"USE {db_config['database']}")
        bot.log.debug(f"Using database: {db_config['database']}")

        for table_name, table_description in tables:
            try:
                bot.log.debug(f"Creating table {table_name}: ")
                cursor.execute(table_description)
            except mariadb.Error as err:
                bot.log.error(err.msg)
            else:
                bot.log.debug("OK")

        for procedure_name, procedure_description in procedures:
            try:
                bot.log.debug(f"Creating procedure {procedure_name}")
                cursor.execute(procedure_description)
            except mariadb.Error as err:
                bot.log.error(err.msg)
            else:
                bot.log.debug("OK")

        db.close()
    except mariadb.Error as err:
        bot.log.error(f"Error connecting to {db_config['database']}.")
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
    cnx = mariadb.pooling.MySQLConnectionPool(pool_size=10, pool_reset_session=True, **db_config)

    run_bot()
