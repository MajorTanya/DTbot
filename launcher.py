from configparser import ConfigParser

import mariadb

from DTbot import DTbot

if __name__ == '__main__':
    config = ConfigParser()
    config.read('./config/config.ini')
    bot = DTbot(bot_config=config)

    db_config = dict(bot.bot_config.items('Database'))
    tables = bot.bot_config.items('Database defaults')
    procedures = config.items("Database procedures")

    # to ensure we have a database, create it on launch with a non-pooled connection
    cnx = mariadb.connect(user=db_config.get('user'), password=db_config.get('password'))
    cursor = cnx.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']} DEFAULT CHARACTER SET 'utf8'")
        bot.log.debug(f"Successfully created database {db_config['database']}")

        cursor.execute(f"USE {db_config['database']}")
        bot.log.debug(f"Using database: {db_config['database']}")

        for table_name, table_description in tables:
            try:
                bot.log.debug(f"Creating table {table_name}")
                cursor.execute(table_description)
            except mariadb.Error as err:
                bot.log.error(err)
            else:
                bot.log.debug("OK")

        for procedure_name, procedure_description in procedures:
            try:
                bot.log.debug(f"Creating procedure {procedure_name}")
                cursor.execute(procedure_description)
            except mariadb.Error as err:
                bot.log.error(err)
            else:
                bot.log.debug("OK")

    except mariadb.Error as err:
        bot.log.error(f"Failed during database startup: {err}")

    finally:
        cursor.close()
        cnx.close()

    bot.run()
