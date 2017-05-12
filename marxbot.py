#!/usr/bin/python
# coding: utf-8

import tweepy
from tweepy import OAuthHandler
import linecache




def authenticate():
    '''
    authenticates with the necessary credentials, returns the shortened api
    '''
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

api = authenticate()


# get the linenumber of the last tweet

with open('tweetnumber', 'r') as statusfile:
    number = int(statusfile.read())

# get a tweet and tweet it
if number <= 9081:
    tweet = linecache.getline('kapital.tweets', number)
    tweet = tweet.rstrip()      # remove the trailing linebreak
    api.update_status(tweet)

# increase the linenumber by 1
with open('tweetnumber', 'w') as statusfile:
    statusfile.write(str(number+1))


