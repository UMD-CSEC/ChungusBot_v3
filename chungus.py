import discord
from discord.ext import commands, tasks
from secret import FLAG, SECRET_FLAG, discord_token
import help_info
import random

##################################### IDK ######################################
intents = discord.Intents().all()
bot = commands.Bot(command_prefix = '---> ', intents=intents)
bot.remove_command('help')

l = len(FLAG)
flags = [FLAG[0:l//4], FLAG[l//4:2*l//4], FLAG[2*l//4:3*l//4], FLAG[3*l//4:]]
assert "".join(flags) == FLAG
print(f'flags = {flags} --- {"".join(flags)}')

#################################### EVENTS ####################################
@bot.event # Show banner and add members to respective guilds in db
async def on_ready():
    print("\n|--------------------|")
    print(f"|  {bot.user.name} - Online   |")
    print(f"|  discord.py {discord.__version__}  |")
    print("|--------------------|")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="My code is somewhere"))

@bot.event # Displays error messages
async def on_command_error(ctx, error):
    msg = ""
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        msg += "Missing a required argument. Display the help menu to see what commands you can run\n"
    if isinstance(error, commands.MissingPermissions):
        msg += "You do not have the appropriate permissions to run this command.\n"
    if isinstance(error, commands.BotMissingPermissions):
        msg += "I don't have sufficient permissions!\n"
    if msg == "":
        if not isinstance(error, commands.CheckFailure):
            msg += "Something went wrong.\n"
            print("error not caught")
            print(error)
            await ctx.send(msg)
    else:
        await ctx.send(msg)

@bot.event
async def on_message(ctx):
    if ctx.author.bot:
        return
    else:
        print(f'msg: {ctx.content}')
        print(str(ctx.content).encode())
        print(str(ctx.content) == ":rofl:")
        if ctx.content == "https://tenor.com/view/sigma-sigma-male-sigma-rule-b2k-sigma-expression-gif-27239871":
            print("here")
            if str(ctx.channel.type) == "private":
                await ctx.channel.send(f'flag0: `{flags[0]}`')
        else:
            await bot.process_commands(ctx)

################################## HELPERS ###################################
def in_dms():
    async def tocheck(ctx):
        # A check for ctf context specific commands
        return str(ctx.channel.type) == "private"
    return commands.check(tocheck)
    
def in_bot_channel():
    async def tocheck(ctx):
        # A check for ctf context specific commands
        return str(ctx.channel.id)  == "1072348075877740634" # Test CTFBot server - chungus_v3 channel
    return commands.check(tocheck)


################################## COMMANDS ###################################
@bot.command()
async def help(ctx, page=None):
    if page == None:
        emb = discord.Embed(description=help_info.help_page, colour=10181046)
    emb.set_author(name='ChungusBot v3 Help')
    await ctx.channel.send(embed=emb)

@bot.command()
@in_dms()
async def flip(ctx, one, two, three):
    flips = [random.randint(0,1) for _ in range(3)]
    guesses = [one, two, three]
    guesses = [0 if g.lower() == "tails" else 1 for g in guesses]

    # I could have made the probability worse here. count your blessings
    if flips == guesses:
        await ctx.channel.send(f'flag1: `{flags[1]}`')
    else:
        msgs = ["wrong", "incorrect", "guess better", "better luck next time"]
        await ctx.channel.send(random.choice(msgs))


@bot.command()
@in_dms()
async def numbers(ctx, a: int, b: int, c: int, d: int):
    #a,b,c,d = int(a)
    if a+b+c+d > 4000 and ((a+b)*(c+d)) % 1337 == 25:
        await ctx.channel.send(f'flag2: `{flags[2]}`')

@bot.command()
@in_dms()
async def bee(ctx, test=None):
    print(f'test = {test}')
    a = ctx.message.attachments
    if len(a) == 1:
        script = await a[0].read()

        # yes, I know. My requirements for a "bee movie script" are pretty low... don't judge
        if b"You like jazz?" in script and len(script) >= 100:
            await ctx.channel.send(f'flag3: `{flags[3]}`')

@bot.command()
@in_bot_channel()
async def gimme(ctx, da=None, fl=None, pl=None):
    if da == "da" and fl == "flag":
        if pl == "please":
            await ctx.channel.send(f'here you go: <{SECRET_FLAG}>')
        else:
            await ctx.channel.send(f'only if you say "please"')


##################################### MAIN #####################################
if __name__ == '__main__': 
    bot.run(discord_token)
