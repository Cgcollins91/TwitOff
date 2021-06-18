
import tweepy
import os
import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()

# twitter_auth = tweepy.OAuthHandler(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_KEY_SECRET'])
# twitter_api = tweepy.API(twitter_auth)
# nasa = twitter_api.get_user("nasa")
# tweets = nasa.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode="Extended")
#
# tweet = tweets[0].text
#
# word2vect_text = nlp(tweet)
# print(word2vect_text.vector)
nlp.to_disk('my_model')





