import os
import tweepy
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import TextBlob

TWITTER_API_KEY = os.environ["TWITTER_API_KEY"]
TWITTER_API_SECRET = os.environ["TWITTER_API_SECRET"]
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]


auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

stmr = PorterStemmer()
stop_words = stopwords.words("english")

# regex patterns
url_pattern = re.compile(r"https://[\w\d./]*")
emoji_code_pattern = re.compile(r"\\u[\w\d]*")
mentions_pattern = re.compile(r"@[\w\d]*")
hashtags_pattern = re.compile(r"#[\w\d]*")
other_pattern = re.compile(r"[🤷♀️]")


def deEmojify(text):
    regrex_pattern = re.compile(
        pattern="["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    return regrex_pattern.sub(r"", text)


def get_sentiment_for_texts(texts: list):
    print("processing ", len(texts), " items")
    res = []
    for text in texts:
        tweet_data = {"original": text}
        # * here we are doing the following
        # * * converting to lower case
        # * * applying stem operation to convert running to run etc.
        # * * excluding stop words (common words) such as the, I , a, an etc.
        _ = " ".join(
            [stmr.stem(word.lower()) for word in text.split() if word not in stop_words]
        )
        _ = re.sub(url_pattern, "", _)
        _ = re.sub(emoji_code_pattern, "", _)
        _ = re.sub(mentions_pattern, "", _)
        _ = re.sub(hashtags_pattern, "", _)
        _ = re.sub(other_pattern, "", _)
        tweet_data["_"] = deEmojify(_)
        tweet_data["sentiment"] = TextBlob(text).sentiment
        res.append(tweet_data)

    # * we could try doing all of these using comprehensions
    # * but would become hard to understand and maintain.
    # texts = [text.lower() for text in texts]
    # texts = [[stmr.stem(word) for word in text if word not in stop_words] for text in texts]

    return res


def get_tweets(query, count=300, lang="en"):

    # empty list to store parsed tweets
    tweets = []
    fetched_tweets = api.search(query, count=count, lang=lang, result_type="popular")
    # parsing tweets one by one
    for tweet in fetched_tweets:
        tweets.append(tweet.text)
    return tweets


def get_tweets_with_sentiment(query: str, count: int, lang="en"):
    """
    gets given `count` number of tweets
    return a dict {text,_,sentiment}
    """
    tweets = get_tweets(query=query, count=count, lang=lang)
    data = get_sentiment_for_texts(tweets)
    return data
