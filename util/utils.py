import random
import time

import discord
from mysql.connector import pooling


def dbcallprocedure(pool: pooling.MySQLConnectionPool, procedure, *, returns: bool = False,
                    params: tuple):
    db = pool.get_connection()
    cursor = db.cursor()
    if returns:
        # we can be certain that the return value is at index [1] from all stored procedures
        # but since we return, we need to ensure the closing of the database connection first, then return
        return_value = cursor.callproc(procedure, params)[1]
        db.close()
        return return_value
    cursor.callproc(procedure, params)
    db.commit()
    db.close()


def checkdbforuser(pool: pooling.MySQLConnectionPool, message: discord.Message):
    result = dbcallprocedure(pool, 'CheckUserExist', returns=True, params=(message.author.id, '@res'))
    if result:
        # entry for this user ID exists, proceed to check for last XP gain time, possibly awarding some new XP
        last_xp_gain = dbcallprocedure(pool, 'CheckXPTime', returns=True, params=(message.author.id, '@res'))
        unix_now = int(time.time())
        if unix_now - last_xp_gain > 120:
            # user got XP more than two minutes ago, award between 15 and 25 XP and update last XP gain time
            dbcallprocedure(pool, 'IncreaseXP', params=(message.author.id, random.randint(15, 25), unix_now))
    else:
        # user is unknown to the database, add it with user ID and default in the other fields
        dbcallprocedure(pool, 'AddNewUser', params=(message.author.id,))


# TODO: need on_interaction_complete (https://github.com/Rapptz/discord.py/issues/8126) to bring back commandstats

def rint(flt: float) -> int | float:
    """Round to 2 digits. Returns int if rounded float has only zeroes after the decimal point."""
    return int(rounded) if (rounded := round(flt, 2)).is_integer() else rounded
