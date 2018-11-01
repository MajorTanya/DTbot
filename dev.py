import discord
from discord.ext import commands

from DTbot import dev_set, sdb_code


class Dev():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True,
                      pass_context=True,
                      description="Lists all servers that DTbot is a member of. Developers only.",
                      brief="Full server list of DTbot. Developers only.")
    async def listservers(self, ctx):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            serverlist = list()
            servers = list(self.bot.servers)
            server_count = len(servers)
            reporting_channel = self.bot.get_channel('441445205678358529')
            embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="A list of all the servers " + self.bot.user.name + " is a member of")
            embed.set_footer(text="Total server count: " + str(server_count))
            for x in range(server_count):
                serverlist.append(servers[x-1].name)
            stringle = '\n'.join(serverlist)
            embed.add_field(name="Servers", value=stringle)
            await self.bot.send_message(reporting_channel, embed=embed)


    @commands.command(hidden=True,
                      pass_context=True,
                      description="Can load additional extensions into DTbot. Developers only.",
                      brief="Load an extension. Developers only.")
    async def load(self, ctx, extension_name: str):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            try:
                self.bot.load_extension(extension_name)
            except (AttributeError, ImportError) as e:
                await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
                return
            await self.bot.say("{} loaded.".format(extension_name))
        else:
            await self.bot.say("Insufficient permissions to modify the loadout of DTbot.")


    @commands.command(hidden=True,
                      pass_context=True,
                      description="Unload an extension. Developers only.",
                      brief="Unload an extension. Developers only.")
    async def unload(self, ctx, extension_name: str):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            self.bot.unload_extension(extension_name)
            await self.bot.say("Module `{}` unloaded.".format(extension_name))


    @commands.command(hidden=True,
                      pass_context=True,
                      description="First unload and then immediately reload a module. Developers only.",
                      brief="Reload an extension. Developers only.")
    async def reload(self, ctx, extension_name: str):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            self.bot.unload_extension(extension_name)
            await self.bot.say("{} unloaded.".format(extension_name))
            try:
                self.bot.load_extension(extension_name)
            except (AttributeError, ImportError) as e:
                await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
                return
            await self.bot.say("{} loaded.".format(extension_name))


    @commands.command(hidden=True,
                      pass_context=True,
                      description='Shutdown command for the bot. Developers only.',
                      brief='Shutdown the bot. Developers only.')
    async def shutdownbot(self, ctx, passcode: str):
        userroles = set()
        for role in ctx.message.author.roles:
            userroles.add(role.id)
        if not dev_set.isdisjoint(userroles):
            if passcode == sdb_code:
                await self.bot.logout()
            else:
                return


def setup(bot):
    bot.add_cog(Dev(bot))
