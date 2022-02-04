from ctypes import sizeof
import os
import sys
import time
import json
import datetime
from pymongo import MongoClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# MongoDB
client = MongoClient()
db = client["cryto_trading_bot"]
db.bitcoin_tweets.ensure_index("id", unique=True, dropDups=True)
collection = db.bitcoin_tweets

# Keywords
keywords = ['$btc', '#btc', 'btc', '$bitcoin', '#bitcoin', 'bitcoin']

# Only grab tweets in english
language = ['en']

# Twitter API stuff
consumer_key = "Lp5mSp9MfKjXZaC3Vikp5uiFw"
consumer_secret = "MzFaF3aE2HG6bArm8X09Qw3kHpD5gYz5eaWfkGAdHFM3OTpQck"
access_token = "1290868623985135618-z4UCpNErMw2fsibsN1emC4OxbphnGo"
access_token_secret = "PrUdx0Xwpqsw0KOCzkpV5WvnkiCvpk5KRBVfeCycxd5AP"

class StdOutListener(StreamListener):
    c=0
    def on_data(self, data):
        # print(data)

        t = json.loads(data)

        tweet_id = t['id_str']
        username = t['user']['screen_name']
        followers = t['user']['followers_count']
        text = t['text']
        hashtags = t['entities']['hashtags']
        timestamp = t['created_at']
        language = t['lang']

        created = datetime.datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y')

        tweet = {'id':tweet_id,
                'username':username,
                'followers':followers,
                'text':text,
                'hashtags':hashtags,
                'language':language,
                'created':created
                }

        os.system('clear')

        if collection.find_one({'id': { "$eq": tweet_id}}):
            print ('Tweet already exists!')
        else:
            print("New tweet! " + tweet_id)
            print(tweet)
            collection.save(tweet)
            # if db.collection.count()==20:
            #     return False

        # break
        # print(db.collection.count())
        return False

    def on_error(self, status):
        print(status)
        return True

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
                # print(consumer_key)
    stream = Stream(auth, l)
    # print(collection)
    stream.filter(track=keywords, languages=language)

