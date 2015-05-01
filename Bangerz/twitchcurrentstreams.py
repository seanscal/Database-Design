import bs4, sys, math, re, MySQLdb, types, urllib, urllib2, datetime, random, time, unicodedata, base64, socket
import requests, json
from datetime import datetime

'''
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''


hostname = '54.88.34.236'
username = 'bangerz'
password = 'gamera@1234'
dbname = 'bangerz'

con = MySQLdb.connect(host=hostname, port=3306, 
    user=username, passwd=password, db=dbname)
cursor = con.cursor()

def insertYoutubeChannel(channel, channelCreated, channelViews, channelFollowers, 
									streamGame, streamViewers, streamCreated):
  global cursor

  print 'testing ', channel   
  sql = "SELECT * FROM current_twitch_streams_and_channels WHERE channel = \'" + channel + "\'"
  cursor.execute(sql)
  result = cursor.fetchone()
  
  if result:
    print 'exists ', channel 
    sql = "UPDATE `current_twitch_streams_and_channels` SET `channel`=\"%s\",`channelCreated`=\"%s\",`channelViews`=%s,`channelFollowers`=%s,`streamGame`=\"%s\",`streamViewers`=%s,`streamCreated`=\"%s\" WHERE 1"  % \
        (channel, channelCreated, channelViews, channelFollowers, streamGame, streamViewers, streamCreated)
    updateinsert = "update"
  else:
    print 'inserting ',channel
    sql = "INSERT INTO `current_twitch_streams_and_channels`(`channel`, `channelCreated`, `channelViews`, `channelFollowers`, `streamGame`, `streamViewers`, `streamCreated`) VALUES (\"%s\",\"%s\",%s,%s,\"%s\",%s,\"%s\")" % \
        (channel, channelCreated, channelViews, channelFollowers, streamGame, streamViewers, streamCreated)
    updateinsert = "insert"
  print sql
  try:
    cursor.execute(sql)
  except:
    print 'failed %s for %s' % (updateinsert, channel)
    pass
  return True

getSource = requests.get("https://api.twitch.tv/kraken/streams?limit=500")
text = json.loads(getSource.text)


for stream in range(0,len(text['streams'])):

	streamViewers = text["streams"][stream]["viewers"]
	streamGame = text["streams"][stream]["game"]
	streamCreated = text["streams"][stream]["created_at"]
	
	channel = text["streams"][stream]["channel"]["name"]
	channelCreated = text["streams"][stream]["channel"]["created_at"]
	
	if "views" in text["streams"][stream]["channel"].keys():
		channelViews = text["streams"][stream]["channel"]["views"]
	else:
		channelViews = 0
	
	if "followers" in text["streams"][stream]["channel"].keys():
		channelFollowers = text["streams"][stream]["channel"]["followers"]
	else:
		channelFollowers = 0

	channelCreated = datetime.strptime(channelCreated, '%Y-%m-%dT%H:%M:%SZ')
	streamCreated = datetime.strptime(streamCreated, '%Y-%m-%dT%H:%M:%SZ')
	insertYoutubeChannel(channel, channelCreated, channelViews, channelFollowers, 
									streamGame, streamViewers, streamCreated)










