import os
import json
from datetime import datetime
from mastodon import Mastodon
from dotenv import load_dotenv

# Load Mastodon token
load_dotenv()
access_token = os.getenv("MASTODON_TOKEN")

# Initialize Mastodon client
mastodon = Mastodon(
    access_token=access_token,
    api_base_url='https://mastodon.social'  # change this if your server is different
)

# Parameters
query = "Trump"
since_date = "2025-06-15"
until_date = "2025-06-21"
limit = 500

# Convert date to datetime objects
since = datetime.strptime(since_date, "%Y-%m-%d")
until = datetime.strptime(until_date, "%Y-%m-%d")

# Storage
results = []

# Search public timeline with keyword filter
for toot in mastodon.timeline_hashtag(query.lower(), limit=limit):
    created_at = toot['created_at']
    if since <= created_at <= until:
        results.append({
            "created_at": created_at.isoformat(),
            "username": toot['account']['acct'],
            "content": toot['content'],
            "reblogs": toot['reblogs_count'],
            "favourites": toot['favourites_count']
        })

# Save results
os.makedirs("data/raw", exist_ok=True)
filename = f"data/raw/mastodon_trump_{since_date}_to_{until_date}.json"
with open(filename, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Saved {len(results)} posts to {filename}")


