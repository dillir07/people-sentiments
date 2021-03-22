import os
import tweepy

TWITTER_API_KEY = os.environ["TWITTER_API_KEY"]
TWITTER_API_SECRET = os.environ["TWITTER_API_SECRET"]
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]


auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def get_tweets(query, count=300, lang="en"):

    # empty list to store parsed tweets
    tweets = []
    fetched_tweets = api.search(query, count=count, lang=lang, result_type="recent")
    # parsing tweets one by one
    for tweet in fetched_tweets:
        tweets.append(tweet.text)
    return tweets


print(get_tweets(query="Donald Trump", count=30, lang="en"))
