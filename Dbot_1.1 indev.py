from discord import Game
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import asyncio
import time
import datetime


bot = commands.Bot(command_prefix='+')

#client = ('bot')

#commands

@bot.command(name='8ball',
             description="Answers a yes/no question.",
             brief="Answers from the beyond.")
async def eightball():
        possible_responses = [
                'Yes',
                'Maybe',
                'No',
                'Probably',
                'Nah',
                'No way',
                'Nope'
                ]
        await bot.say(random.choice(possible_responses))


@bot.group(pass_context=True,
           description="Bitch slaps someone",
           brief="Bitch slaps someone",
           aliases=['Bitchslap'])
async def bitchslap(ctx, user: discord.Member):
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got a bitch slap.".format(user.mention) + "\n\n[Image link](https://i.imgur.com/bTGigCv.gif)")
        embed.set_image(url="https://i.imgur.com/bTGigCv.gif")
        await bot.say(embed=embed)



@bot.group(description="Something Berend says a lot",
           brief="THE BEREND THING",
           aliases=['Berend'])
async def berend():
        await bot.say('I am watching porn.')


@bot.group(pass_context=True,
           description="Kiss someone the non-romantic way",
           brief="A non-romantic kiss")
async def bkiss(ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/AtEvIWI.jpg',
                'https://i.imgur.com/IFeaAkR.jpg'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got kissed.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await bot.say(embed=embed)

    
@bot.group(description="Try and see",
           brief="Try and see")
async def bitcoin():
        await bot.say('Have a bitcoin.')


@bot.group(pass_context=True,
           description="Cuddle someone",
           brief="Cuddle someone")
async def cuddle(ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/7zdANGl.jpg',
                'https://i.imgur.com/IFeaAkR.jpg',
                'https://i.imgur.com/AtEvIWI.jpg'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got cuddled.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await bot.say(embed=embed)


@bot.group(pass_context=True,
           description="Cage someone",
           brief="Cage someone")
async def cage(ctx, user: discord.Member):
        await bot.say('**{}** got caged'.format(user.display_name))
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got caged.".format(user.mention))
        await bot.say(embed=embed)



@bot.command(description="Flips a coin",
             brief="Flip a coin")
async def coinflip():
        possible_responses = [
                'Heads',
                'Tails'
                ]
        await bot.say(random.choice(possible_responses))


@bot.group(description="SAY BLESS YOU TO THE CAT",
           brief="catsneeze",
           aliases=['Cat'])
async def cat():
        await bot.say('<:catsneeze:413201357223493633> <:catsneeze:413201357223493633> <:catsneeze:413201357223493633> <:catsneeze:413201357223493633> <:catsneeze:413201357223493633>')

        
@bot.command(description="Rolls a die",
             brief="Rolls a die",
             aliases=['roll'])
async def dice():
        possible_responses = [
                '1',
                '2',
                '3',
                '4',
                '5',
                '6',
                'No dice'
                ]
        await bot.say(random.choice(possible_responses))


@bot.group(description="Something Demon says a lot",
           brief="THE DEMON THING",
           aliases=['Demon'])
async def demon():
        await bot.say('Fucking bitch')


@bot.group(pass_context=True,
           description="Hug someone",
           brief="Hug someone")
async def hug(ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/wiAW9r6.gif',
                'https://i.imgur.com/wjJvhId.gif',
                'https://i.imgur.com/kCe5Bcl.jpg',
                'https://i.imgur.com/BcabNdw.png',
                'https://i.imgur.com/I6dF7Jk.gif',
                'https://i.imgur.com/75k34aJ.png'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got hugged.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await bot.say(embed=embed)
     

@bot.group(description="Something Ian says a lot",
           brief="THE IAN THING",
           aliases=['Ian'])
async def ian():
        await bot.say('XD')


@bot.group(description="Something Joey says a lot",
           brief="THE JOEY THING",
           aliases=['Joey', 'shadow', 'Shadow'])
async def joey():
        await bot.say('<.<')
        await bot.say('>.>')


@bot.group(description="Something Josh says a lot",
           brief="THE JOSH THING",
           aliases=['Josh'])
async def josh():
        await bot.say('Remove kebab')


@bot.command(description="Actually you can't",
             brief="Kill yourself")
async def kms():
        await bot.say('NO') 


@bot.group(pass_context=True,
           description="What do you think it does",
           brief="It's in the name")
async def kill(ctx, user: discord.Member):
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got killed.".format(user.mention))
        await bot.say(embed=embed)



@bot.group(pass_context=True,
           description="Kiss someone",
           brief="Kiss someone")
async def kiss(ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/nqyZPn9.jpg',
                'https://i.imgur.com/EtaXopA.jpg',
                'https://i.imgur.com/1Suhkjm.jpg'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got kissed.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await bot.say(embed=embed)
    

@bot.group(pass_context=True,
           description="For something LEWD",
           brief="LEWD")
async def lewd(ctx, user: discord.Member):
        await bot.say('Why you gotta be so lewd, **{}**?'.format(user.display_name))


@bot.group(description="Something Nishi says a lot",
           brief="THE NISHI THING",
           aliases=['Nishi', 'Nisher', 'nisher', 'Nishnish', 'nishnish'])
async def nishi():
        await bot.say('I will peg Berend, Zero, Shaggy, Rech, and Fichte.')


@bot.group(description="Something Neo says a lot",
           brief="THE NEO THING",
           aliases=['Neo'])
async def neo():
        await bot.say('Poof')


@bot.group(pass_context=True,
           description="Pat someone",
           brief="Pat someone")
async def pat(ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/pUeah8O.gif',
                'https://i.imgur.com/OtW9yBs.gif',
                'https://i.imgur.com/7C5jWYq.gif',
                'https://i.imgur.com/T6Y2L3u.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got a pat.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await bot.say(embed=embed)


@bot.group(pass_context=True,
           description="Pinch someone's cheeks",
           brief="Pinch someone's cheeks")
async def pinch(ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/i18Rwv9.gif',
                'https://i.imgur.com/KpJfzMb.gif',
                'https://i.imgur.com/w69MBcW.gif',
                'https://i.imgur.com/yEJnATT.gif',
                'https://i.imgur.com/czAJdZR.gif',
                'https://i.imgur.com/XUJZJva.gif',
                'https://i.imgur.com/5MsZXap.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got their cheeks pinched.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await bot.say(embed=embed)


#@bot.group(description="I was lazy and didnt add it",
#           brief="Pong")
#async def ping():
#        await bot.say('Sorry, demon was just too lazy to implement this.')
#        await bot.say('pong :ping_pong:')

@bot.command(pass_context=True,
             description="Pong",
             brief="Pong")
@commands.has_any_role("The Dark Lords", "Administrator", "Tanya")
@commands.cooldown(3, 30, commands.BucketType.server)
async def ping(ctx):
        time_then = time.monotonic()
        pinger = await bot.say('__*`Pinging...`*__')
        ping = '%.2f' % (1000*(time.monotonic()-time_then))
        await bot.edit_message(pinger, ':ping_pong: \n **Pong!** __**`' + ping + 'ms`**__')
        ping = 0


@bot.group(pass_context=True,
           description="Poke someone",
           brief="Poke someone")
async def poke(ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/bIcjhXJ.gif',
                'https://i.imgur.com/h6ddy0V.gif',
                'https://i.imgur.com/7C5jWYq.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got poked.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await bot.say(embed=embed)


@bot.group(pass_context=True,
           description="Someone gonna get punched",
           brief="Punch club")
async def punch(ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/xw9CG0q.gif',
                'https://i.imgur.com/sgXNkUd.gif',
                'https://i.imgur.com/eWQQGja.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got punched.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await bot.say(embed=embed)


@bot.group(description="A random quote from the server",
           brief="Quote me")
async def quote():
        possible_responses = [
                'https://imgur.com/60hKnCs',
                'https://imgur.com/pBGlIed',
                'https://imgur.com/N3TrhhH',
                'https://imgur.com/k2Ipuil',
                'https://imgur.com/ezJb1z1',
                'https://imgur.com/JXr2X90',
                'https://imgur.com/rlu9Iyc',
                'https://imgur.com/Iiwd3wR',                
                'https://imgur.com/o9n988v',                
                'https://imgur.com/HQW8qQM',                
                'https://imgur.com/bdM5nsm',
                'https://imgur.com/KupYQlU',
                'https://imgur.com/QCU9WM5',
                'https://imgur.com/Z1ltrfi',
                'https://imgur.com/ffMEOLz',
                'https://imgur.com/Gg06uLg',
                'https://imgur.com/qX6yi7k',
                'https://imgur.com/jQuiT9Q',
                'https://imgur.com/WBay8cY',
                'https://imgur.com/HD7ZnrH',
                'https://imgur.com/w6UcH4w',
                'https://imgur.com/OXOsy2q',
                'https://imgur.com/IeMI9aW',
		'https://imgur.com/DQCSglA',
                'https://imgur.com/qmoirvy',
                'https://imgur.com/P7lxLp2',
                'https://imgur.com/sJoTstH',
                'https://imgur.com/zBWWip7',
                '<@287727207642693633> This is for you\nhttps://imgur.com/e6i9Y2n'
                ]
        await bot.say(random.choice(possible_responses))

@bot.command(description="It's Russian Roulette",
             brief="Play some Russian Roulette",
             aliases=['russianroulette'])
async def roulette():
        possible_responses = [
                'Dead',
                'Alive',
                'Alive',
                'Alive',
                'Alive'
                ]
        await bot.say(random.choice(possible_responses))

@bot.group(description="IT'S JUST A REEE BRO",
           brief="REEEEE")
async def re():
        await bot.say('REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')


@bot.group(pass_context=True,
           description="Slap 'em hard",
           brief="Slap someone")
async def slap(ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/DfRsmUY.gif',
                'https://i.imgur.com/yTTzzKv.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="{} got slapped.".format(user.mention) + "\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await bot.say(embed=embed)


@bot.command(description="WOW YOU MUST BE DUMB TO NOT GET THAT",
             brief="Gives you a random scenario")
async def scenario():
        possible_responses = [
                'Nishi now owns the server',
                'Zero sold you for a plane',
                'Berend made you watch bad porn',
                'Tanya killed you for hurting Nishi',
                'Josh removed a kebab',
                'You got hacked',
                '<.<',
                'Nishi just took over the world'
                ]
        await bot.say(random.choice(possible_responses))


@bot.group(description="Something Sophie says a lot",
           brief="THE SOPHIE THING",
           aliases=['Sophie'])
async def sophie():
        await bot.say('You have been diagnosed with the gay')


@bot.group(description="Something Shaggy says a lot",
           brief="THE SHAGGY THING",
           aliases=['Shaggy'])
async def shaggy():
        await bot.say('Heh')


@bot.group(description="Something Sam says a lot",
           brief="THE SAM THING",
           aliases=['Sam'])
async def sam():
        await bot.say('Howdy')


@bot.group(description="Something Tanya says a lot",
           brief="THE TANYA THING",
           aliases=['Tanya'])
async def tanya():
        await bot.say('Hurt Nishi and I will kill you.')


@bot.group(description="Something Toasted says a lot",
           brief="THE TOASTED THING",
           aliases=['Toasted'])
async def toasted():
        await bot.say(':egg::egg::egg::egg::egg::egg::egg::egg::egg::egg::egg::egg::egg::egg::egg:')


@bot.group(pass_context=True,
           description="Whip someone",
           brief="Whip someone")
async def whip(ctx, user: discord.Member):
        possible_responses = [
                'https://i.imgur.com/GBp5khP.gif',
                'https://i.imgur.com/kAtQ5oB.gif',
                'https://i.imgur.com/0LU52nw.gif',
                'https://i.imgur.com/9SbK1p7.gif'
                ]
        chosen = random.choice(possible_responses)
        embed = discord.Embed(colour=discord.Colour(0x5e51a8), description="Bow down, {}.".format(user.mention) + " Time for a whipping!\n\n[Image link](" + chosen + ")")
        embed.set_image(url="" + chosen + "")
        await bot.say(embed=embed)


@bot.group(description="Something White said that one time",
           brief="THE WHITE THING SHE SAID",
           aliases=['White'])
async def white():
        await bot.say('The voices in your head never end.')


@bot.group(description="Something Zero says a lot",
           brief="THE ZERO THING",
           aliases=['Zero'])
async def zero():
        await bot.say('Even if I drink all the water in the universe, I will still be thirsty.')


@bot.group(hidden=True,
           description="ZERO SPAM",
           brief="ZERO TIME")
async def zeroarmy():
        await bot.say('Zero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero\nZero Zero Zero Zero Zero')


@bot.group(description="Info about me, Dbot. Please take a look.",
           brief="Info about me")
async def info():
        embed=discord.Embed(title="Dbot's info", description="Hello, I'm <@427902715138408458>, a bot created by <@327763028701347840> for one server only.\nIf you have any requests or questions, please primarily ask <@274684924324347904>.\nYou can find a version of the code minus the server specific stuff here: https://github.com/angelgggg/Pbot\nThank you and have a good day.")
        await bot.say(embed=embed)

@bot.group(pass_context=True,
           description="Shows details on user, such as Name, Join Date, or Highest Role",
           brief="Get info on a user",
           aliases=['uinfo'])
async def userinfo(ctx, user: discord.Member):
    
  embed = discord.Embed(title="{}'s info".format(user.name), description='Here is what I could find:', color=ctx.message.author.color)
  embed.add_field(name='Nickname', value='{}'.format(user.display_name))
  embed.add_field(name='ID', value='{}'.format(user.id), inline=True)
  embed.add_field(name='Status', value='{}'.format(user.status), inline=True)
  embed.add_field(name='Highest Role', value='<@&{}>'.format(user.top_role.id), inline=True)
  embed.add_field(name='Joined at', value='{:%d. %h \'%y at %H:%M}'.format(user.joined_at), inline=True)
  embed.add_field(name='Created at', value='{:%d. %h \'%y at %H:%M}'.format(user.created_at), inline=True)
  embed.add_field(name='Discriminator', value='{}'.format(user.discriminator), inline=True)
  embed.add_field(name='Playing', value='{}'.format(user.game))
  embed.set_footer(text="{}'s Info".format(user.name), icon_url='{}'.format(user.avatar_url))
  embed.set_thumbnail(url=user.avatar_url)

  
  await bot.say(embed=embed)


#online confirmation
@bot.event
async def on_ready():
        await bot.change_presence(game=Game(name="+help"))
        print(bot.user.name)
        print('online')
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
   
bot.run('')

