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
import operator
from collections import Counter

from nltk.corpus import stopwords
import string

import streamListener as sl
import tokenizer as t

consumer_key = 'JFPPrFllbgNsL7DU0oeeXxDYc'
consumer_secret = 'N1Hflo3aTNfcRWATUSTz5QsDyffa86iwTQXL6EJgqkwOtvFeTV'
access_token = '939138889708687362-PvRLlT9V01sG2dQnzFrk9YCrnChQwdt'
access_secret = 'cxGbKvmqWzCpjJGL1DBO1fxn37jZqbIfAHTgxBy4B4S7v'    

def process_or_store(tweet):
    print(json.dumps(tweet))

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
#print(api.rate_limit_status())

#for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
#    print(status.text+"\n")
#    process_or_store(status._json)
#    with open('tweet_dump.json', 'a') as outfile:
#        json.dump(status._json, outfile)
    
def clearExistingFiles(user):
    if user is not "None":
        filename = user + "_tweet_dump.json"
        minfilename = user + "_tweet_dump.min.json"
    else:
        filename = "tweet_dump.json"
        minfilename = "tweet_dump.min.json"

    open(filename, 'w').close()
    open(minfilename, 'w').close()

def get_clArgs():
    clArgs = argparse.ArgumentParser(description="Tweet miner.")
    
    clArgs.add_argument("-f", "--filter", 
                        dest="filter", 
                        help="Trend Tweet stream filter. Must start with \'#\'.",
                        default="-") # To be implemented.
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
    clArgs.add_argument("-d", "--download",
                        dest="download",
                        help="Download tweets.",
                        default="False") # To be implemented.
    clArgs.add_argument("-s", "--separate",
                        dest="separate",
                        help="Stores tweets in seprate file. Use with download.",
                        default="False") # To be implemented.
    
    return clArgs

def trendStream(trendFilter = '#duck'):
    twitter_stream = sl.Stream(auth, sl.MyListener())
    twitter_stream.filter(track=[trendFilter])
    
def getminTweet(tweet):
    try:
        media_url = tweet.entities['media'][0]['media_url']
    except (AttributeError, KeyError):
        media_url = None
    
    tweet_min = {"time" : tweet.created_at.strftime("%A %d/%B/%Y at %I:%M:%S %p UTC +0000"), 
                 "screen_name" : tweet.user.screen_name,
                 "username" : tweet.user.name,
                 "tweet" : tweet.text,
                 "media_url" : media_url,
                 "id_str" : tweet.id_str,
                 "user_id_str" : tweet.user.id_str}

    
    return tweet_min

def generateJSON(tweet, mintweet, user, username):
    if user:
        filename = username + "_tweet_dump.json"
        minfilename = username + "_tweet_dump.min.json"
    else:
        filename = "tweet_dump.json"
        minfilename = "tweet_dump.min.json"
        
    with open(filename, 'a') as outfile:
        json.dump(tweet._json, outfile)
        outfile.write('\n')
        
    with open(minfilename, 'a') as minoutfile:
        json.dump(mintweet, minoutfile)
        minoutfile.write('\n')
        
def textTokenize(text):
    return t.preprocess(text)
    
def tweetAnalyizer(user):
    if user is not "None":
        minfilename = user + "_tweet_dump.min.json"
    else:
        minfilename = "tweet_dump.min.json"
    
    with open(minfilename, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            tokens = tweetAnalyizer(tweet['tweet'])
#            do_something_else(tokens)
            
def phraseCount(user):
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT', 'the', 'The']
    
    if user is not "None":
        fname = user + "_tweet_dump.min.json"
        phraseCountLog = user + "_commonPhrases.txt"
        
    else:
        fname = "tweet_dump.min.json"
        phraseCountLog = "commonPhrases.txt"
    
    count_all = Counter()
        
    with open(fname, 'r') as f:
        for line in f:
#            print("-------------------------------------")
#            print(line)
#            print("-------------------------------------")
            tweet = json.loads(line)            
            # Create a list with all the terms
            terms_stop = [term for term in textTokenize(tweet['tweet']) if term not in stop and len(term) > 2]
            # Update the counter
            count_all.update(terms_stop)
        # Print the first 20 most frequent words
        print(count_all.most_common(20))
    
    with open(phraseCountLog, 'w') as f:
        counter = 1
        for phrase in count_all.most_common(20):
            f.write(str(counter) + ": " + str(phrase) + "\n")
            counter += 1
        
    
def tweetWalker(args):    
    if args.user is not "None":
        for status in tweepy.Cursor(api.user_timeline, screen_name=args.user).items(int(args.count)):
            # Process a single status
            mintweet = getminTweet(status);
            print(mintweet)
            
            generateJSON(status, mintweet, True, mintweet['screen_name'])
            
            if args.photos == "True" and mintweet['media_url'] != None:
                directory = mintweet['screen_name'] + "_tweet"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                urllib.request.urlretrieve(mintweet['media_url'], directory + "/" + mintweet['screen_name'] + "_" + mintweet['media_url'].split('/')[-1])
                
    elif args.user is "None":
        for status in tweepy.Cursor(api.home_timeline).items(int(args.count)):
            # Process a single status
            mintweet = getminTweet(status);
            print(mintweet)
            
            generateJSON(status, mintweet, False, None)
        
            if args.photos == "True" and mintweet['media_url'] != None:
                directory = mintweet['screen_name'] + "_tweet"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                urllib.request.urlretrieve(mintweet['media_url'], directory + "/" + mintweet['screen_name'] + "_" + mintweet['media_url'].split('/')[-1])       
#    elif args.filter[0] is '#':
#        trendStream(trendFilter=args.filter)
        
    print("< |=== END ===| >")
                
    
    
def main():
    args = get_clArgs().parse_args()
    tweetWalker(args)
#    tweetAnalyizer(args.user)
    phraseCount(args.user)
    
    

if __name__ == '__main__':
    main()
    
    
    
