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

@bot.command(name = "verify", pass_context=True)
async def verify_steam(ctx, arg):
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