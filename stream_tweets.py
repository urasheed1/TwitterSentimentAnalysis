import os
from dotenv import load_dotenv
import tweepy

# Load environment variables
load_dotenv()

# Setup Tweepy with your credentials
client = tweepy.Client(
    bearer_token=os.getenv('BEARER_TOKEN'),
    consumer_key=os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    access_token=os.getenv('ACCESS_TOKEN'),
    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
)
print("Bearer Token:", os.getenv('BEARER_TOKEN'))

# Define a class to handle the stream
class MyStream(tweepy.StreamingClient):
    def __init__(self, bearer_token, max_tweets):
        super().__init__(bearer_token)
        self.num_tweets = 0
        self.max_tweets = max_tweets

    def on_tweet(self, tweet):
        self.num_tweets += 1
        print(f"{tweet.text.encode('utf8')}")
        if self.num_tweets >= self.max_tweets:
            self.disconnect()

# Create an instance of the stream
my_stream = MyStream(client.bearer_token, max_tweets=5)

# Add rules to filter the tweets you want to track
# Replace 'python' with the actual keywords you want to stream
rule = tweepy.StreamRule("python")
my_stream.add_rules(rule)

# Start streaming
my_stream.filter()
