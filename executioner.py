# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 18:23:50 2018

@author: faraz
"""

import tweepy
from tweepy import OAuthHandler
import json
import argparse
import urllib.request
import os

import streamListener as sl

consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_secret = 'ACCESS_SECRET'    

def process_or_store(tweet):
    print(json.dumps(tweet))

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
#print(api.rate_limit_status())

#for status in tweepy.Cursor(api.home_timeline).items(10):
#    # Process a single status
##    print(status.text+"\n")
##    process_or_store(status._json)
#    with open('tweet_dump.json', 'a') as outfile:
#        json.dump(status._json, outfile)

def get_clArgs():
    clArgs = argparse.ArgumentParser(description="Tweet miner.")
    
    clArgs.add_argument("-f", "--filter", 
                        dest="filter", 
                        help="Trend Tweet stream filter. Must start with \'#\'.",
                        default="-")
    clArgs.add_argument("-u", "--user",
                        dest="user",
                        help="Get tweets of a certain user.",
                        default="None")
    clArgs.add_argument("-p", "--photos",
                        dest="photos",
                        help="Set it 'True' to download photos. Default is 'False'.",
                        default="False")
    clArgs.add_argument("-c", "--count",
                        dest="count",
                        help="Number of tweets to retrieve. Max is 100, Default is 25.",
                        default=25)
    clArgs.add_argument("-j", "--json",
                        dest="json",
                        help="Store/View in JSON format.",
                        default="False")
    clArgs.add_argument("-d", "--download",
                        dest="download",
                        help="Download tweets.",
                        default="False")
    clArgs.add_argument("-s", "--separate",
                        dest="separate",
                        help="Stores tweets in seprate file. Use with download.",
                        default="False")
    
    return clArgs

def trendStream(trendFilter = '#duck'):
    twitter_stream = sl.Stream(auth, sl.MyListener())
    twitter_stream.filter(track=[trendFilter])
    
def getminTweet(tweet):
    try:
        media_url = tweet.entities['media'][0]['media_url']
    except (AttributeError, KeyError):
        media_url = None
    
    tweet_min = {"time" : tweet.created_at, 
                 "screen_name" : tweet.user.screen_name,
                 "username" : tweet.user.name,
                 "tweet" : tweet.text,
                 "media_url" : media_url,
                 "id_str" : tweet.id_str,
                 "user_id_str" : tweet.user.id_str}
    
    return tweet_min
    
    
def main():
    args = get_clArgs().parse_args()
    
    if args.user is not "None":
        for status in tweepy.Cursor(api.user_timeline, screen_name=args.user).items(int(args.count)):
        # Process a single status
            mintweet = getminTweet(status);
            print(mintweet)
            
            if args.photos == "True" and mintweet['media_url'] != None:
                directory = mintweet['screen_name'] + "_tweet"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                urllib.request.urlretrieve(mintweet['media_url'], directory + "/" + mintweet['screen_name'] + "_" + mintweet['media_url'].split('/')[-1])
                
    else:
        for status in tweepy.Cursor(api.home_timeline).items(int(args.count)):
        # Process a single status
            print(getminTweet(status))
        
            if args.photos == "True" and mintweet['media_url'] != None:
                urllib.request.urlretrieve(mintweet['media_url'], mintweet['screen_name'] + "_" + mintweet['media_url'].split('/')[-1])

    print("< |=== END ===| >")
                
    if args.filter[0] is '#':
        trendStream(trendFilter=args.filter)

if __name__ == '__main__':
    main()
    
    
    
