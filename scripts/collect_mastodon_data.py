import os
import json
from datetime import datetime, timezone
from mastodon import Mastodon
from dotenv import load_dotenv

# Load Mastodon token
load_dotenv()
access_token = os.getenv("MASTODON_TOKEN")
print("Token:", access_token)

# Initialize Mastodon client
mastodon = Mastodon(
    access_token=access_token,
    api_base_url='https://mastodon.social'
)

# Parameters
query = "trump"  # change this for testing
since_date = "2025-06-15"
until_date = "2025-06-21"
max_posts = 100

# Convert date to timezone-aware datetime objects
since = datetime.strptime(since_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
until = datetime.strptime(until_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

# Storage
results = []

# --- ✅ DEBUG: Collect first N results, no date filtering ---
print("🔍 Collecting posts without date filter...")
for i, toot in enumerate(mastodon.timeline_hashtag(query.lower(), limit=max_posts)):
    print(f"[{i+1}] {toot['created_at']} - {toot['account']['acct']} - {toot['content'][:80]}...")
    results.append({
        "created_at": toot['created_at'].isoformat(),
        "username": toot['account']['acct'],
        "content": toot['content'],
        "reblogs": toot['reblogs_count'],
        "favourites": toot['favourites_count']
    })

# --- 💤 Old loop with date filtering (commented out) ---
# next_page = None
# fetched = 0
# while True:
#     page = mastodon.timeline_hashtag(query.lower(), limit=40) if next_page is None else mastodon.fetch_next(next_page)
#     if not page:
#         break
#     for toot in page:
#         created_at = toot['created_at']
#         if since <= created_at <= until:
#             results.append({
#                 "created_at": created_at.isoformat(),
#                 "username": toot['account']['acct'],
#                 "content": toot['content'],
#                 "reblogs": toot['reblogs_count'],
#                 "favourites": toot['favourites_count']
#             })
#         fetched += 1
#         if fetched >= max_posts:
#             break
#     if fetched >= max_posts:
#         break
#     next_page = page

# Save results
os.makedirs("data/raw", exist_ok=True)
filename = f"data/raw/mastodon_{query.lower()}_{since_date}_to_{until_date}.json"
with open(filename, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Saved {len(results)} posts to {filename}")
