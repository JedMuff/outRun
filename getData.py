import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Changed by user on installation
bot_directory = "C:\\Users\\Jed\\Documents\\outrun_website\\"
client_id = "48491"
client_secret = '5586197e3f2480908459c131580245061f507da1'
# Constants
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

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
    try: # code will only work once so possibility of failing
        res1 = requests.post(auth_url, data=refresh_payload, verify=False) #API request
        refresh_token = res1.json()['refresh_token'] # Gets data
        print("Refresh Token = {}\n".format(refresh_token))
        # Writes it to storage
        f = open(bot_directory+"users.txt", "a+")
        f.write(username+" ; "+str(refresh_token)+"\n")
        f.close()
        return refresh_token # Returns the token
    except:
        print("An error has occurred. Please try again")
        print(res1) # Prints error
        print()
        return

def getActivityList(refresh_token):
    # get access token
    access_payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,#'492e30240f29029462739c25b7b78cb99de2bdbf'
        'grant_type': "refresh_token",
        'f': 'json'
    }
    print("Requesting Token...\n")
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

# Reads the file to get users
f=open(bot_directory+"users.txt", "r")
contents =f.read()
users = contents.split('\n')
names = []
for name in users:
    names.append(name.split(' ; '))
try:
    names.pop()
    print(names)
    for i in range(len(names)):
        my_dataset = getActivityList(names[i][1])# gets the activity list of one person
        print(my_dataset)
except:
    print("An error has occurred. Check number of users")
