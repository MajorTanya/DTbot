import random
import time

import mysql.connector as mariadb
from discord.ext import commands
from mysql.connector import pooling

from launcher import db_config

# open the pooled connection used for everything but prefix checks
cnx = mariadb.pooling.MySQLConnectionPool(pool_size=10, pool_reset_session=True, **db_config)


def dbcallprocedure(procedure, *, returns: bool = False, params: tuple):
    db = cnx.get_connection()
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


def checkdbforuser(message):
    result = dbcallprocedure('CheckUserExist', returns=True, params=(message.author.id, '@res'))
    if result:
        # entry for this user ID exists, proceed to check for last XP gain time, possibly awarding some new XP
        last_xp_gain = dbcallprocedure('CheckXPTime', returns=True, params=(message.author.id, '@res'))
        unix_now = int(time.time())
        if unix_now - last_xp_gain > 120:
            # user got XP more than two minutes ago, award between 15 and 25 XP and update last XP gain time
            dbcallprocedure('IncreaseXP', params=(message.author.id, random.randint(15, 25), unix_now))
    else:
        # user is unknown to the database, add it with user ID and default in the other fields
        dbcallprocedure('AddNewUser', params=(message.author.id,))


class DatabaseManagement(commands.Cog, command_attrs=dict(hidden=True)):
    """Manages the DTbot MariaDB database"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.message.author)

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author == self.bot.user) or message.author.bot:
            return
        try:
            checkdbforuser(message)
        finally:
            pass
        pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        dbcallprocedure('AddNewServer', params=(guild.id, guild.member_count))

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        result = dbcallprocedure('CheckCommandExist', returns=True, params=(ctx.command.qualified_name, '@res'))
        if result:
            dbcallprocedure('IncrementCommandUsage', params=(ctx.command.qualified_name,))
        else:
            if ctx.command.cog_name is None:
                cog_name = "main"
            else:
                cog_name = ctx.command.cog_name
            dbcallprocedure('AddNewCommand', params=(ctx.command.qualified_name, cog_name))
            # because the command was used this one time, we increment the default value (0) by 1
            dbcallprocedure('IncrementCommandUsage', params=(ctx.command.qualified_name,))

    @commands.command(description="Manually adds an entry to the table 'users' of DTbot's database."
                                  "\nGenerally not required. Developers only.")
    async def adduserdata(self, ctx, user_id: int, user_xp: int, user_last_xp_gain: int, user_rep: int,
                          user_last_rep_awarded: int):
        params = (user_id, user_xp, user_last_xp_gain, user_rep, user_last_rep_awarded)
        try:
            dbcallprocedure('ManualNewUser', params=params)
            await ctx.send(f"Row added successfully to table `users` in database `{db_config['database']}`.")
        except mariadb.Error as err:
            self.bot.log.error(err)
        except Exception as e:
            self.bot.log.error(e)

    @commands.command(description="Manually cycles through the bot's servers to refresh the table 'servers' of the "
                                  "database.\nGenerally not required. Developers only.")
    async def refreshservers(self, ctx):
        for guild in self.bot.guilds:
            dbcallprocedure('AddNewServer', params=(guild.id, guild.member_count))
        await ctx.send('Server list refreshed.', delete_after=5)


def setup(bot):
    bot.add_cog(DatabaseManagement(bot))
