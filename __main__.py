import tweepy
from datetime import datetime, timedelta
import sys 
from os import environ

if __name__ == "__main__":

    consumer_key = environ['API_KEY']
    consumer_secret_key = environ['API_SECRET_KEY']
    access_token = environ['ACCESS_TOKEN']
    access_token_secret = environ['ACCESS_TOKEN_SECRET']

    # Authorize with the Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    delete_old_tweets()


# Delete tweets older than 365 days that are not pinned or favorited by user
def delete_old_tweets():

    # Loop through all tweets
    for status in tweepy.Cursor(api.user_timeline, screen_name=get_user().screen_name).items():

        # If the date is equal or older than one year from now
        if datetime.today() - timedelta(days=365) > status.created_at:
                
            # if the tweet is not a retweet
            if not hasattr(status, 'retweeted_status') and status.favorited == False:

                # Delete it
                try:
                    api.destroy_status(status.id)
                except:
                    print("Error while deleting tweet:", status.id)

def get_user():
    user = api.get_user('stephen_eades')
    return user