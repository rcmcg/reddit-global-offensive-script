from twilio.rest import Client
from script import send_text_message, get_reddit_instance

NUM_POSTS_TO_SCAN = 50

reddit = get_reddit_instance()

TEST_STRING = ''

# Find a self post (text only) to run the test on
for submission in reddit.subreddit('globaloffensive').hot(limit=NUM_POSTS_TO_SCAN):
    if submission.is_self and not submission.stickied:
        TEST_STRING = submission.title
        break

if TEST_STRING == '':
    print('No self post was found in the top', NUM_POSTS_TO_SCAN, 'posts')
else:
    # Scan hot for TEST_STRING and send the text message
    for submission in reddit.subreddit('globaloffensive').hot(limit=NUM_POSTS_TO_SCAN):
        if TEST_STRING in submission.title:
            print("Sending text message")
            send_text_message(submission)
            break
