There are two parts to setting up this bot:the discord bot and the strava API.
Everything you need to run this bot is in the outun folder. Put this folder where you want to run the bot.
# Bot Setup
This is simple. All you have to do is put your bot token in the .env file were it says to inset it.
In the outrun python file you can also change the competition distance and start time at the top of the file.

# Strava API Setup
The strava API is fairly simple. First you have to create an app with strava. This is done by going to this link and putting in the values it requires. The wbesite value is needed but won't be used. Put any website in for this, it doesnt even have to be real.
https://www.strava.com/settings/api

After this is done you will need to get the client ID and Client Secret. This is put in at the top of outrun.py file where it says to insert it.

Done! the bot should be ready to go once you add it to the server you want.

