import tweepy
import os
import spacy
from twitter_app.twitter_data_model import DB, Tweet, User

twitter_auth = tweepy.OAuthHandler(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_KEY_SECRET'])
twitter_api = tweepy.API(twitter_auth)

nlp = spacy.load('my_model')


def upsert_user(twitter_handle):
    try:
        twitter_user = twitter_api.get_user(twitter_handle)
        if User.query.get(twitter_user.id):
            db_user = User.query.get(twitter_user.id)
        else:
            db_user = User(id=twitter_user.id, name=twitter_handle)
        DB.session.add(db_user)

        user_tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode="extended")

        for tweet in user_tweets:
            vectorized_tweet = nlp(tweet.full_text).vector
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        raise e
    else:
        DB.session.commit()
    return db_user
