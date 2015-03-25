import bs4, sys, math, re, MySQLdb, types, urllib, urllib2, datetime, random, time, unicodedata, base64, socket
import requests, json
from datetime import datetime

def iterparse(file_obj):
    decoder = json.JSONDecoder()
    buf = ""
    for line in file_obj:
        buf += line.strip()
        try:
            res = decoder.raw_decode(buf)
            buf = ""
            yield res[0]
        except ValueError:
            pass


with open('database_bigdata_algorithm.20150318-165942.json') as data_file: 
	for obj in iterparse(data_file):
		hashtags = []
		screenName = obj["user"]["screen_name"]
		name = obj["user"]["name"]
		for tag in range(0,len(obj["entities"]["hashtags"])):
			hashtags.append(obj["entities"]["hashtags"][tag]["text"])
		favoriteCount = obj["favorite_count"][0]
		retweetCount = obj["retweet_count"][0]
		createdAt = obj["created_at"]
		coordinates = obj["coordinates"]

		print "Name: %35s, \tScreen Name: %15s, \tHashtags: %40s, \tFavorites %6s, \tRetweets: %6s, \tcreatedAt: %10s, \tCoordinates: %s" % \
			(name,screenName,hashtags,favoriteCount,retweetCount,createdAt,coordinates)
