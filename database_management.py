import random
import time

import mysql.connector as mariadb
from discord.ext import commands
from mysql.connector import errorcode

from DTbot import config, dev_set

DB_USER = config.get('Database', 'db_user')
DB_PASS = config.get('Database', 'db_pass')
DB_HOST = config.get('Database', 'db_host')
DB_NAME = config.get('Database', 'db_name')
users_default = config.get('Database', 'users_default')
commandstats_default = config.get('Database', 'commandstats_default')

prepstmt_checkuserexist = "SELECT * FROM users WHERE user_id = ? LIMIT 1"
prepstmt_checkxptime = "SELECT user_last_xp_gain FROM users WHERE user_id = ? LIMIT 1"
prepstmt_incrxp = "UPDATE IGNORE users SET user_xp = user_xp + ?, user_last_xp_gain = ? WHERE user_id = ?"
prepstmt_newuser = "INSERT IGNORE INTO users (user_id) VALUES (?)"
prepstmt_manualnewuser = "INSERT IGNORE INTO users (user_id, user_xp, user_last_xp_gain, user_rep, user_last_rep_awarded) VALUES (?, ?, ?, ?, ?)"
prepstmt_xpget = "SELECT user_xp FROM users WHERE user_id = ? LIMIT 1"

PREPSTMTS = (prepstmt_checkuserexist, prepstmt_checkxptime, prepstmt_incrxp, prepstmt_newuser, prepstmt_manualnewuser,
             prepstmt_xpget)

cnx = mariadb.connect(user=DB_USER, password=DB_PASS, host=DB_HOST)
cursor = cnx.cursor()
prepcursor = cnx.cursor(prepared=True)


def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mariadb.Error as err:
        print("Failed creating database: {}".format(err))


def start_db():
    try:
        # try to USE the given database, or create it
        cursor.execute("USE {}".format(DB_NAME))
        print("Using {}".format(DB_NAME))
    except mariadb.Error as err:
        print("Database {} does not exist.".format(DB_NAME))
        print(err)
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME

    tables = {'users': users_default, 'commandstats': commandstats_default}

    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mariadb.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def checkdbforuser(message):
    query = "EXECUTE stmnt1 USING " + str(message.author.id) + ";"
    cursor.execute(query)
    row = cursor.fetchone()
    if row:
        # entry for this user ID exists, proceed to check for last XP gain time, possibly awarding some new XP
        query = "EXECUTE stmnt2 USING " + str(message.author.id) + ";"
        cursor.execute(query)
        last_xp_gain = cursor.fetchone()[0]
        unix_now = int(time.time())
        if unix_now - last_xp_gain > 120:
            # user got XP more than two minutes ago, award some
            params = (random.randint(15, 25), unix_now, str(message.author.id))
            query = "EXECUTE stmnt3 USING " + ", ".join(str(param) for param in params) + ";"
            cursor.execute(query)
            cnx.commit()
        else:
            # user got XP less than two minutes ago, don't award new XP
            pass
    else:
        # user is unknown to the database, add it with user ID and default in the other fields
        query = "EXECUTE stmnt4 USING " + str(message.author.id) + ";"
        cursor.execute(query)
        cnx.commit()


class DatabaseManagement:
    def __init__(self, bot):
        self.bot = bot

        start_db()

        i = 0
        for x in PREPSTMTS:
            i = i + 1
            prepstmnt = "PREPARE stmnt" + str(i) + " FROM '" + x + "';"
            try:
                cursor.execute(prepstmnt)
                print(prepstmnt)
            except mariadb.Error as e:
                print(e)


    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        elif message.author.bot:
            return
        try:
            checkdbforuser(message)
        finally:
            pass
        pass


    @commands.command(hidden=True,
                      pass_context=True,
                      description="Manually adds an entry to the table 'users' of DTbot's database."
                                  "\nGenerally not required. Developers only.")
    async def adduserdata(self, ctx, user_id: int, user_xp: int, user_last_xp_gain: int, user_rep: int, user_last_rep_awarded: int):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            params = (user_id, user_xp, user_last_xp_gain, user_rep, user_last_rep_awarded)
            try:
                s_params = ", ".join(str(param) for param in params)
                query = "EXECUTE stmnt5 USING " + s_params + ";"
                cursor.execute(query)
                cnx.commit()
                await self.bot.say("Row added successfully to table `users` in database `{}`.".format(DB_NAME))
            except mariadb.Error as err:
                print(err)
            except Exception as e:
                print(e)


def setup(bot):
    bot.add_cog(DatabaseManagement(bot))
