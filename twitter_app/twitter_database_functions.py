import tweepy
from os import getenv
import os
import spacy
from .twitter_data_model import DB, Tweet, User

twitter_api = tweepy.OAuthHandler(
    getenv("TWITTER_API_KEY"),
    getenv("TWITTER_API_KEY_SECRET")
)

nlp_path = os.path.join('/'.join(os.path.abspath(__file__).split('/')[:-1]), 'my_model')
nlp = spacy.load(nlp_path)


def insert_user_or_update(twitter_handle, flag):
    try:
        twitter_user = twitter_api.get_user(twitter_handle)
        if User.query.get(twitter_user.id):
            db_user = User.query.get(twitter_user.id)
        else:
            db_user = User(id=twitter_user.id, name=twitter_handle)
        if flag == 'insert':
            DB.session.add(db_user)
        else:
            User.query.filter(User.name == twitter_handle).delete()
            DB.session.commit()

        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode="extended")

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            vectorized_tweet = nlp(tweet.full_text).vector
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        raise e
    else:
        DB.session.commit()
    return db_user

