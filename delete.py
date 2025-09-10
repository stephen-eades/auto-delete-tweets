"""
Delete (most of) your tweets using Tweepy v2 Client. 

Notes:
- Free api limits to retrieving up to 100 Posts per month.
- v2 timelines paginate; you'll delete up to the max retrievable timeline (historical depth limits apply).
- Requires tweet.write permission in user context.
"""

import os
from datetime import datetime, timezone, timedelta
import tweepy

# -----------------------------
# CONFIG (edit env vars, not code)
# -----------------------------
DRY_RUN = False  # False to actually delete tweets                 
SKIP_PINNED = True  # Don't delete the pinned tweet.
AGE_DAYS = None  # None or ex. 365              

# Credentials
client = tweepy.Client(
    bearer_token=os.environ["TW_BEARER_TOKEN"],
    consumer_key=os.environ["TW_CONSUMER_KEY"],
    consumer_secret=os.environ["TW_CONSUMER_SECRET"],
    access_token=os.environ["TW_ACCESS_TOKEN"],
    access_token_secret=os.environ["TW_ACCESS_TOKEN_SECRET"],
    wait_on_rate_limit=True,
)

def get_me():
    me = client.get_me(user_fields=["pinned_tweet_id"])
    if me.data is None:
        raise RuntimeError("Failed to resolve the authorized user.")
    return me.data

def should_delete(tweet, pinned_id, cutoff_dt):
    # Skip pinned
    if SKIP_PINNED and pinned_id and str(tweet.id) == str(pinned_id):
        return False
    # Optional age filter
    if cutoff_dt is not None and tweet.created_at is not None:
        return tweet.created_at < cutoff_dt
    return True

def delete_old_tweets():
    me = get_me()
    my_user_id = me.id
    pinned_id = getattr(me, "pinned_tweet_id", None)

    # Use optional cutoff datetime
    cutoff_dt = None
    if AGE_DAYS is not None:
        cutoff_dt = datetime.now(timezone.utc) - timedelta(days=AGE_DAYS)

    print(f"Authenticated as @{me.username} (id={my_user_id}). Pinned: {pinned_id}.")
    if DRY_RUN:
        print("DRY RUN is ON — no tweets will be deleted.\n")

    deleted = 0
    examined = 0

    # Fetch your tweets in reverse-chronological order
    paginator = tweepy.Paginator(
        client.get_users_tweets,
        id=my_user_id,
        tweet_fields=["created_at"],
        max_results=100,
        exclude=None  # can exclude specific types of posts: ['retweets','replies'] 
    )

    for page in paginator:
        if page.data is None or len(page.data) == 0:
            break
        for tweet in page.data:
            examined += 1
            if should_delete(tweet, pinned_id, cutoff_dt):
                if DRY_RUN:
                    print(f"[WOULD DELETE] {tweet.id}  created_at={tweet.created_at}")
                else:
                    try:
                        client.delete_tweet(tweet.id)
                        print(f"[DELETED] {tweet.id}  created_at={tweet.created_at}")
                        deleted += 1
                    except tweepy.TweepyException as e:
                        print(f"[ERROR] Failed to delete {tweet.id}: {e}")

    print(f"\nExamined: {examined}  Deleted: {deleted}  (DRY_RUN={DRY_RUN}, SKIP_PINNED={SKIP_PINNED}, AGE_DAYS={AGE_DAYS})")
