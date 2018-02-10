# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 18:58:45 2018

@author: faraz

Reference: https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
"""

from tweepy import Stream
from tweepy.streaming import StreamListener
 
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True