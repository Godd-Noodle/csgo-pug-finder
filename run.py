import discord
from discord.ext import commands
from discord.utils import get
import urllib.request, urllib.error, urllib.parse
from discord.ext.commands import has_role




import json

# read file
with open("credentials_discord.json", 'r') as myfile:
    data=myfile.read()

# parse file
creds_discord = json.loads(data)
#print(creds_discord)


TOKEN = str(creds_discord["TOKEN"])
PREFIX = str(creds_discord["PREFIX"])


urlFaceitStats = "https://faceitstats.com/player,"
urlSteam = "https://steamcommunity.com/profiles/"

bot = commands.Bot(command_prefix=PREFIX)

#bot.remove_command("help")


@bot.event
async def on_ready():
    #activity = discord.Game(name="with the laws of reality", type=3)
    await bot.change_presence(status=discord.Status.do_not_disturb)# , activity = activity
    print("Bot is ready")

@bot.command(name = "ready")
async def ready(ctx):

    authorRoles = ", ".join([str(r.name) for r in ctx.author.roles])
    print(authorRoles)
    readyRole = get(ctx.message.guild.roles, name='Ready')
    if not  authorRoles.find("Ready") == -1:
        await ctx.author.remove_roles(readyRole)
    else:
        
        await ctx.author.add_roles(readyRole)

    

    
@bot.command(name = "roles")
async def roles(ctx):
    print(", ".join([str(r.name) for r in ctx.guild.roles]))
    print(ctx.guild.roles)

    for role in ctx.author.roles:
        print(str(role))

@bot.command(name = "ping")
async def respond(ctx):
    await ctx.send('pong')
    print(f"{str(ctx.author)} sent command !ping")

@bot.command(name = "quit")
@commands.is_owner()
@commands.dm_only()
async def close(ctx):
    await ctx.send("shutting down!!")
    await bot.change_presence(status=discord.Status.offline)
    await bot.close()

@bot.command(name = "verify", pass_context=True)
async def verify(ctx,arg):
    
    response = urllib.request.urlopen(urlFaceitStats +arg)
    
    webcontentfs = str(response.read())

    index = webcontentfs.find(urlSteam)


    if (index == -1):
        await ctx.send("This isnt a faceit profile")
        return
    i_e = webcontentfs[index:].find('"')

    urlSteamFull = webcontentfs[index:index+i_e]

    response = urllib.request.urlopen(urlSteamFull)
    
    webcontentsteam = str(response.read())
    
    
    
    p_s = webcontentsteam.find(str('<div class="profile_summary">'))
    p_e = webcontentsteam.find(str('<div class="profile_summary_footer">'))


    level_s = webcontentfs.find("level: <strong>")

    level = webcontentfs[level_s:level_s+20]

    level_filter = filter(str.isdigit, level)
    faceitLevel = "".join(level_filter)
    found = webcontentsteam[p_s:p_e].find(str(ctx.author))

    if (found == -1):
        await ctx.send(f"could not find your discord id '{ctx.author}'on this steam profile, ensure it has this so we can verify that it is your account we are linking to your faceit")
        return
    await ctx.send(f"Welcome {str(arg)}, thank you for verifying your account, you can now remove your discord tag from your steam account if you wish")
    roleLinked = discord.utils.get(ctx.author.guild.roles, name = "Linked")
    await ctx.author.add_roles(roleLinked)
    roleFaceitLevel = discord.utils.get(ctx.author.guild.roles, name = "FACEIT " + str(faceitLevel))
    await ctx.author.add_roles(roleFaceitLevel)
    if not (str(ctx.author) == "Godd_Noodle#3075"):

        await ctx.author.edit(nick=str(arg))
    #print(faceitLevel)  



        
@bot.command(name = "print")
async def print_all(ctx, arg):
    await ctx.channel.send(ctx.author)
    await ctx.channel.send(ctx.message)
    


#Past this point are event handlings

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please send in all required arguments")

@verify.error
async def verifyError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a FACEIT username to begin verification steps ")

bot.run(TOKEN)