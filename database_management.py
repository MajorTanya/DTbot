import random
import time

import mysql.connector as mariadb
from discord.ext import commands

from dev import dev_set
from launcher import cnx, logger, DB_NAME


def checkdbforuser(message):
    db = cnx.get_connection()
    cursor = db.cursor()
    result = cursor.callproc('CheckUserExist', (message.author.id, '@res'))[1]
    if result:
        # entry for this user ID exists, proceed to check for last XP gain time, possibly awarding some new XP
        last_xp_gain = cursor.callproc('CheckXPTime', (message.author.id, '@res'))[1]
        unix_now = int(time.time())
        if unix_now - last_xp_gain > 120:
            # user got XP more than two minutes ago, award between 15 and 25 XP and update last XP gain time
            cursor.callproc('IncreaseXP', (message.author.id, random.randint(15, 25), unix_now))
            db.commit()
    else:
        # user is unknown to the database, add it with user ID and default in the other fields
        cursor.callproc('AddNewUser', (message.author.id,))
        db.commit()
    db.close()


class DatabaseManagement(commands.Cog, command_attrs=dict(hidden=True)):
    """Manages the DTbot MariaDB database"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        userroles = set()
        for role in ctx.author.roles:
            userroles.add(str(role.id))
        return not dev_set.isdisjoint(userroles)

    @commands.Cog.listener()
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

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = cnx.get_connection()
        cursor = db.cursor()
        cursor.callproc('AddNewServer', (guild.id, guild.member_count))
        db.commit()
        db.close()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        db = cnx.get_connection()
        cursor = db.cursor()
        result = cursor.callproc('CheckCommandExist', (ctx.command.qualified_name, '@res'))[1]
        if result:
            cursor.callproc('IncrementCommandUsage', (ctx.command.qualified_name,))
            db.commit()
        else:
            if ctx.command.cog_name is None:
                cog_name = "main"
            else:
                cog_name = ctx.command.cog_name
            cursor.callproc('AddNewCommand', (ctx.command.qualified_name, cog_name))
            db.commit()
            # because the command was used this one time, we increment the default value (0) by 1
            cursor.callproc('IncrementCommandUsage', (ctx.command.qualified_name,))
            db.commit()
        db.close()

    @commands.command(description="Manually adds an entry to the table 'users' of DTbot's database."
                                  "\nGenerally not required. Developers only.")
    async def adduserdata(self, ctx, user_id: int, user_xp: int, user_last_xp_gain: int, user_rep: int,
                          user_last_rep_awarded: int):
        db = cnx.get_connection()
        cursor = db.cursor()
        params = (user_id, user_xp, user_last_xp_gain, user_rep, user_last_rep_awarded)
        try:
            cursor.callproc('ManualNewUser', params)
            db.commit()
            await ctx.send(f"Row added successfully to table `users` in database `{DB_NAME}`.")
        except mariadb.Error as err:
            logger.error(err)
        except Exception as e:
            logger.error(e)
        db.close()

    @commands.command(description="Manually changes the prefix a server wants to use for DTbot."
                                  "\nNeeds to be 1-3 characters in length.\nCurrently not in use. Developers only.",
                      aliases=['csp', 'changeprefix'],
                      rest_is_raw=True)
    async def changeserverprefix(self, ctx, *newprefix: str):
        newprefix = ''.join(newprefix)
        if len(newprefix) <= 3:
            db = cnx.get_connection()
            cursor = db.cursor()
            cursor.callproc('ChangeServerPrefix', (ctx.message.guild.id, newprefix))
            db.commit()
            db.close()
        else:
            await ctx.send("Invalid prefix length (max. 3 characters)")

    @commands.command(description="Manually cycles through the bot's servers to refresh the table 'servers' of the "
                                  "database.\nGenerally not required. Developers only.")
    async def refreshservers(self, ctx):
        db = cnx.get_connection()
        cursor = db.cursor()
        for guild in self.bot.guilds:
            cursor.callproc('AddNewServer', (guild.id, guild.member_count))
            db.commit()
        db.close()
        await ctx.send('Server list refreshed.', delete_after=5)

    @commands.command(description="Manually resets the prefix a server wants to use for DTbot to the default."
                                  "\nCurrently not in use. Developers only.")
    async def resetserverprefix(self, ctx):
        db = cnx.get_connection()
        cursor = db.cursor()
        cursor.callproc('ChangeServerPrefix', (ctx.message.guild.id, '+'))
        db.commit()
        db.close()


def setup(bot):
    bot.add_cog(DatabaseManagement(bot))
