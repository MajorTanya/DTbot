import logging
import os
import sys
from configparser import ConfigParser
from datetime import UTC, datetime

import discord.utils
import mariadb
from dotenv import load_dotenv
from mariadb.constants import CLIENT

from DTbot import DTbot
from util.utils import get_file_handler, get_stream_handler


def main():
    load_dotenv(dotenv_path="./config/.env", override=True)

    token = os.environ.get("DTBOT_TOKEN")
    if token is None:
        raise RuntimeError("Couldn't get DTBOT_TOKEN from environment")

    startup_time = datetime.now(tz=UTC).replace(microsecond=0)
    dev_mode = "--dev" in sys.argv

    # region Logging setup
    logger = logging.getLogger("dtbot")
    logger.setLevel(logging.DEBUG)
    if dev_mode:
        stream_handler = get_stream_handler(level=logging.DEBUG, stream=sys.stdout)
        file_handler = discord.utils.MISSING
    else:
        stream_handler = get_stream_handler()
        file_handler = get_file_handler(logs_folder="./logs", startup_time=startup_time)
        logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    # endregion

    # region Database setup
    basic_db_creds = {
        "host": os.environ.get("DTBOT_DB_HOST"),
        "user": os.environ.get("DTBOT_DB_USER"),
        "password": os.environ.get("DTBOT_DB_PASS"),
    }
    pool_db_config = {
        "database": os.environ.get("DTBOT_DB_NAME"),
        "pool_name": os.environ.get("DTBOT_DB_POOL"),
    }
    basic_creds_missing = [k for k, v in basic_db_creds.items() if v is None]
    pool_creds_missing = [k for k, v in pool_db_config.items() if v is None]
    total_missing = basic_creds_missing + pool_creds_missing
    if len(total_missing) != 0:
        raise RuntimeError(f"Incomplete database credentials: {",".join(m.upper() for m in total_missing)}")

    cnx: mariadb.Connection
    cursor: mariadb.Cursor

    # to ensure we have a database, create it on launch with a non-pooled connection
    # for client_flag cf.: https://jira.mariadb.org/browse/CONPY-109#comment-164771
    with mariadb.connect(
        **basic_db_creds,
        client_flag=CLIENT.MULTI_STATEMENTS,
    ) as cnx:
        try:
            with cnx.cursor() as cursor:
                with open("./database_scripts/database_and_tables.sql", encoding="utf-8") as definitions_file:
                    logger.debug(f"Running {definitions_file.name}")
                    cursor.execute(definitions_file.read())
                    logger.debug(f"Successfully ran {definitions_file.name}")

            with cnx.cursor() as cursor:
                with open("./database_scripts/migrations.sql", encoding="utf-8") as migrations_file:
                    logger.debug(f"Running {migrations_file.name}")
                    cursor.execute(migrations_file.read())
                    logger.debug(f"Successfully ran {migrations_file.name}")

            with cnx.cursor() as cursor:
                with open("./database_scripts/procedures.sql", encoding="utf-8") as procedures_file:
                    logger.debug(f"Running {procedures_file.name}")
                    cursor.execute(procedures_file.read())
                    logger.debug(f"Successfully ran {procedures_file.name}")

        except mariadb.Error as err:
            logger.error(f"Failed during database startup: {err}")
            raise err

        else:  # No Exceptions were thrown, log success
            logger.debug("Successfully executed all SQL scripts.")

    db_connection_pool = mariadb.ConnectionPool(pool_size=10, reconnect=True, **basic_db_creds, **pool_db_config)
    # endregion

    bot_config = ConfigParser()
    bot_config.read("./config/config.ini")

    bot = DTbot(
        bot_config=bot_config,
        db_connection_pool=db_connection_pool,
        in_dev_mode=dev_mode,
        logger=logger,
        startup_time=startup_time,
    )

    bot.run(token, log_handler=file_handler)


if __name__ == "__main__":
    raise SystemExit(main())
