#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import bs4, sys, math,subprocess, re, MySQLdb, types, urllib, urllib2, datetime, random, time, unicodedata, base64, socket
from urlparse import urljoin
from urllib2 import URLError
import os.path
from datetime import datetime

'''
'http://socialblade.com/twitch/top/500/channelviews'
'''

hostname = '54.88.34.236'
username = 'gamera'
password = 'gamera@1234'
dbname = 'gamera'

con = MySQLdb.connect(host=hostname, port=3306, 
    user=username, passwd=password, db=dbname)
cursor = con.cursor()

def getIDs():
  f=open('channelviews.html')

  soup = bs4.BeautifulSoup(f)
  for script in soup.findAll('script'):
    script.extract()

  returnArray = []
  for names in soup.find_all('a')[76:576]:
    returnArray.append(names.text)

  return returnArray

def runWgetUrl(url):
  req = urllib2.Request(url)
  ok=False
  try:
    cmd = "wget %s" % (url)
    print "Running  subprocess %s " % (cmd)
    p=subprocess.Popen(cmd, shell=True)
    p.wait()
    print 'pid ', p.pid

    ok=True
  except IOError, e:
    ok=False
    print 'IOError', e.code

  if not ok:
    sys.exit(0)

def rename(files):
  cmd = "mv %s %s.html" % (files, files)
  p=subprocess.Popen(cmd, shell=True)
  p.wait()

def runGetSinglePlayerPages():
  ids = getIDs()
  newIds = []
  for name in ids:
    if os.path.isfile("%s.html" % name) == True:
      continue
    else:
      newIds.append(name)

  for names in newIds:
    url = "http://socialblade.com/twitch/user/%s" % names
    runWgetUrl(url)
    rename(names)

def insertTwitchStreamer(key, vals):
  global cursor

  print 'testing ', key   
  sql = "SELECT * FROM most_popular_twitch_streamers WHERE channel = \'" + key + "\'"
  cursor.execute(sql)
  result = cursor.fetchone()

  vals[2] = datetime.strptime(vals[2], '%Y-%m-%d')

  if vals[4] == '--':
    vals[4] = "No Recent Game Played"

  if vals[3] == '--':
    vals[3] = "No Team"
  
  if result:
    print 'exists ', key 
    sql = "UPDATE `most_popular_twitch_streamers` SET `Channel`=\"%s\",`Followers`=%s,`Views`=%s,`Date_Joined`=\"%s\", `Current_Team`=\"%s\", `Most_Recent_Game`= \"%s\" WHERE 1"  % \
            (key, vals[0], vals[1], vals[2], vals[3], vals[4])
    updateinsert = "update"
  else:
    print 'inserting ',key
    sql = "INSERT INTO `most_popular_twitch_streamers`(`Channel`, `Followers`, `Views`, `Date_Joined`, `Current_Team`, `Most_Recent_Game`) VALUES (\"%s\",%s,%s,\"%s\",\"%s\",\"%s\")" % \
          (key, vals[0], vals[1], vals[2], vals[3], vals[4])
    updateinsert = "insert"
  print sql
  try:
    cursor.execute(sql)
  except:
    print 'failed %s for %s' % (updateinsert, key)
    pass
  return True







if os.path.isfile("channelviews.html") == False:
  rename('channelviews')

  if os.path.isfile("channelviews") == False:
    req = urllib2.Request('http://socialblade.com/twitch/top/1000/channelviews')
    ok=False

    try:
      cmd = "wget %s" % ('http://socialblade.com/twitch/top/500/channelviews')
      print "Running  subprocess %s " % (cmd)
      p=subprocess.Popen(cmd, shell=True)
      p.wait()
      print 'pid ', p.pid
      ok=True

    except IOError, e:
      ok=False
      print 'IOError', e.code
    if not ok:
      sys.exit(0)
    rename('channelviews')

runGetSinglePlayerPages()

ids = getIDs()
returnDict = {}
ok = True

for name in ids:
  f=open("%s.html" % name)

  soup = bs4.BeautifulSoup(f)
  for script in soup.findAll('script'):
    script.extract()

  for stats in soup.find_all('div', {'class': "stats-top-data-content"})[:]:

    followers = int(soup.find_all('div', {'class': "stats-top-data-content"})[0].text.replace(',', ''))
    views = int(soup.find_all('div', {'class': "stats-top-data-content"})[1].text.replace(',', ''))
    date = soup.find_all('div', {'class': "stats-top-data-content"})[2].text
    team = soup.find_all('div', {'class': "stats-top-data-content"})[3].text
    game = soup.find_all('div', {'class': "stats-top-data-content"})[4].text

    returnDict[name] = [followers,views,date,team,game]

for key in sorted(returnDict.keys()):
  vals = returnDict[key]
  x = insertTwitchStreamer(key,vals)
  # print "Channel: %30s, Followers: %13s, Views: %14s, Date Joined: %15s, Current Team: %s, Most Recent Game: %s" % (keys, vals[0], vals[1], vals[2], vals[3], vals[4])















