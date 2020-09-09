from twilio.rest import Client

import praw
import os

# Reddit constants
REDDIT_USERNAME = "rcmcgreddit"
USER_AGENT = "windows10:global-offensive-script:v1.0 (by /u/narcbebeets under /u/rcmcgreddit)"

# Official update posts have UPDATE_TITLE followed by the date of the update
GAME_UPDATE_POST_TITLE = "Counter-Strike: Global Offensive update for"

NUM_POSTS_TO_SCAN = 50
GAME_UPDATE_TEXT_MESSAGE_TITLE = "There is a new update for CSGO!"
GAME_UPDATE_OPERATION_TEXT_MESSAGE_TITLE = "There is a new operation for CSGO!"


def format_text(submission):
    """Formats a string to be sent via text message"""
    # Check if this update is an operation (a large, special type of game update)
    if 'Operation' in submission.selftext:
        title = GAME_UPDATE_OPERATION_TEXT_MESSAGE_TITLE
    else:
        title = GAME_UPDATE_TEXT_MESSAGE_TITLE

    if len(submission.selftext) > 1400:
        body = submission.selftext[:1400]
    else:
        body = submission.selftext

    text = '\n' + title + '\n\n' + submission.url + '\n\n' + body

    return text


def send_text_message(submission):
    """Sends a text using Twilio"""
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(body=format_text(submission),
                                     from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                                     to=os.environ.get('PERSONAL_PHONE_NUMBER'))


def get_reddit_instance():
    return praw.Reddit(client_id=os.environ.get('GLOBAL_OFFENSIVE_SCRIPT_CLIENT_ID'),
                       client_secret=os.environ.get('GLOBAL_OFFENSIVE_SCRIPT_CLIENT_SECRET'),
                       username=REDDIT_USERNAME,
                       password=os.environ.get('RCMCGREDDIT_PASSWORD'),
                       user_agent=USER_AGENT)


def main():
    reddit = get_reddit_instance()

    # Scan top NUM_POSTS_TO_SCAN on the 'hot' section of reddit.com/r/GlobalOffensive and check if there is an update
    for submission in reddit.subreddit('globaloffensive').hot(limit=NUM_POSTS_TO_SCAN):
        if GAME_UPDATE_POST_TITLE in submission.title:
            print("Sending text message")
            send_text_message(submission)
            break


if __name__ == '__main__':
    main()
