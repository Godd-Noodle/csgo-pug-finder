import discord
from discord.ext import commands
from discord.utils import get
import urllib.request, urllib.error, urllib.parse
from  faceit import FaceitData
import discord.ext.commands.context as context
#from discord.ext.commands import has_role
import json

# read file
with open("credentials_discord.json", 'r') as myfile:
    data=myfile.read()

# parse file
creds_discord = json.loads(data)
#print(creds_discord)


TOKEN = str(creds_discord["TOKEN"])
PREFIX = "/"
FACEIT_TOKEN = str(creds_discord["FACEIT"])
URL = str(creds_discord["URL"])
PORT  =  str(creds_discord["PORT"])
USERNAME = str(creds_discord["USERNAME"])
PASSWORD = str(creds_discord["PASSWORD"])



intents = discord.Intents.all()
intents.members = True


urlSteam = "https://steamcommunity.com/profiles/"

bot = commands.Bot(command_prefix=PREFIX, intents=intents)




#bot.remove_command("help")


@bot.event
async def on_ready():
    #activity = discord.Game(name="with the laws of reality", type=3)
    await bot.change_presence(status=discord.Status.do_not_disturb)# , activity = activity
    print("Bot is ready")

@bot.event
async def on_reaction_add(ctx : context.Context, arg):
    if arg.id  == bot.user.id:
        return
    if ctx.message.channel.name == "live-lobbies" and ctx.emoji.id == 779068863672615012:
        #can now start edditing messages to add to q
        print("")
        if str(arg.id) in ctx.message.content:
            print("already in the message")
        else:
            pos = ctx.message.content.rfind(">")
            await ctx.edit(ctx, ctx.message[:pos] + str(arg.mention) + ctx.message[pos:])
    
    
    

@bot.command(name = "ready")
async def ready(ctx : context.Context):
    channel = "ready"
    if not str(ctx.channel) == channel:
        print(f"Not correct channel '{ctx.channel}', looking for '{channel}'")
        return


    authorRoles = [str(r.name) for r in ctx.author.roles]
    #print(authorRoles)
    readyRole = get(ctx.message.guild.roles, name='Ready')
    if readyRole in authorRoles:
        await ctx.author.remove_roles(readyRole)
    else:
        
        await ctx.author.add_roles(readyRole)
    
    await ctx.message.delete()


@bot.command(name = "roles")
@commands.is_owner()
async def roles(ctx : context.Context):
    print(", ".join([str(r.name) for r in ctx.guild.roles]))
    print(ctx.guild.roles)
    
    print(", ".join([str(r.name) for r in ctx.author.roles]))

@bot.command(name = "ping")
async def respond(ctx : context.Context):
    print(f"{str(ctx.author)} sent command {PREFIX}ping")
    channel = "bot"
    if not str(ctx.channel) == channel:
        print(f"Not correct channel '{ctx.channel}', looking for '{channel}'")
        return
    await ctx.send('pong')
    

@bot.command(name = "quit")
@commands.is_owner()
@commands.dm_only()
async def close(ctx : context.Context):
    print("bot shutting down")
    await ctx.send("shutting down!!")
    await bot.change_presence(status=discord.Status.offline)
    await bot.close()

@bot.command(name = "verify", pass_context=True)
async def verify(ctx : context.Context, arg):
    #Ask for faceit username

    channel = "verify"
    if not str(ctx.channel) == channel:
        print(f"Not correct channel '{ctx.channel}', looking for '{channel}'")
        return
    
    fd = FaceitData(FACEIT_TOKEN)
    
    match_details = FaceitData.player_details(fd,arg,"csgo")
    
    #print(match_details)
    elo = match_details["games"]["csgo"]["faceit_elo"]
    lvl = match_details["games"]["csgo"]["skill_level"]
    urlSteamFull = urlSteam +  match_details["steam_id_64"]

    await ctx.send(f"{elo},{lvl}")


    if (elo == 0):
        await ctx.send("`This isnt a faceit profile, please give your faceit username`")
        return

    
    #extract the steam summary and check if the discord tag exists in it
    response = urllib.request.urlopen(urlSteamFull)
    webcontentsteam = str(response.read())
    p_s = webcontentsteam.find(str('<div class="profile_summary">'))
    p_e = webcontentsteam.find(str('<div class="profile_summary_footer">'))
    found = str(ctx.author) in webcontentsteam[p_s:p_e]
    #print(found)


    if not found:
        await ctx.send(f"`could not find your discord id '{ctx.author}' on this steam profile's bio, ensure it has this so we can verify that it is your account we are linking to your FACEIT`")
        return
    

    print(lvl)

    roleLinked = get(ctx.author.guild.roles, name = "Linked")
    await ctx.author.add_roles(roleLinked)
    roleFaceitLevel = get(ctx.author.guild.roles, name = "Level " + str(lvl))
    await ctx.author.add_roles(roleFaceitLevel)
    
    
    await ctx.send(f"`Welcome {str(arg)}, thank you for verifying your account, you can now remove your discord tag from your steam account if you wish`")
    

    if ctx.author.id == ctx.guild.owner_id:
        await ctx.author.send(f"please set your nickname to '{str(arg)}', I dont seem to be able to myself\n(Perhaps you are the server owner)")
    else:
        await ctx.author.edit(nick=str(arg))


  
@bot.command(name = "print")
async def print_all(ctx : context.Context, arg):
    await ctx.channel.send(ctx.author)
    await ctx.channel.send(ctx.message)
    
#create lobby signups
@bot.command(name = "lobby")
async def lobby(ctx : context.Context, *arg):
    print("lobby function called")
    channel = "lobby"
    if not str(ctx.channel) == channel:
        print(f"Not correct channel '{ctx.channel}', looking for '{channel}'")
        return
    channelLL = get(ctx.guild.text_channels, name="live-lobbies")
    message = await channelLL.send(f"Faceit lobby created\n\nPlayers:\n{str(ctx.author.mention)}\n\nRange:\nNOT IMPLEMENTED YET")
    await message.add_reaction(get(ctx.guild.emojis, name="tick"))
    


@bot.command(name = "purge",pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx : context.Context, count = 20):
    flag = False
    if count > 20:
        count  = 20
        flag = True
   

    await ctx.channel.purge(limit=count)

    if flag:
        ctx.send("Messages to delete cannot be greater than 20")
    
    #await ctx.message.delete()


#Past this point are event handlings

@bot.event
async def on_command_error(ctx : context.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please send in all required arguments")

    print(error)

@verify.error
async def verifyError(ctx : context.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a FACEIT username to begin verification steps ")

bot.run(TOKEN)
del(TOKEN)
del(PREFIX)
del(FACEIT_TOKEN)
del(URL)
del(PORT)
del(USERNAME)
del(PASSWORD)