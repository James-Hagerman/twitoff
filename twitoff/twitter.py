""" Retrieve Tweets, word embeddings, and populate DB"""
from os import getenv
import tweepy
import spacy
from .models import DB, tweet, user


# TWITTER_API_KEY = 'Q2jivjP6aHAPTEzCaIXSvnuW4'
# TWITTER_API_KEY_SECRET = 'oxNv2EqHrXt8T0NEGRaFE8HIbvEIYqBLDTJxK02Q1LEFHWaSc9'
# TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
# TWITTER = tweepy.API(TWITTER_API)

TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGo',
                 'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen',
                 'common_squirrel', 'KenJennings', 'conanobrien',
                 'big_ben_clock', 'IAM_SHAKESPEARE']

TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_API_KEY'),
                                   getenv('TWITTER_API_KEY_SECRET'))

TWITTER = tweepy.API(TWITTER_AUTH)
# Loading in nlp model and returning 300 size embedding

nlp = spacy.load('my_model')
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector



def add_or_update_user(username):
    """Allows us to add/update users to our DB"""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (user.query.get(twitter_user.id)) or user(id = twitter_user, name = username)
        DB.session.add(db_user)
        # We want as many recent non-retweet/reply statuses as we can get
        # 200 is a Twitter API limit, we will usually see less due to exclusions


        tweets = twitter_user.timeline(
            count = 200, exclude_replies = True,
            include_rts = False, tweet_mode = 'Extended', since_id = db_user.newest_tweet_id
    )
        if tweets:
            db_user.newest_tweet_id = tweets[0].id 
        for tweet in tweets: 
            # Calculating embedding on the full tweet, but truncate for storing
            # embedding now uses spacy
            embedding = vectorize_tweet(tweet.full_text)
            db_tweet = tweet(id = tweet.id, text = tweet.full_text[:300],
                             embedding = embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_test) 
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()

def add_users(users=TWITTER_USERS):
    """ 
    Add/update a list of users (string of user names).
    May take a while, so run "offline" (flask shell).
    """
    for user in users:
        add_or_update_user(user)

def update_all_users():
    """ Update all tweets for all users in the user table."""
    for user in user.query.all():
        add_or_update_user(user.name)

    #DB.session.commit()
