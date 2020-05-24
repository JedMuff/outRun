# bot.py
import os

import discord
from discord.ext import commands
import operator
client = commands.Bot(command_prefix = '.')
from time import time
starttime=time()
import os
from dotenv import load_dotenv
from dotenv import find_dotenv
load_dotenv(dotenv_path=find_dotenv(), verbose=True) #seaches for the .env stops the programme if it cant be found
TOKEN = os.getenv("DISCORD_TOKEN") #retrieves discord token from .env file
print(TOKEN)
q = 1
WhiteList = []
Namelist = []

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
@client.command()
async def Help(ctx): ## what you think it does
    await ctx.send("First go to this link")
    await ctx.send("http://www.strava.com/oauth/authorize?client_id=48491&redirect_uri=http://localhost&response_type=code&scope=activity:read_all")
    await ctx.send("Login to your strava account and you should be directed to a page similar to this")
    await ctx.send(file=discord.File('Example.png'))
    await ctx.send("Choose your privacy settings and select Authorise")
    await ctx.send("It should then take you to a page you cant reach")
    await ctx.send(file=discord.File('Example2.png'))
    await ctx.send("Copy the highlighted code and use the .Code command followed by your copied code")
    await ctx.send(file=discord.File('Example3.png'))
    await ctx.send("Enter this and you should be added to the leaderboard")
@client.command()##takes the code given and the user who entered the code
async def Code(ctx, val: int):
    WhiteList.append(val)
    Namelist.append(ctx.message.author)
    await ctx.send(val)
@client.command() ##  lets user search through current list
async def List(ctx,x):
    await ctx.send(WhiteList[x])
    await ctx.send(Namelist[x])

print("bot online")
client.run(TOKEN)

print("10 seconds")
