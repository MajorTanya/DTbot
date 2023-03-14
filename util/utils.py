import enum
import random
import time
import typing

import discord
import mariadb  # type: ignore


class DBProcedure(enum.StrEnum):
    GetUserXp = 'GetUserXp'
    CheckXPTime = 'CheckXPTime'
    CheckAppCommandExist = 'CheckAppCommandExist'
    CheckUserExist = 'CheckUserExist'
    AddNewAppCommand = 'AddNewAppCommand'
    IncrementAppCommandUsage = 'IncrementAppCommandUsage'
    AddNewUser = 'AddNewUser'
    IncreaseXP = 'IncreaseXP'
    AddNewServer = 'AddNewServer'

    @classmethod
    def bool_procedures(cls) -> list[typing.Self]:
        return [DBProcedure.CheckUserExist, DBProcedure.CheckAppCommandExist]

    @classmethod
    def int_procedures(cls) -> list[typing.Self]:
        return [DBProcedure.GetUserXp, DBProcedure.CheckXPTime]

    @classmethod
    def returning_procedures(cls) -> list[typing.Self]:
        return [*DBProcedure.bool_procedures(), *DBProcedure.int_procedures()]

    @classmethod
    def non_returning_procedures(cls) -> list[typing.Self]:
        return [
            DBProcedure.AddNewAppCommand,
            DBProcedure.IncrementAppCommandUsage,
            DBProcedure.AddNewUser,
            DBProcedure.IncreaseXP,
            DBProcedure.AddNewServer,
        ]


_BoolProcedures = typing.Literal[DBProcedure.CheckUserExist, DBProcedure.CheckAppCommandExist]
_IntProcedures = typing.Literal[DBProcedure.GetUserXp, DBProcedure.CheckXPTime]
_NoReturnProcedures = typing.Literal[
    DBProcedure.AddNewAppCommand,
    DBProcedure.IncrementAppCommandUsage,
    DBProcedure.AddNewUser,
    DBProcedure.IncreaseXP,
    DBProcedure.AddNewServer,
]
_ReturnProcedures = typing.Literal[
    DBProcedure.CheckUserExist,
    DBProcedure.CheckAppCommandExist,
    DBProcedure.GetUserXp,
    DBProcedure.CheckXPTime,
]


@typing.overload
def dbcallprocedure(pool: mariadb.ConnectionPool, procedure: _BoolProcedures, *,
                    params: tuple[typing.Any, ...] = ()) -> bool:
    ...


@typing.overload
def dbcallprocedure(pool: mariadb.ConnectionPool, procedure: _IntProcedures, *,
                    params: tuple[typing.Any, ...] = ()) -> int:
    ...


@typing.overload
def dbcallprocedure(pool: mariadb.ConnectionPool, procedure: _NoReturnProcedures, *,
                    params: tuple[typing.Any, ...] = ()) -> None:
    ...


def dbcallprocedure(pool: mariadb.ConnectionPool, procedure: DBProcedure, *,
                    params: tuple[typing.Any, ...] = ()) -> bool | int | None:
    """Calls a stored procedure with the given parameters.

    Parameters
    -----------
    pool : mariadb.ConnectionPool
        The mariadb.ConnectionPool to get a connection from
    procedure : DBProcedure
        The Stored Procedure to call
    params : tuple
        A tuple of parameters to supply to the Stored Procedure (Default: ())
    """
    pconn: mariadb.Connection
    result = None
    returns = procedure in DBProcedure.returning_procedures()
    with pool.get_connection() as pconn:
        with pconn.cursor() as cursor:
            cursor.callproc(procedure, params)
            if returns:
                # we can be certain that the return value is at index [0] from all stored procedures
                result = cursor.fetchone()[0]
        pconn.commit()
    if returns and result is not None:
        return result


def checkdbforuser(pool: mariadb.ConnectionPool, message: discord.Message):
    result = dbcallprocedure(pool, DBProcedure.CheckUserExist, params=(message.author.id, '@res'))
    if result:
        # entry for this user ID exists, proceed to check for last XP gain time, possibly awarding some new XP
        last_xp_gain = dbcallprocedure(pool, DBProcedure.CheckXPTime, params=(message.author.id, '@res'))
        unix_now = int(time.time())
        if unix_now - last_xp_gain > 120:
            # user got XP more than two minutes ago, award between 15 and 25 XP and update last XP gain time
            dbcallprocedure(pool, DBProcedure.IncreaseXP, params=(message.author.id, random.randint(15, 25), unix_now))
    else:
        # user is unknown to the database, add it with user ID and default in the other fields
        dbcallprocedure(pool, DBProcedure.AddNewUser, params=(message.author.id,))


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
