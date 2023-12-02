import os
from configparser import ConfigParser

import mariadb
from dotenv import load_dotenv
from mariadb.constants import CLIENT

from DTbot import DTbot

if __name__ == "__main__":
    load_dotenv(dotenv_path="./config/.env", override=True)
    config = ConfigParser()
    config.read("./config/config.ini")
    bot = DTbot(bot_config=config)

    cnx: mariadb.Connection
    cursor: mariadb.Cursor

    # to ensure we have a database, create it on launch with a non-pooled connection
    # for client_flag cf.: https://jira.mariadb.org/browse/CONPY-109 (comment by Georg Richter)
    with mariadb.connect(
        user=os.environ.get("DTBOT_DB_USER"),
        password=os.environ.get("DTBOT_DB_PASS"),
        client_flag=CLIENT.MULTI_STATEMENTS,
    ) as cnx:
        try:
            with cnx.cursor() as cursor:
                with open("./database_scripts/database_and_tables.sql", encoding="utf-8") as definitions_file:
                    bot.log.debug(f"Running {definitions_file.name}")
                    cursor.execute(definitions_file.read())
                    bot.log.debug(f"Successfully ran {definitions_file.name}")

            with cnx.cursor() as cursor:
                with open("./database_scripts/migrations.sql", encoding="utf-8") as migrations_file:
                    bot.log.debug(f"Running {migrations_file.name}")
                    cursor.execute(migrations_file.read())
                    bot.log.debug(f"Successfully ran {migrations_file.name}")

            with cnx.cursor() as cursor:
                with open("./database_scripts/procedures.sql", encoding="utf-8") as procedures_file:
                    bot.log.debug(f"Running {procedures_file.name}")
                    cursor.execute(procedures_file.read())
                    bot.log.debug(f"Successfully ran {procedures_file.name}")

        except mariadb.Error as err:
            bot.log.error(f"Failed during database startup: {err}")
            raise err

        else:  # No Exceptions were thrown, log success
            bot.log.debug("Successfully executed all SQL scripts.")

    bot.run()
