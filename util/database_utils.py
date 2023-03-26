import enum
import random
import time
import typing

import discord
import mariadb


class DBProcedure(enum.StrEnum):
    AddNewAppCommand = "AddNewAppCommand"
    AddNewServer = "AddNewServer"
    AddNewUser = "AddNewUser"
    CheckAppCommandExist = "CheckAppCommandExist"
    CheckUserExist = "CheckUserExist"
    CheckXPTime = "CheckXPTime"
    GetServers = "GetServers"
    GetUserXp = "GetUserXp"
    IncreaseXP = "IncreaseXP"
    IncrementAppCommandUsage = "IncrementAppCommandUsage"
    InvalidateMissingServer = "InvalidateMissingServer"

    @classmethod
    def bool_procedures(cls) -> list[typing.Self]:
        return [
            DBProcedure.CheckAppCommandExist,
            DBProcedure.CheckUserExist,
        ]

    @classmethod
    def int_procedures(cls) -> list[typing.Self]:
        return [
            DBProcedure.CheckXPTime,
            DBProcedure.GetUserXp,
        ]

    @classmethod
    def list_procedures(cls) -> list[typing.Self]:
        return [
            DBProcedure.GetServers,
        ]

    @classmethod
    def returning_procedures(cls) -> list[typing.Self]:
        return [
            *DBProcedure.bool_procedures(),
            *DBProcedure.int_procedures(),
            *DBProcedure.list_procedures(),
        ]

    @classmethod
    def returning_many_procedures(cls) -> list[typing.Self]:
        return [*DBProcedure.list_procedures()]

    @classmethod
    def non_returning_procedures(cls) -> list[typing.Self]:
        return [
            DBProcedure.AddNewAppCommand,
            DBProcedure.AddNewServer,
            DBProcedure.AddNewUser,
            DBProcedure.IncreaseXP,
            DBProcedure.IncrementAppCommandUsage,
            DBProcedure.InvalidateMissingServer,
        ]


_BoolProcedures = typing.Literal[
    DBProcedure.CheckAppCommandExist,
    DBProcedure.CheckUserExist,
]
_IntProcedures = typing.Literal[
    DBProcedure.CheckXPTime,
    DBProcedure.GetUserXp,
]
_ListProcedures = typing.Literal[
    DBProcedure.GetServers,
]
_NoReturnProcedures = typing.Literal[
    DBProcedure.AddNewAppCommand,
    DBProcedure.AddNewServer,
    DBProcedure.AddNewUser,
    DBProcedure.IncreaseXP,
    DBProcedure.IncrementAppCommandUsage,
    DBProcedure.InvalidateMissingServer,
]


@typing.overload
def dbcallprocedure(
    pool: mariadb.ConnectionPool,
    procedure: _BoolProcedures,
    *,
    params: tuple[typing.Any, ...] = (),
) -> bool:
    ...


@typing.overload
def dbcallprocedure(
    pool: mariadb.ConnectionPool,
    procedure: _IntProcedures,
    *,
    params: tuple[typing.Any, ...] = (),
) -> int:
    ...


@typing.overload
def dbcallprocedure(
    pool: mariadb.ConnectionPool,
    procedure: _ListProcedures,
    *,
    params: tuple[typing.Any, ...] = (),
) -> list[dict[str, typing.Any]]:
    ...


@typing.overload
def dbcallprocedure(
    pool: mariadb.ConnectionPool,
    procedure: _NoReturnProcedures,
    *,
    params: tuple[typing.Any, ...] = (),
) -> None:
    ...


def dbcallprocedure(
    pool: mariadb.ConnectionPool,
    procedure: DBProcedure,
    *,
    params: tuple[typing.Any, ...] = (),
) -> bool | int | list[dict[str, typing.Any]] | None:
    """Calls a stored procedure with the given parameters.

    If the procedure returns several results, the returned list will contain dicts representing each row, where the
    dict key will be the field name, and the dict value will be the field's value.

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
    returns_many = procedure in DBProcedure.returning_many_procedures()
    with pool.get_connection() as pconn:
        with pconn.cursor(dictionary=returns_many) as cursor:
            cursor.callproc(procedure, params)
            if returns:
                if returns_many:  # stored procedure returns more than one row of results
                    result = cursor.fetchall()
                else:
                    # we can be certain that the return value is at index [0] from all simple stored procedures
                    result = cursor.fetchone()[0]
        pconn.commit()
    if returns and result is not None:
        return result


def checkdbforuser(pool: mariadb.ConnectionPool, message: discord.Message):
    result = dbcallprocedure(pool, DBProcedure.CheckUserExist, params=(message.author.id,))
    if result:
        # entry for this user ID exists, proceed to check for last XP gain time, possibly awarding some new XP
        last_xp_gain = dbcallprocedure(pool, DBProcedure.CheckXPTime, params=(message.author.id,))
        unix_now = int(time.time())
        if unix_now - last_xp_gain > 120:
            # user got XP more than two minutes ago, award between 15 and 25 XP and update last XP gain time
            dbcallprocedure(pool, DBProcedure.IncreaseXP, params=(message.author.id, random.randint(15, 25), unix_now))
    else:
        # user is unknown to the database, add it with user ID and default in the other fields
        dbcallprocedure(pool, DBProcedure.AddNewUser, params=(message.author.id,))
