import praw
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import argparse

# Load credentials from .env
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("SECRET")
user_agent = os.getenv("AGENT")

# Connect to Reddit API
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True, help="Reddit post URL")
args = parser.parse_args()

submission = reddit.submission(url=args.url)
submission.comments.replace_more(limit=None)

comments = []

def extract_comments(comment_list, parent=None):
    for comment in comment_list:
        comments.append({
            "id": comment.id,
            "parent_id": parent,
            "author": str(comment.author),
            "score": comment.score,
            "body": comment.body,
            "created_utc": comment.created_utc
        })
        extract_comments(comment.replies, parent=comment.id)

extract_comments(submission.comments)

# Save to JSON
os.makedirs("data/raw", exist_ok=True)
post_id = submission.id
filename = f"data/raw/reddit_{post_id}_comments.json"
with open(filename, "w") as f:
    json.dump(comments, f, indent=2)

print(f" Saved {len(comments)} comments to {filename}")