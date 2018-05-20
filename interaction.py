import random
import discord
from discord.ext import commands

class Interaction():
    """Commands which interact with others"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True,
                      description="Bitch slaps someone",
                      brief="Bitch slaps someone",
                      aliases=['Bitchslap'])
    async def bitchslap(self, ctx, user: discord.Member):
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got a bitch slap.".format(user.mention) + "\n\n[Image link](https://i.imgur.com/bTGigCv.gif)")
        embed.set_image(url="https://i.imgur.com/bTGigCv.gif")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Kiss someone the non-romantic way",
                      brief="A non-romantic kiss")
    async def bkiss(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/AtEvIWI.jpg',
                'https://i.imgur.com/IFeaAkR.jpg'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got kissed.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Blush",
                      brief="Blush")
    async def blush(self, ctx):
        possible_responses = [
                'https://i.imgur.com/5d4EtC7.gif',
                'https://i.imgur.com/VlkficM.gif',
                'https://i.imgur.com/SrBENaT.gif',
                'https://i.imgur.com/51oJ8DP.gif',
                'https://i.imgur.com/N4u4D4Q.gif',
                'https://i.imgur.com/MwMD8Ma.gif',
                'https://i.imgur.com/jDUYhHe.gif',
                'https://i.imgur.com/aRbQjjd.gif',
                'https://i.imgur.com/54lcIDr.gif',
                'https://i.imgur.com/CTK6JcI.gif',
                'https://i.imgur.com/etIOF6J.gif',
                'https://i.imgur.com/9dJjBok.gif',
                'https://i.imgur.com/CG61JYj.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} blushed! How cute!".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Cuddle someone",
                      brief="Cuddle someone")
    async def cuddle(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/7zdANGl.jpg',
                'https://i.imgur.com/Yv1vzs8.gif',
                'https://i.imgur.com/ssEihPL.gif',
                'https://i.imgur.com/Smw9dWd.gif',
                'https://i.imgur.com/VU6ZtyK.gif',
                'https://i.imgur.com/5UFTH4e.gif',
                'https://i.imgur.com/3xL3xOp.gif',
                'https://i.imgur.com/ufyssIG.gif',
                'https://i.imgur.com/7Gvgzpa.gif',
                'https://i.imgur.com/QMfcwVh.gif',
                'https://i.imgur.com/juPh4SS.gif',
                'https://i.imgur.com/qrE8NgM.gif',
                'https://i.imgur.com/PnA0l5s.gif',
                'https://i.imgur.com/3n65uZZ.gif',
                'https://i.imgur.com/dXcW5FZ.gif',
                'https://i.imgur.com/GFjVEhK.gif',
                'https://i.imgur.com/pd60o2N.gif',
                'https://i.imgur.com/FiVYGOt.gif',
                'https://i.imgur.com/qMC5eMR.gif',
                'https://i.imgur.com/QWCjCcS.gif',
                'https://i.imgur.com/EAjbxc1.gif',
                'https://i.imgur.com/n2W3s4w.gif',
                'https://i.imgur.com/9618Een.gif',
                'https://i.imgur.com/vZrnDMZ.gif',
                'https://i.imgur.com/P7nr3g7.gif',
                'https://i.imgur.com/2LMoGHb.gif',
                'https://i.imgur.com/DGpmONM.gif',
                'https://i.imgur.com/ikAgEjS.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got cuddled.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Cage someone",
                      brief="Cage someone")
    async def cage(self, ctx, user: discord.Member):
        possible_responses = [
              'https://i.imgur.com/VW0qjFL.jpg',
              'https://i.imgur.com/zn1jItN.jpg',
              'https://i.imgur.com/WHY04lb.jpg',
              'https://i.imgur.com/DLcfCy0.jpg'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got caged.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="High five someone",
                      brief="High five someone",
                      aliases=['5'])
    async def highfive(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/DdLVhQl.gif',
                'https://i.imgur.com/DS27ujM.gif',
                'https://i.imgur.com/zOA0axl.gif',
                'https://i.imgur.com/1yNYgxt.gif',
                'https://i.imgur.com/P2bOnRD.gif',
                'https://i.imgur.com/MmxehbX.gif',
                'https://i.imgur.com/7D2HdEV.gif',
                'https://i.imgur.com/wu9fRh7.gif',
                'https://i.imgur.com/1d7Htb8.gif',
                'https://i.imgur.com/jLeYpIP.gif',
                'https://i.imgur.com/AJC39Sj.gif',
                'https://i.imgur.com/ESmtHHi.gif',
                'https://i.imgur.com/O5kxmby.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + " got a high five from {}.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Hug someone",
                      brief="Hug someone")
    async def hug(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/wiAW9r6.gif',
                'https://i.imgur.com/wjJvhId.gif',
                'https://i.imgur.com/kCe5Bcl.jpg',
                'https://i.imgur.com/BcabNdw.png',
                'https://i.imgur.com/I6dF7Jk.gif',
                'https://i.imgur.com/75k34aJ.png',
                'https://i.imgur.com/u7ADDIf.gif',
                'https://i.imgur.com/MymLTif.gif',
                'https://i.imgur.com/rYJ7jd1.gif',
                'https://i.imgur.com/FeRFRdg.gif',
                'https://i.imgur.com/qGpIWAw.gif',
                'https://i.imgur.com/PImjH6C.gif',
                'https://i.imgur.com/Y5FgKIs.gif',
                'https://i.imgur.com/bEHkvAl.gif',
                'https://i.imgur.com/WVxUM2i.gif',
                'https://i.imgur.com/ejJuHlg.gif',
                'https://i.imgur.com/0aNrj7n.gif',
                'https://i.imgur.com/4BUS10Z.gif',
                'https://i.imgur.com/gTgkq5I.gif',
                'https://i.imgur.com/GTs6esu.gif',
                'https://i.imgur.com/U1uupRT.gif',
                'https://i.imgur.com/dkcSG2z.gif',
                'https://i.imgur.com/5RWjDeE.gif',
                'https://i.imgur.com/0lavkJS.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got hugged.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Kiss someone",
                      brief="Kiss someone")
    async def kiss(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/nqyZPn9.jpg',
                'https://i.imgur.com/EtaXopA.jpg',
                'https://i.imgur.com/1Suhkjm.jpg',
                'https://i.imgur.com/fleBrUm.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got kissed.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
           description="Pat someone",
           brief="Pat someone")
    async def pat(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/pUeah8O.gif',
                'https://i.imgur.com/OtW9yBs.gif',
                'https://i.imgur.com/7C5jWYq.gif',
                'https://i.imgur.com/T6Y2L3u.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got a pat.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Pinch someone's cheeks",
                      brief="Pinch someone's cheeks")
    async def pinch(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/i18Rwv9.gif',
                'https://i.imgur.com/KpJfzMb.gif',
                'https://i.imgur.com/w69MBcW.gif',
                'https://i.imgur.com/yEJnATT.gif',
                'https://i.imgur.com/czAJdZR.gif',
                'https://i.imgur.com/XUJZJva.gif',
                'https://i.imgur.com/5MsZXap.gif',
                'https://i.imgur.com/j1WqEzI.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got their cheeks pinched.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Poke someone",
                      brief="Poke someone")
    async def poke(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/bIcjhXJ.gif',
                'https://i.imgur.com/h6ddy0V.gif',
                'https://i.imgur.com/7C5jWYq.gif',
                'https://i.imgur.com/TgdGQji.gif',
                'https://i.imgur.com/wfH2tpV.gif',
                'https://i.imgur.com/wz6netM.gif',
                'https://i.imgur.com/5WE4RmD.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got poked.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Someone gonna get punched",
                      brief="Punch club")
    async def punch(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/xw9CG0q.gif',
                'https://i.imgur.com/sgXNkUd.gif',
                'https://i.imgur.com/eWQQGja.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got punched.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Slap 'em hard",
                      brief="Slap someone")
    async def slap(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/DfRsmUY.gif',
                'https://i.imgur.com/yTTzzKv.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got slapped.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Stab someone",
                      brief="Stab someone")
    async def stab(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/Jf597ta.gif',
                'https://i.imgur.com/WW9bFux.gif',
                'https://i.imgur.com/acmB9dg.gif',
                'https://i.imgur.com/lTTz2Zr.gif',
                'https://i.imgur.com/X9Ltb40.gif',
                'https://i.imgur.com/tlZ3wbY.gif',
                'https://i.imgur.com/at3GzKc.gif',
                'https://i.imgur.com/HfKOknc.gif',
                'https://i.imgur.com/boqQnRk.gif',
                'https://i.imgur.com/v7eAScr.gif',
                'https://i.imgur.com/5nlpyoc.gif',
                'https://i.imgur.com/4sJBxh6.gif',
                'https://i.imgur.com/MHAdhmy.gif',
                'https://i.imgur.com/DLLOHhv.gif',
                'https://i.imgur.com/goFfJot.gif',
                'https://i.imgur.com/0gbigx6.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + " got stabbed by {}.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="Whip someone",
                      brief="Whip someone")
    async def whip(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/GBp5khP.gif',
                'https://i.imgur.com/kAtQ5oB.gif',
                'https://i.imgur.com/0LU52nw.gif',
                'https://i.imgur.com/9SbK1p7.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="Bow down, {}.".format(user.mention) + " Time for a whipping!\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="What do you think it does",
                      brief="It's in the name")
    async def kill(self, ctx, user: discord.Member):
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got killed.".format(user.mention))
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True,
                      description="For something LEWD",
                      brief="LEWD")
    async def lewd(self, ctx, user: discord.Member = None):
        if user:
                await self.bot.say('Why you gotta be so lewd, **{}**?'.format(user.display_name))
        else:
                await self.bot.say('Why you gotta be so lewd?')


    @commands.command(pass_context=True,
           description="Glomp someone",
           brief="Glomp someone")
    async def glomp(self, ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/bTEt1M0.gif',
                'https://i.imgur.com/EeYf3KO.gif',
                'https://i.imgur.com/5d61E06.gif',
                'https://i.imgur.com/XBMmfMy.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{}".format(user.mention) + " got a glomp from {}.".format(ctx.message.author.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Interaction(bot))
