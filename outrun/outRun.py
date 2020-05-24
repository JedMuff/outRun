import discord
from discord.ext import commands
import operator
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
### retrieving environmental libaries###
import os
from dotenv import load_dotenv
from dotenv import find_dotenv
load_dotenv(dotenv_path=find_dotenv(), verbose=True) #seaches for the .env stops the programme if it cant be found
TOKEN = os.getenv("DISCORD_TOKEN") #retrieves discord token from .env file

# Changed by user on installation
# Competition constraints.
startDate = "2020-04-29T00:00:00Z" # Start date of competition
distance = 5000 # 5 KM

bot_directory = "C:\\Users\\Jed\\Documents\\outrun_website\\"
client_id = INSERT_CLIENT_ID_HERE
client_secret = INSERT_CLIENT_SECRET_HERE

# Constants
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

# Variable client is given as any statement prefixed by ".".
client = commands.Bot(command_prefix='.')
# These variables are stated because Python doesn't reserve the words null, true and false, without these statements the code will not run because the imported data has all three words throughout it.
null = None
true = True
false = False
# Gives an empty dictionary, which will be used for the final leaderboard.
leaderBoard = {}

def getRefreshTokens(username,code): # Gets the refresh tokens needed to get information from the strava account
    # Also stores in a file for later use
    # Payload is needed to send API command
    refresh_payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': "authorization_code",
        'f': 'json'
    }
    print("Requesting Refresh Token...")
    #try: # code will only work once so possibility of failing
    res1 = requests.post(auth_url, data=refresh_payload, verify=False) #API request
    refresh_token = res1.json()['refresh_token'] # Gets data
    print("Refresh Token = {}\n".format(refresh_token))
    # Writes it to storage
    f = open(bot_directory+"users.txt", "a+")
    f.write(username+" ; "+str(refresh_token)+"\n")
    f.close()
    return
    # except:
        # print("An error has occurred. Please try again")
        # print(res1) # Prints error
        # print()
        # return

def getActivityList(refresh_token):
    # get access token
    access_payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,#'492e30240f29029462739c25b7b78cb99de2bdbf'
        'grant_type': "refresh_token",
        'f': 'json'
    }
    print("Requesting Token...")
    try:
        res2 = requests.post(auth_url,data=access_payload, verify=False)
        access_token = res2.json()['access_token']
        print("Access Token = {}\n".format(access_token))

        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': 200, 'page': 1}
        activityList = requests.get(activites_url, headers=header, params=param).json()
        return activityList
    except:
        print("An error has occurred. Please try again")
        print(res2)
        print()
        return

def leaderBoard_update(user, activityList):
    # Filters lists by date and distance depending on competition constraints.
    for item in activityList:
        # test_filtered is the filtered list of test, filtered by date.
        activityList_filtered = list(filter(lambda i: i["start_date"] > startDate, activityList))

        # new_test is the filtered list of test_filtered, filtered by distance travelled.
        new_activityList = list(filter(lambda b: b["distance"] > distance, activityList_filtered))

    # Sorts the new_activityList by time values, in ascending order- so fastest time first.
    activityList_again = []
    for key in new_activityList:
        timing = key
        total = timing.get("moving_time")
        activityList_again = sorted(new_activityList, key=lambda h: h["moving_time"], reverse = True)
    # This for loop takes the first index of the activityList_again list and gets the name of the individual and their time- converted to minutes to two decimal places.
    for activityList_again[0] in activityList_again:
        again = activityList_again[0]
        id_name = {}
        id_name = again.get("athlete")

        tim = again.get("moving_time")
        tim = tim / float(60)
        tim = "%.2f" % tim
        # Adds the name and time to the leaderBoard dictionary.
        leaderBoard[user] = str(tim)
    # Empty dictionary called competitors.
    competitors = {}
    # For loop takes key and value from the leaderBoard dictionary and puts them into the competitors dictionary.
    for user in leaderBoard:
        competitors[user] = leaderBoard[user]
    return competitors


## Code for discord bot actions.
# Statement to begin event from client input.
@client.event
# Function on_ready prints "Bot online" to the monitor once the bot is active.
async def on_ready():
    print("Bot online")

# Statement for a bot command.
@client.command()
# Command defined as .work, ctx means context and is a shorter, better way of referring to specific channels in servers.
async def check(ctx):
    # Reads the file to get users
    f = open(bot_directory + "users.txt", "r")
    contents = f.read()
    users = contents.split('\n')
    names = []
    for name in users:
        names.append(name.split(' ; '))

    names.pop()
    for i in range(len(names)):
        print(names[i][0])
        my_dataset = getActivityList(names[i][1])  # gets the activity list of one person
        competitors = leaderBoard_update(names[i][0], my_dataset)

    # Sorts the competitors dictionary by fastest time from all competitors.
    competitors_sort = dict(sorted(competitors.items(), key=operator.itemgetter(1)))
    # Prints the statement to the channel along with the sorted competitors dictionary.
    await ctx.send("Leaderboard:\n")
    position = 0

    for i in competitors_sort:
        position = position + 1
        if(position == 1):
            await ctx.send(str(position)+"st) "+str(i) + " " + str(competitors_sort.get(i)) + " Minutes")
        elif (position == 2):
            await ctx.send(str(position) + "nd) " + str(i) + " " + str(competitors_sort.get(i)) + " Minutes")
        elif (position == 3):
            await ctx.send(str(position) + "rd) " + str(i) + " " + str(competitors_sort.get(i)) + " Minutes")
        else:
            await ctx.send(str(position)+"th) "+str(i) + " " + str(competitors_sort.get(i)) + " Minutes")

@client.command()
async def readme(ctx): ## what you think it does
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
async def code(ctx, val: str):
    getRefreshTokens(str(ctx.message.author), str(val))

# This statement sets up the bot, using the token identifier in the brackets.
client.run(TOKEN)
