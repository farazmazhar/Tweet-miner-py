# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 18:23:50 2018

@author: faraz
"""

import tweepy
from tweepy import OAuthHandler

consumer_key = 'CONSUMER-KEY'
consumer_secret = 'CONSUMER-SECRET'
access_token = 'ACCESS-TOKEN'
access_secret = 'ACCESS-SECRET'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)