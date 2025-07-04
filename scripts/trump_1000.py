import os
import json
from mastodon import Mastodon
from dotenv import load_dotenv

# Load Mastodon token
load_dotenv()
access_token = os.getenv("MASTODON_TOKEN")
print("Token:", access_token)

# Initialize Mastodon client
mastodon = Mastodon(
    access_token=access_token,
    api_base_url='https://mastodon.social'  # change this if your server is different
)

# Search parameters
query = "Trump AND Netanyahu"
limit = 1000

# Run search and store results
search_results = mastodon.search(f"{query}", result_type="statuses")
toots = search_results['statuses'][:limit]
results = []

# Collect post data
for toot in toots:
    results.append({
        "created_at": toot['created_at'].isoformat(),
        "username": toot['account']['acct'],
        "content": toot['content'],
        "reblogs": toot['reblogs_count'],
        "favourites": toot['favourites_count']
    })

# Save to file
os.makedirs("data/raw", exist_ok=True)
filename = "data/raw/mastodon_trump_netanyahu.json"
with open(filename, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Saved {len(results)} posts to {filename}")
