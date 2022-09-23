import random
import time
import typing

import discord
import mariadb

TProcedures = typing.Literal['AddNewAppCommand', 'CheckAppCommandExist', 'IncrementAppCommandUsage',
                             'AddNewUser', 'CheckUserExist', 'CheckXPTime', 'GetUserXp', 'IncreaseXP', 'AddNewServer']


def dbcallprocedure(pool: mariadb.ConnectionPool, procedure: TProcedures, *, returns: bool = False, params: tuple = ()):
    pconn: mariadb.Connection = pool.get_connection()
    cursor: mariadb.Cursor = pconn.cursor()
    cursor.callproc(procedure, params)
    if returns:
        # we can be certain that the return value is at index [0] from all stored procedures
        # but since we return, we need to ensure the closing of the cursor and database connection first, then return
        result = cursor.fetchone()[0]
        cursor.close()
        pconn.close()
        return result
    pconn.commit()
    cursor.close()
    pconn.close()


def checkdbforuser(pool: mariadb.ConnectionPool, message: discord.Message):
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


def even_out_embed_fields(embed: discord.Embed):
    """Evens out Embed fields to avoid a misaligned last row
    (does not account for inline=False being set on any field)"""
    if len(embed.fields) % 3 != 0:  # even out the last line of embed fields
        embed.add_field(name='\u200b', value='\u200b')
        if len(embed.fields) % 3 == 2:  # if we added one and still need one more to make it 3
            embed.add_field(name='\u200b', value='\u200b')
    return embed


def rint(flt: float, digits: int = 2) -> int | float:
    """Round to [digits] (default: 2) digits. Returns int if rounded float has only zeroes after the decimal point."""
    return int(rounded) if (rounded := round(flt, digits)).is_integer() else rounded
