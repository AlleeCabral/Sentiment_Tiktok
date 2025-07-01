import tweepy
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--start_date", required=True, help="Start date (YYYY-MM-DD)")
parser.add_argument("--end_date", required=True, help="End date (YYYY-MM-DD)")
args = parser.parse_args()

# Convert to ISO 8601 format
start_date = f"{args.start_date}T00:00:00Z"
end_date = f"{args.end_date}T23:59:59Z"

# Load API credentials
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Authenticate
auth = tweepy.AppAuthHandler(api_key, api_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Search query
query = "Trump -filter:retweets"
lang = "en"
max_tweets = 1000

tweets = []

for tweet in tweepy.Cursor(api.search_tweets, 
                            q=query, 
                            lang=lang, 
                            tweet_mode='extended',
                            since=args.start_date, 
                            until=args.end_date).items(max_tweets):
    tweets.append({
        "created_at": str(tweet.created_at),
        "user": tweet.user.screen_name,
        "text": tweet.full_text,
        "likes": tweet.favorite_count,
        "retweets": tweet.retweet_count
    })

# Save JSON file with date range in filename
os.makedirs("data/raw", exist_ok=True)
filename = f"data/raw/twitter_trump_{args.start_date}_to_{args.end_date}.json"
with open(filename, "w") as f:
    json.dump(tweets, f, indent=2)

print(f"Saved {len(tweets)} tweets to {filename}")

