# reddit-global-offensive-script
Simple Python script for scanning reddit.com/r/GlobalOffensive for updates to the game Counter Strike: Global Offensive. The script is hosted on Heroku and is run once per day at 11:00pm UTC (4:00pm PDT). The script checks if there has been an update by checking the 'hot' section of the subreddit for an official post about an update to the game. If a game update post is found, a text message is sent using Twilio.

