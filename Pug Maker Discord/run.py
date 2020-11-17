import discord
from discord.ext import commands
from discord.utils import get
import urllib.request, urllib.error, urllib.parse
from discord.ext.commands import has_role




import json

# read file
with open('credentials_discord.json', 'r') as myfile:
    data=myfile.read()

# parse file
creds_discord = json.loads(data)
#print(creds_discord)


TOKEN = str(creds_discord["TOKEN"])
PREFIX = str(creds_discord["PREFIX"])


url_start = "https://faceitstats.com/player,"
steam_pre = 'http://steamcommunity.com/id/'

bot = commands.Bot(command_prefix=PREFIX)

#bot.remove_command("help")

@bot.command(name = "ping")
async def respond(ctx):
    await ctx.send('pong')

@bot.command(name = "quit")
@has_role("Head Honchos")
async def close(ctx):

    await bot.close()

@bot.command(name = "vfaceit", pass_context=True)
async def vfaceit(ctx,arg):
    
    webpage = "https://faceitstats.com/player,"
    response = urllib.request.urlopen(webpage +arg)
    
    webcontentfs = str(response.read())

    index = webcontentfs.find("https://steamcommunity.com/profiles/")


    if (index == -1):
        await ctx.send("This isnt a faceit profile")
        return
    i_e = webcontentfs[index:].find('"')

    steamurl = webcontentfs[index:index+i_e]

    response = urllib.request.urlopen(steamurl)
    
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
    await ctx.send(f"index of found is {found}, faceit level is {faceitLevel}")
    role = discord.utils.get(ctx.author.guild.roles, name = "Linked")
    await ctx.author.add_roles(role)
    role = discord.utils.get(ctx.author.guild.roles, name = str(faceitLevel))
    await ctx.author.add_roles(role)
    print(faceitLevel)  

@bot.command(name = "verify", pass_context=True)
async def verify(ctx, arg):
    #print(ctx)
    found = -1

    if not str(arg).startswith(steam_pre):
        
        
        return
    
    #print(url)
    
    response = urllib.request.urlopen(str(arg))
    
    webcontent = str(response.read())
    
    
    
    p_s = webcontent.find(str('<div class="profile_summary">'))
    p_e = webcontent.find(str('<div class="profile_summary_footer">'))

    
    found = webcontent[p_s:p_e].find(str(ctx.author))

    if not found == -1:
        
        
        role = discord.utils.get(ctx.author.guild.roles, name = "Linked")
        
        await ctx.author.add_roles(role)
    
        
    
        
@bot.command(name = "print")
async def print_all(ctx, arg):
    await ctx.channel.send(ctx.author)
    await ctx.channel.send(ctx.message)
    







bot.run(TOKEN)