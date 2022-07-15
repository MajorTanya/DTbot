from configparser import ConfigParser

from mysql import connector as mariadb

from DTbot import DTbot

if __name__ == '__main__':
    config = ConfigParser()
    config.read('./config/config.ini')
    bot = DTbot(bot_config=config)

    db_config = dict(bot.bot_config.items('Database'))
    commandstats_default = bot.bot_config.get('Database defaults', 'commandstats_default')
    servers_default = bot.bot_config.get('Database defaults', 'servers_default')
    users_default = bot.bot_config.get('Database defaults', 'users_default')

    # to ensure we have a database, create it on launch with a non-pooled connection
    cnx = mariadb.connect(user=db_config.get('user'), password=db_config.get('password'))
    cursor = cnx.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']} DEFAULT CHARACTER SET 'utf8'")
        bot.log.debug(f"Successfully created database {db_config['database']}")

        cursor.execute(f"USE {db_config['database']}")
        bot.log.debug(f"Using database: {db_config['database']}")

        tables = {'users': users_default, 'commandstats': commandstats_default, 'servers': servers_default}

        for table_name in tables:
            table_description = tables[table_name]
            try:
                bot.log.debug(f"Creating table {table_name}: ")
                cursor.execute(table_description)
            except mariadb.Error as err:
                bot.log.error(err.msg)
            else:
                bot.log.debug("OK")

    except mariadb.Error as err:
        bot.log.error(f"Failed during database startup: {err}")

    finally:
        cnx.close()

    bot.run()
